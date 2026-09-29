# EEG data for the upstream baseline

The upstream `train.py` and `Pretrain.py` expect a pickle dictionary saved with
the `.npy` filename suffix, containing `preprocessed_eeg_data`, `ch_names`, and
`times`. Do not replace these inputs with arbitrary `.pt` exports.

Use `LidongYang/EEG_Image_decode`, revision
`dbe34bb2407164f70883c661c76664f0d596e522`, directory
`Preprocessed_data_250Hz/`. The manifest in `scripts/things_eeg_manifest.json`
pins all 20 sizes and SHA256 hashes (103,521,660,090 bytes total).

On 2026-09-28, the executable Python AST of this repository's
`preprocess/preprocessing_utils.py` was compared with the data publisher's
[`EEG-preprocessing/preprocessing_utils.py`](https://github.com/dongyangli-del/EEG_Image_decode/blob/main/EEG-preprocessing/preprocessing_utils.py):
they were identical. This covers 63 ordered channels, 250 Hz resampling,
baseline correction, removal of the prestimulus samples, training-derived MVNN,
condition ordering, repetition shuffling, and dictionary serialization.
The MindAlign README does not pin a downloadable dataset revision; this is a
compatible published preprocessing version, not an author-confirmed checksum
of the exact files used for the MindAlign paper.

Expected EEG shapes before repetition averaging:

- Training: `(16540, 4, 63, 250)`.
- Test: `(200, 80, 63, 250)`.

On the file-transfer host (Bash), download without CPU-heavy hashing:

```bash
python scripts/prepare_things_eeg.py \
  --root /public/home/hugf2022/Things_EEG2 \
  --endpoint https://hf-mirror.com --workers 4 --download-only
```

Then run on allocated CPU resources (no external network required):

```bash
python scripts/prepare_things_eeg.py \
  --root /public/home/hugf2022/Things_EEG2 --workers 2 --verify-only
```

The default endpoint is the publisher's `https://huggingface.co`; the mirror
option is for server connectivity. Both are checked against the same pinned
publisher hashes. Interrupted downloads retain `.part` files and resume.
The script reserves an 8 GiB free-space margin and executes no downloaded
pickle while inspecting file headers. It does not alter EEG values or train
the model. Only `COMPLETE: 20 files verified` means all files passed verification;
`downloaded; SHA256 verification pending` is an intermediate state.

Point `--eeg_data_path` to
`/public/home/hugf2022/Things_EEG2/Preprocessed_data_250Hz`.
The upstream cached image/text features are restored under `features/`;
baseline reproduction does not require generating them again. Upstream text
loading still uses `./EEG2image/features/`, so provide that runtime directory
or a symlink to `features/` when starting training. Data preparation alone is
not a passed training or paper-reproduction experiment.
