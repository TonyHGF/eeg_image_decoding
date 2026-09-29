# Paired rank fusion experiment

Frozen grid: C = 1, 4/3, 5/3, 2; L = 5, 10. Each candidate ID represents
one image and its fixed Qwen caption. Each branch contributes
`weight * (C + 1) / (C + rank)` if rank <= L, otherwise zero.

Two equally weighted branches (CN image, OpenAI text) and four equally weighted
branches (CN image, CN text, OpenAI image, OpenAI text) give 16 fusion settings.
Four single-branch baselines are evaluated using the same frozen checkpoints.
No embedding alignment, retraining, similarity-score calibration or learned
branch weights are introduced. Configuration: `configs/rank_fusion.json`.

Each backend uses its lowest-validation-loss checkpoint. This differs from the
earlier report's average of three checkpoint metrics; do not directly attribute
differences from that report to fusion. As an extraction check, all three saved
checkpoints are also evaluated against the earlier Top-1 through Top-10 metrics;
any mismatch above 1e-5 stops execution before the rank cache is written.

Validation uses the original 740 held-out images. Each validation query has its
positive and 199 fixed seed-2023 distractors from the validation set, matching
the 200-candidate test size. EEG inference retains the original batch grouping
(740 validation, 200 test) because the upstream GAT has a batch-index limitation.
Test candidates are all 200 test image/caption pairs. The same candidate sets,
pair IDs, caption hash, EEG split and author pretraining identities are checked
across backends. Saved checkpoint and rank-cache hashes provide provenance.

Select one C/L per branch combination using mean validation Top-1, then Top-5,
then configuration order. Choose the overall family by the same validation
rule. Test results for all fixed settings are descriptive, not a test-based
selection procedure. This is an exploratory follow-up after inspecting the
previous test results, with one seed and ten within-subject models.

Numerical ties use vote rounded to 12 decimals, then lower weighted mean rank
over all candidates, then ascending candidate ID. The secondary rank rule only
breaks exact ties; candidates outside L have zero primary vote. Top-1 tie rates
are reported. Each output prediction contains one candidate ID, image path,
caption and the four branch ranks, keeping image/text selection paired.

Local PowerShell checks (no duplicate ML environment required):

```powershell
python -m unittest discover -s tests -p test_rank_fusion.py
python -m py_compile scripts/extract_fusion_ranks.py scripts/evaluate_rank_fusion.py
```

On an allocated server GPU, with the existing environment and shared datasets:

```bash
python scripts/extract_fusion_ranks.py --config configs/rank_fusion.json --eeg /path/to/Preprocessed_data_250Hz --features /path/to/assets/features --runs /path/to/20260929 --output /path/to/fusion/ranks --subjects 1
python scripts/evaluate_rank_fusion.py --config configs/rank_fusion.json --ranks /path/to/fusion/ranks --captions /path/to/shared-qwen-captions.jsonl --output /path/to/fusion/smoke --subjects 1
```

Use a clean frozen checkout with `slurm/run.sh FULL_SHA python ...`. After the
subject-1 smoke passes, extract subjects 2..10 into the same ranks directory
(existing subject files are never overwritten), then omit `--subjects` for the
full report. Extraction uses one A100, four CPUs, 32 GiB RAM; evaluation can use
allocated CPUs or run locally with NumPy after downloading only rank metadata.

Outputs: all per-subject Top-1..10, group mean/sample-SD tables, validation-selected
parameters, paired differences against all four single branches, and per-query
paired predictions. Large EEG data and model weights remain on the server.
