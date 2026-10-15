"""Student checks: file count, content multiplicity and dated-image decoding.

This does not grade date accuracy or report completeness.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

IMAGE_SUFFIXES = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".webp",
    ".heic",
}
DATE_BUCKET = re.compile(r"^\d{4}(-\d{2})?$")


def sha256(path: Path) -> str:
    """Hash file contents in fixed-size chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(directory: Path) -> dict[Path, str]:
    """Map regular files to hashes; reject missing paths and symbolic links."""
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(
            f"Directory missing or not a real directory: {directory}"
        )
    files = {}
    for path in directory.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Symbolic links are not supported: {path}")
        if path.is_file():
            files[path] = sha256(path)
    return files


def check(source: Path, output: Path) -> int:
    """Print checks and return zero for pass or one for failed requirements.

    Raise ValueError for invalid input/output paths. Date accuracy and report
    completeness require separate checks by the student.
    """
    if source.is_symlink() or output.is_symlink():
        raise ValueError("Input and output must not be symbolic links")
    source, output = source.resolve(), output.resolve()
    if (
        source == output
        or source in output.parents
        or output in source.parents
    ):
        raise ValueError(
            "Input and output must be separate, non-nested directories"
        )
    before, after = inventory(source), inventory(output)
    if not before:
        raise ValueError("Input is empty; initialize the dataset first")
    before_counts, after_counts = (
        Counter(before.values()),
        Counter(after.values()),
    )
    foreign = [
        path for path, digest in after.items() if digest not in before_counts
    ]
    missing = before_counts - after_counts
    extra = after_counts - before_counts
    broken = []
    for path in after:
        relative = path.relative_to(output)
        if path.suffix.lower() in IMAGE_SUFFIXES and any(
            DATE_BUCKET.fullmatch(p) for p in relative.parts[:-1]
        ):
            try:
                with Image.open(path) as image:
                    image.load()
            except (
                OSError,
                ValueError,
                SyntaxError,
                Image.DecompressionBombError,
            ) as exc:
                broken.append((relative, type(exc).__name__))
    checks = [
        (
            "C1",
            len(before) == len(after),
            f"数量守恒: 输入 {len(before)} / 输出 {len(after)}",
        ),
        ("C2", not foreign, f"外来文件: {len(foreign)}"),
        (
            "C3",
            not missing and not extra,
            f"内容副本数: 缺少 {sum(missing.values())} / "
            f"多出 {sum(extra.values())}",
        ),
        ("C4", not broken, f"日期目录中打不开的图片: {len(broken)}"),
    ]
    for code, ok, description in checks:
        print(f"{code} {'PASS' if ok else 'FAIL'} | {description}")
    for path, reason in broken[:5]:
        print(f"  {path}: {reason}")
    groups = defaultdict(list)
    for path, digest in after.items():
        groups[digest].append(path)
    duplicates = [paths for paths in groups.values() if len(paths) > 1]
    print(
        f"信息: 输出中有 {len(duplicates)} 组字节相同的文件"
        "（不表示你已正确分类或报告）"
    )
    failures = [code for code, ok, _ in checks if not ok]
    print("未通过: " + (", ".join(failures) if failures else "无"))
    print("本自检不检查日期准确性、报告完整性、近重复质量或视频可播放性。")
    return 1 if failures else 0


def main() -> int:
    """Return 0 for pass, 1 for failed checks, or 2 for invalid arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        return check(args.source, args.output)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
