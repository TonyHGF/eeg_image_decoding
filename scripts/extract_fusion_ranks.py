"""Reuse frozen checkpoints; reproduce old metrics and cache aligned ranks."""
import argparse
import gc
import hashlib
import json
from pathlib import Path
import random
import sys
import time

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from train import HYBRID, Proj_img
from rank_fusion import rank_scores


def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def normalize(x):
    return x / (x.norm(dim=-1, keepdim=True) + 1e-12)


def extract(args):
    config = json.loads(args.config.read_text(encoding='utf-8'))
    if config['checkpoint'] != 'lowest_validation_loss' or config['candidate_count'] != 200:
        raise ValueError('Unsupported extraction protocol')
    args.output.mkdir(parents=True, exist_ok=True)
    manifests = [json.loads((args.features / b / 'manifest.json').read_text()) for b in ('cn', 'openai')]
    if manifests[0]['images'] != manifests[1]['images'] or manifests[0]['captions_sha256'] != manifests[1]['captions_sha256']:
        raise ValueError('Shared candidate provenance mismatch')
    perm = np.random.RandomState(config['seed']).permutation(16540)
    split_hash = hashlib.sha256(perm.tobytes()).hexdigest()
    validation_indices = perm[:740]
    # Match 200-way test difficulty: one positive and 199 fixed validation distractors.
    rng = random.Random(config['seed'])
    val_candidates = np.array([sorted([i] + rng.sample([j for j in range(740) if j != i], 199))
                               for i in range(740)])
    val_truth = np.argmax(val_candidates == np.arange(740)[:, None], axis=1)
    for subject in args.subjects:
        started = time.time()
        target = args.output / f'sub{subject:02d}.npz'
        if target.exists():
            raise FileExistsError(f'Refusing to overwrite extracted ranks: {target}')
        torch.cuda.reset_peak_memory_stats()
        directory = args.eeg / f'sub-{subject:02d}'
        raw = np.load(directory / 'preprocessed_eeg_training.npy', allow_pickle=True)['preprocessed_eeg_data']
        val_eeg = raw[validation_indices].mean(axis=1).astype(np.float32)
        del raw
        raw = np.load(directory / 'preprocessed_eeg_test.npy', allow_pickle=True)['preprocessed_eeg_data']
        test_eeg = raw.mean(axis=1).astype(np.float32)
        del raw
        gc.collect()
        outputs = {'val_candidates': validation_indices[val_candidates], 'val_query_ids': validation_indices,
                   'val_truth': val_truth, 'test_candidates': np.tile(np.arange(200), (200, 1)),
                   'test_truth': np.arange(200)}
        audit = dict(subject=subject, split_sha256=split_hash, checkpoints={}, reproduction={},
                     config_sha256=file_hash(args.config), captions_sha256=manifests[0]['captions_sha256'])
        baseline_metadata = None
        all_val, all_test = [], []
        for backend in ('cn', 'openai'):
            run = args.runs / f'{backend}-shared'
            meta = json.loads((run / f'metrics_sub{subject:02d}.json').read_text())
            if meta['split_sha256'] != split_hash or meta['config']['seed'] != config['seed']:
                raise ValueError('Training split mismatch')
            if baseline_metadata:
                for key in ('split_sha256', 'loaded_parameter_keys', 'pretrain_checkpoint'):
                    if meta[key] != baseline_metadata[key]:
                        raise ValueError(f'Paired model mismatch: {key}')
            baseline_metadata = meta
            model, projection = HYBRID().cuda().eval(), Proj_img().cuda().eval()
            feature_dir = args.features / backend
            img_test = torch.load(feature_dir / 'image_test.pt', map_location='cpu', weights_only=True)['img_features'].cuda().float()
            txt_test = torch.from_numpy(np.load(feature_dir / 'text_test.npy')).cuda().float()
            img_val = torch.load(feature_dir / 'image_train.pt', map_location='cpu', weights_only=True)['img_features'][validation_indices].cuda().float()
            txt_val = torch.from_numpy(np.load(feature_dir / 'text_train.npy')[validation_indices]).cuda().float()
            prior = {'retrieval_topk': [], 'text_topk': []}
            audit['checkpoints'][backend] = []
            for position, epoch in enumerate(meta['selected_epochs'], 1):
                checkpoint_dir = run / 'model' / f'sub-{subject:02d}'
                eeg_path = checkpoint_dir / f'eeg_top{position}_epoch{epoch}.pth'
                img_path = checkpoint_dir / f'image_top{position}_epoch{epoch}.pth'
                model.load_state_dict(torch.load(eeg_path, map_location='cpu', weights_only=True), strict=True)
                projection.load_state_dict(torch.load(img_path, map_location='cpu', weights_only=True), strict=True)
                audit['checkpoints'][backend].append(dict(epoch=epoch, eeg_sha256=file_hash(eeg_path), image_sha256=file_hash(img_path)))
                for split, eeg, image, text in [('test', test_eeg, img_test, txt_test), ('val', val_eeg, img_val, txt_val)]:
                    if split == 'val' and position != 1:
                        continue
                    # Preserve original full-batch behavior, including upstream GAT limitation.
                    with torch.inference_mode():
                        z = normalize(model(torch.from_numpy(eeg).cuda(), torch.full((len(eeg),), subject - 1, device='cuda', dtype=torch.long)))
                        scores = [100 * z @ normalize(projection(image)).T, 100 * z @ normalize(text).T]
                    for modality, score in zip(('image', 'text'), scores):
                        if split == 'test':
                            order = score.softmax(-1).topk(10).indices.cpu().numpy()
                            prior['retrieval_topk' if modality == 'image' else 'text_topk'].append(
                                [float(np.any(order[:, :k] == np.arange(200)[:, None], axis=1).mean()) for k in range(1, 11)])
                        if position == 1:
                            matrix = score.cpu().numpy()
                            if split == 'val':
                                matrix = matrix[np.arange(740)[:, None], val_candidates]
                            (all_val if split == 'val' else all_test).append(rank_scores(matrix))
            for key, values in prior.items():
                actual = np.mean(values, axis=0)
                expected = np.array([meta[key][str(k)] for k in range(1, 11)])
                error = float(np.max(np.abs(actual - expected)))
                audit['reproduction'][f'{backend}_{key}'] = dict(max_absolute_error=error, reproduced=actual.tolist())
                if error > 1e-5:
                    raise ValueError(f'Previous test metric reproduction failed: {backend} {key} error={error}')
            del model, projection, img_test, txt_test, img_val, txt_val
            gc.collect()
            torch.cuda.empty_cache()
        outputs.update(val_ranks=np.stack(all_val), test_ranks=np.stack(all_test))
        np.savez_compressed(target, **outputs)
        audit.update(seconds=time.time() - started, peak_gpu_memory_bytes=torch.cuda.max_memory_allocated(), ranks_sha256=file_hash(target))
        target.with_suffix('.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
        print(f'COMPLETE subject={subject} seconds={audit["seconds"]:.1f} reproduction PASS', flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('config', 'eeg', 'features', 'runs', 'output'):
        p.add_argument(f'--{name}', type=Path, required=True)
    p.add_argument('--subjects', type=int, nargs='+', default=list(range(1, 11)))
    extract(p.parse_args())
