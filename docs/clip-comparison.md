# CN-CLIP / OpenAI RN50 comparison

## Completed upstream smoke

The unchanged upstream training source at `a31dd8b` completed subject 1,
one epoch, batch 64, seed 2023, `--no_pretrain`, with the four upstream cached
features. Job 4154367 exited 0 on an A100. Image retrieval top-1/top-5 was
20.5%/47%; text retrieval top-1/top-5 was 2.5%/9.5%. These are pipeline checks,
not final trained-model results.

## Conditions and controls

1. **CN cached**: the exact upstream image/text feature bytes.
2. **CN shared captions**: CN-CLIP RN50, regenerated features with frozen Qwen captions.
3. **OpenAI shared captions**: OpenAI CLIP RN50, using those same images/captions.

The original caption strings are absent from the repository. Therefore 2 vs 3
is the controlled encoder comparison. Condition 1 is the upstream cached-feature
reference; its difference from 3 also includes caption-generation differences.
The shared captions follow the upstream English prompt, Qwen2-VL-7B-Instruct,
70-token generation limit, repetition penalty 1.2 and 210-character trimming.
Generation is deterministic and saved once; no tuning uses the test scores.

Use the same 10 in-subject datasets, seed 2023, 740 validation images, HYBRID
encoder, loss alpha=0.1, AdamW/lr/weight decay, and 150-epoch cap with the upstream
validation-loss early stopping. Validate feasible batch size before freezing it
for all conditions. Use `--init_groups T` to keep constructor/checkpoint weights.
When author MAE checkpoints load correctly, use the same checkpoint per subject
for every condition. Record a scratch comparison separately if needed.

Report all upstream metrics: image and text retrieval top-1 through top-10,
2/4/10/20/50/100-way scores; individual subjects and group means; validation loss,
chosen epochs, wall time and peak GPU allocation. The upstream 'ensemble' is
the mean of metrics across three validation-selected checkpoints, not fused
predictions. Text retrieval is caption retrieval among 200 images, not a new
semantic-class classification dataset. Keep these interpretations in reports.

## Necessary training fixes

- Respect text CLI paths and Slurm GPU assignment; create output directories.
- Load selected checkpoint keys into the unwrapped encoder with `strict=True`;
  upstream saved unwrapped keys but reloaded into DataParallel with
  `strict=False`, which can silently skip the EEG weights.
- Reject missing/invalid MAE checkpoints and reinitialization after loading;
  preserve the explicit `--no_pretrain` path.
- Save per-subject models/results, split hashes and training histories.
- Use identical seeded candidate sets for each k-way evaluation across models.

No EEG model architecture or loss redesign is included. The upstream GAT edge
index only describes the first graph of a batch; this is a known limitation
retained consistently in these baseline comparisons. A GAT correction would
require a separate labeled ablation, not silent incorporation in one condition.

## Commands

PowerShell syntax check (the user requested server-only environment setup):

```powershell
python -m compileall -q train.py scripts
```

Bash on a network-enabled transfer host:

```bash
python scripts/download_comparison_assets.py --root /path/to/assets --endpoint https://hf-mirror.com
```

On allocated GPU resources, generate captions, then encode both backends:

```bash
python scripts/build_clip_features.py captions --images /path/to/images_set --captions /path/to/captions.jsonl --qwen-model /path/to/assets/qwen
python scripts/build_clip_features.py features --images /path/to/images_set --captions /path/to/captions.jsonl --weights /path/to/assets/weights --output /path/to/features
python train.py --subjects 1 --epoch 2 --batch-size 64 --no_pretrain --init_groups T --eeg_data_path /path/to/Preprocessed_data_250Hz --img_train_path /path/to/features/cn/image_train.pt --img_test_path /path/to/features/cn/image_test.pt --text_train_path /path/to/features/cn/text_train.npy --text_test_path /path/to/features/cn/text_test.npy --result_path /path/to/run/
```

Create a log directory, then submit from a clean frozen checkout using
`sbatch` resource flags followed by `slurm/run.sh FULL_SHA python ...`.
Inspect `squeue`, `sacct`, logs and per-subject JSON/CSV outputs. All large
model assets and experimental outputs live on `/home_data`; verified EEG
stays under `/public/home/hugf2022/Things_EEG2/Preprocessed_data_250Hz`.
