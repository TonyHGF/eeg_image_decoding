#!/usr/bin/env bash
# Submit from the fixed checkout with resource flags on sbatch.
set -euo pipefail
expected_commit=$1
shift
cd "${SLURM_SUBMIT_DIR:?}"
test "$(git rev-parse HEAD)" = "$expected_commit"
test -z "$(git status --porcelain --untracked-files=normal)"
set +u  # Conda's compiler activation hooks read unset toolchain variables.
source "${CONDA_BASE:-$HOME/anaconda3}/etc/profile.d/conda.sh"
conda activate eeg-image-decoding-hpc
set -u
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
printf 'COMMIT=%s JOB=%s NODE=%s CUDA=%s\n' "$expected_commit" "$SLURM_JOB_ID" "$SLURM_JOB_NODELIST" "${CUDA_VISIBLE_DEVICES:-unset}"
printf 'COMMAND:'
printf ' %q' "$@"
printf '\n'
"$@"
