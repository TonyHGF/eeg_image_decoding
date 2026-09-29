"""Freeze Qwen captions once, then encode identical images/text with both RN50s."""
import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import random
from clip_backends import load_backend


def images(root):
    records = []
    for split, expected in [('training', 16540), ('test', 200)]:
        paths = sorted(p for p in (root / f'{split}_images').rglob('*')
                       if p.suffix.lower() in {'.jpg', '.jpeg', '.png'})
        if len(paths) != expected:
            raise ValueError(f'{split}: found {len(paths)} images, expected {expected}')
        for i, path in enumerate(paths):
            records.append(dict(split=split, index=i, path=path.relative_to(root).as_posix()))
    return records


def captions(args, records):
    import torch
    from PIL import Image
    from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
    random.seed(2023)
    torch.manual_seed(2023)
    processor = AutoProcessor.from_pretrained(args.qwen_model, local_files_only=True)
    processor.tokenizer.padding_side = 'left'
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        args.qwen_model, local_files_only=True, torch_dtype=torch.float16,
        attn_implementation='sdpa').to('cuda').eval()
    done = {}
    if args.captions.exists():
        for line in args.captions.read_text(encoding='utf-8').splitlines():
            row = json.loads(line)
            done[row['path']] = row
    remaining = [r for r in records if r['path'] not in done]
    args.captions.parent.mkdir(parents=True, exist_ok=True)
    with args.captions.open('a', encoding='utf-8') as handle:
        for start in range(0, len(remaining), args.caption_batch):
            batch = remaining[start:start + args.caption_batch]
            pictures = [Image.open(args.images / r['path']).convert('RGB') for r in batch]
            prompts = []
            for row, picture in zip(batch, pictures):
                label = Path(row['path']).parent.name.split('_', 1)[1].replace('_', ' ')
                prompt = f'Describe only what is directly visible in the image of {label} in one short sentence.'
                messages = [dict(role='user', content=[dict(type='image', image=picture),
                                                       dict(type='text', text=prompt)])]
                prompts.append(processor.apply_chat_template(messages, add_generation_prompt=True, tokenize=False))
            inputs = processor(text=prompts, images=pictures, padding=True, return_tensors='pt').to('cuda')
            with torch.inference_mode():
                output = model.generate(**inputs, max_new_tokens=70, do_sample=False,
                                        repetition_penalty=1.2, no_repeat_ngram_size=3)
            decoded = processor.batch_decode(output[:, inputs.input_ids.shape[1]:], skip_special_tokens=True)
            for row, text in zip(batch, decoded):
                text = text.strip()[:210].strip()
                if not text:
                    raise ValueError(f'Empty caption: {row["path"]}')
                handle.write(json.dumps(dict(row, caption=text), ensure_ascii=False) + '\n')
            handle.flush()
            print(f'CAPTIONS {len(done) + min(start + len(batch), len(remaining))}/{len(records)}', flush=True)


def features(args, records):
    import numpy as np
    import torch
    from PIL import Image
    text_rows = [json.loads(s) for s in args.captions.read_text(encoding='utf-8').splitlines()]
    by_path = {r['path']: r for r in text_rows}
    if len(by_path) != len(records) or len(text_rows) != len(records):
        raise ValueError('Captions must cover each image exactly once')
    for row in records:
        saved = by_path[row['path']]
        if (saved['split'], saved['index']) != (row['split'], row['index']):
            raise ValueError('Caption order does not match image manifest')
    captions_hash = hashlib.sha256(args.captions.read_bytes()).hexdigest()
    for backend in args.backends:
        model, preprocess, tokenize = load_backend(backend, args.weights)
        model = model.float().eval()
        target = args.output / backend
        target.mkdir(parents=True, exist_ok=True)
        manifest = dict(backend=backend, model='RN50', dtype='float32',
                        captions_sha256=captions_hash, images=records)
        for split in ['training', 'test']:
            selected = [r for r in records if r['split'] == split]
            image_features, text_features = [], []
            for start in range(0, len(selected), args.batch_size):
                batch = selected[start:start + args.batch_size]
                pixels = torch.stack([preprocess(Image.open(args.images / r['path']).convert('RGB')) for r in batch]).cuda()
                tokens = tokenize([by_path[r['path']]['caption'] for r in batch]).cuda()
                with torch.inference_mode():
                    img = model.encode_image(pixels).float()
                    txt = model.encode_text(tokens).float()
                    img = torch.nn.functional.normalize(img, dim=-1)
                    txt = torch.nn.functional.normalize(txt, dim=-1)
                if img.shape[1] != 1024 or txt.shape[1] != 1024:
                    raise ValueError(f'Unexpected feature dimensions: {img.shape}, {txt.shape}')
                image_features.append(img.cpu())
                text_features.append(txt.cpu())
                if start % (args.batch_size * 20) == 0:
                    print(f'FEATURES {backend} {split} {start}/{len(selected)}', flush=True)
            short = 'train' if split == 'training' else 'test'
            torch.save({'img_features': torch.cat(image_features)}, target / f'image_{short}.pt')
            np.save(target / f'text_{short}.npy', torch.cat(text_features).numpy())
        (target / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        del model
        gc.collect()
        torch.cuda.empty_cache()
        print(f'COMPLETE {backend}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['captions', 'features'])
    parser.add_argument('--images', type=Path, required=True)
    parser.add_argument('--captions', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--weights', type=Path)
    parser.add_argument('--qwen-model', type=Path)
    parser.add_argument('--caption-batch', type=int, default=4)
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--backends', nargs='+', choices=['cn', 'openai'], default=['cn', 'openai'])
    args = parser.parse_args()
    os.environ.setdefault('HF_HUB_OFFLINE', '1')
    rows = images(args.images)
    globals()[args.stage](args, rows)
