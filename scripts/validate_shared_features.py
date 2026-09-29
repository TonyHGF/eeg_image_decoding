"""Audit the shared-caption RN50 inputs on allocated CPU resources."""
import argparse
import hashlib
import json
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def validate(images, captions, features, output):
    import numpy as np
    import torch

    records = []
    for split, count in [('training', 16540), ('test', 200)]:
        paths = sorted(p for p in (images / f'{split}_images').rglob('*')
                       if p.suffix.lower() in {'.jpg', '.jpeg', '.png'})
        if len(paths) != count:
            raise ValueError(f'Image count mismatch: {split}')
        records.extend(dict(split=split, index=i, path=p.relative_to(images).as_posix())
                       for i, p in enumerate(paths))
    rows = [json.loads(line) for line in captions.read_text(encoding='utf-8').splitlines()]
    if len(rows) != len(records) or len({r['path'] for r in rows}) != len(records):
        raise ValueError('Caption count or uniqueness mismatch')
    by_path = {r['path']: r for r in rows}
    for record in records:
        row = by_path[record['path']]
        if any(row[k] != v for k, v in record.items()) or not row['caption'].strip():
            raise ValueError(f'Caption/image alignment mismatch: {record}')
    caption_hash = sha256(captions)
    report = dict(captions_sha256=caption_hash, image_count=len(records), backends={})
    for backend in ['cn', 'openai']:
        directory = features / backend
        manifest_path = directory / 'manifest.json'
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if manifest['images'] != records or manifest['captions_sha256'] != caption_hash:
            raise ValueError(f'Manifest alignment mismatch: {backend}')
        if manifest['backend'] != backend or manifest['model'] != 'RN50':
            raise ValueError(f'Manifest model mismatch: {backend}')
        result = dict(manifest_sha256=sha256(manifest_path), files={})
        for split, count in [('train', 16540), ('test', 200)]:
            for modality in ['image', 'text']:
                path = directory / f'{modality}_{split}.{ "pt" if modality == "image" else "npy"}'
                if modality == 'image':
                    array = torch.load(path, map_location='cpu', weights_only=True)['img_features'].numpy()
                else:
                    array = np.load(path, allow_pickle=False)
                if array.shape != (count, 1024) or array.dtype != np.float32 or not np.isfinite(array).all():
                    raise ValueError(f'Invalid feature shape/type/values: {path}')
                error = float(np.max(np.abs(np.linalg.norm(array, axis=1) - 1)))
                if error > 1e-4:
                    raise ValueError(f'Feature norm mismatch: {path}: {error}')
                result['files'][path.name] = dict(shape=list(array.shape), dtype=str(array.dtype),
                                                 max_norm_error=error, sha256=sha256(path))
                del array
        report['backends'][backend] = result
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ['images', 'captions', 'features', 'output']:
        parser.add_argument(f'--{argument}', type=Path, required=True)
    validate(**vars(parser.parse_args()))
