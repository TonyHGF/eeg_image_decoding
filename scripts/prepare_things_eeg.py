"""Download the pinned EEG files used by the unchanged upstream data loader.

No pickle is executed: verification checks published SHA256 and parses only
the small pickle header to confirm the EEG shape. Run hashing on a CPU node.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import pickletools
import shutil
import subprocess
import time


REVISION = "dbe34bb2407164f70883c661c76664f0d596e522"
REPO = "LidongYang/EEG_Image_decode"
GIB = 1024 ** 3


def verify(path, entry):
    if path.stat().st_size != entry["size"]:
        raise ValueError(f"Size mismatch: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != entry["sha256"]:
        raise ValueError(f"SHA256 mismatch: {path}; retained for inspection")
    with path.open("rb") as handle:
        prefix = handle.read(512)
    ops = []
    # The first ndarray shape precedes the dtype object and the large payload.
    for op, arg, _ in pickletools.genops(prefix):
        ops.append((op.name, arg))
        if arg == "dtype":
            break
    expected = (200, 80, 63, 250) if "_test" in path.name else (16540, 4, 63, 250)
    numbers = [arg for name, arg in ops if name in ("BININT", "BININT1", "BININT2")]
    if tuple(numbers[-4:]) != expected or ("SHORT_BINUNICODE", "preprocessed_eeg_data") not in ops:
        raise ValueError(f"Unexpected EEG header: {path}")
    print(f"VERIFIED {entry['path']} shape={expected} sha256={digest.hexdigest()}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Things_EEG2 directory")
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("things_eeg_manifest.json"))
    parser.add_argument("--endpoint", default="https://huggingface.co")
    parser.add_argument("--workers", type=int, default=2, choices=range(1, 5))
    parser.add_argument("--subject", help="Optional single subject, e.g. sub-01")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    assert manifest["revision"] == REVISION and manifest["repo"] == REPO
    entries = [e for e in manifest["files"] if not args.subject or args.subject in Path(e["path"]).parts]
    if not entries:
        raise ValueError("No matching subject")
    root = args.root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    remaining = 0
    for entry in entries:
        target = (root / entry["path"]).resolve()
        if not target.is_relative_to(root):
            raise ValueError("Manifest path escapes destination")
        partial = target.with_suffix(target.suffix + ".part")
        have = target.stat().st_size if target.exists() else partial.stat().st_size if partial.exists() else 0
        remaining += max(0, entry["size"] - have)
    if shutil.disk_usage(root).free < remaining + 8 * GIB:
        raise OSError(f"Need {remaining / GIB:.2f} GiB plus 8 GiB free-space margin")

    def download(entry):
        target = root / entry["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            verify(target, entry)
            return
        partial = target.with_suffix(target.suffix + ".part")
        url = f"{args.endpoint.rstrip('/')}/datasets/{REPO}/resolve/{REVISION}/{entry['path']}"
        for attempt in range(4):
            if not partial.exists() or partial.stat().st_size < entry["size"]:
                print(f"DOWNLOAD {entry['path']} attempt={attempt + 1}", flush=True)
                command = ["curl", "-fsSL", "--continue-at", "-", "--connect-timeout", "30",
                           "--max-time", "3600", "--output", str(partial), url]
                with subprocess.Popen(command) as process:
                    while process.poll() is None:
                        if shutil.disk_usage(root).free < 8 * GIB:
                            process.terminate()
                            raise OSError("Shared filesystem has less than 8 GiB free; stopped download")
                        time.sleep(2)
                    if process.returncode:
                        if attempt == 3:
                            raise RuntimeError(f"curl failed for {entry['path']}: {process.returncode}")
                        time.sleep(5)
                        continue
            verify(partial, entry)
            partial.rename(target)
            return

    print(f"START revision={REVISION} files={len(entries)} remaining_bytes={remaining}", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(download, entries))
    print(f"COMPLETE: {len(entries)} files verified; root={root}", flush=True)


if __name__ == "__main__":
    main()
