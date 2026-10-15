"""Verify the supplied exercise baseline, fixtures, tools and document links.

Run from the repository root before solving the exercises. This verifies the
distributed material, not a student's completed solution.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRADE = ROOT / "labs/01-grade-stats"
PHOTO = ROOT / "labs/02-photo-organizer"


def sha256(payload: bytes) -> str:
    """Return a content checksum."""
    return hashlib.sha256(payload).hexdigest()


def verify_fixtures() -> None:
    """Check the preserved grade source and every photo fixture byte."""
    source = json.loads((GRADE / "provenance.json").read_text("utf-8"))
    for name, expected in source["normalized_lf_sha256"].items():
        payload = (GRADE / name).read_bytes().replace(b"\r\n", b"\n")
        if sha256(payload) != expected:
            raise ValueError(f"Exercise baseline changed: {name}")
    manifest = json.loads((PHOTO / "data/manifest.json").read_text("utf-8"))
    archive_path = PHOTO / "data/photos.zip"
    if sha256(archive_path.read_bytes()) != manifest["archive_sha256"]:
        raise ValueError("Photo archive checksum mismatch")
    entries = manifest["files"]
    with zipfile.ZipFile(archive_path) as archive:
        names = [entry["name"] for entry in entries]
        if not (
            manifest["file_count"] == len(entries) == 205
            and len(names) == len(set(names))
            and sorted(archive.namelist()) == sorted(names)
        ):
            raise ValueError("Photo archive inventory mismatch")
        for entry in entries:
            payload = archive.read(entry["name"])
            if (
                len(payload) != entry["size"]
                or sha256(payload) != entry["sha256"]
            ):
                raise ValueError(f"Photo checksum mismatch: {entry['name']}")
    print("PASS: grade baseline and 205 photo fixtures")


def verify_documents_and_syntax() -> None:
    """Check links and Python syntax in the distributed source directories."""
    sources = [ROOT / "scripts", GRADE, PHOTO]
    ignored = {"input", "output", "reports", "__pycache__", ".venv"}
    for source in sources:
        for path in source.rglob("*.py"):
            if any(
                part in ignored or part.startswith(("output-", "reports-"))
                for part in path.relative_to(source).parts
            ):
                continue
            ast.parse(path.read_text("utf-8"), feature_version=(3, 10))
    documents = [ROOT / "README.md", ROOT / "AGENTS.md"]
    for folder in [ROOT / "docs", GRADE, PHOTO]:
        documents.extend(folder.rglob("*.md"))
    for path in documents:
        text = path.read_text("utf-8")
        if text.count("```") % 2:
            raise ValueError(f"Unpaired code fence: {path}")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            if not (path.parent / target.split("#")[0]).exists():
                raise ValueError(f"Broken local link: {path}: {target}")
    print("PASS: local Markdown links and Python 3.10 syntax")


def run_tests(
    folder: Path, arguments: list[str]
) -> subprocess.CompletedProcess:
    """Run tests with explicit UTF-8 output and no bytecode side effects."""
    return subprocess.run(
        [sys.executable, *arguments],
        cwd=folder,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={
            **os.environ,
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        check=False,
    )


def main() -> int:
    """Return zero only when the distributed exercise baseline is valid."""
    try:
        verify_fixtures()
        verify_documents_and_syntax()
        baseline = run_tests(GRADE, ["-m", "unittest", "-v"])
        result = baseline.stdout + baseline.stderr
        if not (
            baseline.returncode == 1
            and "Ran 3 tests" in result
            and "FAILED (errors=2)" in result
            and "ValueError" in result
        ):
            raise ValueError("Unexpected grade baseline:\n" + result)
        print("PASS: grade exercise has its 2 expected errors out of 3 tests")
        tools = run_tests(
            PHOTO, ["-m", "unittest", "discover", "-s", "tests", "-v"]
        )
        print(tools.stdout + tools.stderr)
        if tools.returncode != 0 or "Ran 0 tests" in tools.stderr:
            raise ValueError("Photo tool regression tests failed")
    except (OSError, ValueError, KeyError, SyntaxError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: repository baseline checks completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
