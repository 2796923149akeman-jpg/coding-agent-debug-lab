"""Prepare verified input files with their original modification times."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(payload: bytes) -> str:
    """Return the SHA-256 checksum of a byte sequence."""
    return hashlib.sha256(payload).hexdigest()


def prepare(
    destination: Path,
    *,
    check_only: bool = False,
    data_dir: Path = ROOT / "data",
) -> int:
    """Initialize or check input; never overwrite an existing directory.

    Return zero on success. Raise ValueError for invalid or changed data and
    OSError for filesystem failures. Check-only mode never creates files.
    """
    destination = Path(destination).absolute()
    manifest = json.loads(
        (data_dir / "manifest.json").read_text(encoding="utf-8")
    )
    entries = manifest["files"]
    expected = {row["name"]: row for row in entries}
    if len(expected) != manifest["file_count"] or len(expected) != len(
        entries
    ):
        raise ValueError("Invalid dataset manifest")
    if any(
        Path(name).name != name
        or name in {".", ".."}
        or ":" in name
        or "\\" in name
        or "/" in name
        for name in expected
    ):
        raise ValueError("Unsafe dataset filename")
    if destination.is_symlink():
        raise ValueError("Input directory must not be a symbolic link")
    stamp = manifest["mtime_epoch"]
    if destination.exists():
        if not destination.is_dir():
            raise ValueError("Input path is not a directory")
        actual = list(destination.iterdir())
        if {p.name for p in actual} != set(expected) or any(
            not p.is_file() or p.is_symlink() for p in actual
        ):
            raise ValueError(
                "Existing input differs from dataset; use a fresh workspace"
            )
        for path in actual:
            row = expected[path.name]
            if (
                path.stat().st_size != row["size"]
                or digest(path.read_bytes()) != row["sha256"]
            ):
                raise ValueError(f"Input content changed: {path.name}")
            if abs(path.stat().st_mtime - stamp) > 1:
                raise ValueError(
                    f"Input modification time changed: {path.name}; "
                    "use a fresh workspace"
                )
        print(
            f"PASS: {len(actual)} input files; "
            "bytes and modification times unchanged"
        )
        return 0
    if check_only:
        raise ValueError(
            "Input directory is missing; run python prepare.py first"
        )

    archive_path = data_dir / "photos.zip"
    if digest(archive_path.read_bytes()) != manifest["archive_sha256"]:
        raise ValueError("Dataset archive checksum mismatch")
    # Validate the complete archive before creating any output.
    payloads = {}
    with zipfile.ZipFile(archive_path) as archive:
        if len(archive.namelist()) != len(expected) or set(
            archive.namelist()
        ) != set(expected):
            raise ValueError("Archive members differ from manifest")
        for name, row in expected.items():
            payload = archive.read(name)
            if len(payload) != row["size"] or digest(payload) != row["sha256"]:
                raise ValueError(f"Dataset checksum mismatch: {name}")
            payloads[name] = payload
    destination.mkdir(parents=True, exist_ok=False)
    for name, payload in payloads.items():
        target = destination / name
        with target.open("xb") as file:
            file.write(payload)
        os.utime(target, (stamp, stamp))
    print(f"Prepared {len(payloads)} files in {destination}")
    print(f"Modification time: {manifest['mtime_display']}")
    return 0


def main() -> int:
    """Parse command-line arguments and return zero or an error code of two."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "destination", nargs="?", type=Path, default=ROOT / "input"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="check existing input without writing",
    )
    args = parser.parse_args()
    try:
        return prepare(args.destination, check_only=args.check)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
