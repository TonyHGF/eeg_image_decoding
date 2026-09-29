"""GPU audit of cached feature identity, offline RN50s and MAE key coverage."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch
from PIL import Image
import cn_clip.clip as cn_clip
import open_clip
from eeg_encoders import HYBRID
from modules import ParameterGroupManager

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--assets', type=Path, required=True)
parser.add_argument('--cached', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
report = {}
for backend in ['cn', 'openai']:
    if backend == 'cn':
        model, transform = cn_clip.load_from_name('RN50', device='cuda', download_root=str(args.assets / 'weights'))
        tokenizer = cn_clip.tokenize
    else:
        model, _, transform = open_clip.create_model_and_transforms('RN50',
            pretrained='openai', cache_dir=str(args.assets / 'weights'), device='cuda')
        tokenizer = open_clip.get_tokenizer('RN50')
    model = model.float().eval()
    report[backend] = {}
    for split, indices in [('training', [0, 100, 10000]), ('test', [0, 199])]:
        paths = sorted((args.assets / 'images_set' / f'{split}_images').rglob('*.jpg'))
        pixels = torch.stack([transform(Image.open(paths[i]).convert('RGB')) for i in indices]).cuda()
        with torch.inference_mode():
            feats = torch.nn.functional.normalize(model.encode_image(pixels).float(), dim=-1).cpu()
            text = model.encode_text(tokenizer(['A photo of an object.']).cuda())
        short = 'train' if split == 'training' else 'test'
        cached = torch.load(args.cached / f'clip-rn50_features_{short}.pt', map_location='cpu', weights_only=True)['img_features']
        cached = torch.nn.functional.normalize(cached[indices].float(), dim=-1)
        report[backend][split] = dict(indices=indices, cosine_to_upstream=(cached * feats).sum(-1).tolist(),
                                     image_dim=feats.shape[1], text_dim=text.shape[1])
    del model
    torch.cuda.empty_cache()
ParameterGroupManager._COMPILED = ParameterGroupManager.compile_patterns()
eeg_model = HYBRID()
checkpoint = args.assets / 'mae/mae_pretrain_HYBRID_sub01_best.pth'
if checkpoint.exists():
    loaded = torch.load(checkpoint, map_location='cpu', weights_only=True)
    state = loaded.get('model_state', loaded)
    filtered = ParameterGroupManager.build_load_dict(eeg_model, state, ParameterGroupManager.parse_groups('ALL'))
    target = eeg_model.state_dict()
    report['mae'] = dict(top_level_keys=list(loaded), source_tensors=len(state), mapped_tensors=len(filtered),
                         target_tensors=len(target),
                         mismatches={k: [list(v.shape), list(target[k].shape)] for k,v in filtered.items()
                                     if v.shape != target[k].shape}, sample_keys=list(state)[:12])
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
