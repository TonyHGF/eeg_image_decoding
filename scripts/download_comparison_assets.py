"""Download fixed public model revisions on the file-transfer host."""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import time


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, required=True)
parser.add_argument('--endpoint', default='https://huggingface.co')
args = parser.parse_args()
os.environ['HF_ENDPOINT'] = args.endpoint
os.environ['HF_HUB_DISABLE_XET'] = '1'
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '120'
from huggingface_hub import hf_hub_download, snapshot_download

args.root.mkdir(parents=True, exist_ok=True)
weights = args.root / 'weights'
weights.mkdir(exist_ok=True)

def retry(function, **kwargs):
    for attempt in range(4):
        try:
            return function(**kwargs)
        except Exception:
            if attempt == 3:
                raise
            time.sleep(10)


print('Download CN-CLIP RN50', flush=True)
retry(hf_hub_download, repo_id='OFA-Sys/chinese-clip-rn50',
      revision='717ba215769231e53b9b7c6b9d329b9cc5944418', filename='clip_cn_rn50.pt', local_dir=weights)
print('Download OpenAI RN50', flush=True)
expected = 'afeb0e10f9e5a86da6080e35cf09123aca3b358a0c3e3b6c78a7b63bc04b6762'
path = weights / 'RN50.pt'
if not path.exists():
    subprocess.run(['curl', '-fsSL', '--retry', '4', '--connect-timeout', '30', '--max-time', '1800',
                    '--continue-at', '-', '-o', str(path.with_suffix('.pt.part')),
                    f'https://openaipublic.azureedge.net/clip/models/{expected}/RN50.pt'], check=True)
    path.with_suffix('.pt.part').rename(path)
with path.open('rb') as handle:
    digest = hashlib.sha256()
    for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b''):
        digest.update(chunk)
if digest.hexdigest() != expected:
    raise ValueError('OpenAI model SHA256 mismatch')
print('Download author MAE checkpoints', flush=True)
retry(snapshot_download, repo_id='anon-eeg/EEG-pretrained', repo_type='dataset',
      revision='1e1a895c047c7ab9bbcd634dcc538ef4edfd3579', allow_patterns=['*.pth'],
      local_dir=args.root / 'mae', max_workers=4)
print('Download Qwen2-VL-7B-Instruct', flush=True)
retry(snapshot_download, repo_id='Qwen/Qwen2-VL-7B-Instruct',
      revision='eed13092ef92e448dd6875b2a00151bd3f7db0ac',
      allow_patterns=['*.json', '*.safetensors', '*.txt', '*.model', '*.jinja'],
      local_dir=args.root / 'qwen', max_workers=4)
print('ALL MODEL DOWNLOADS COMPLETE', flush=True)
