"""Regression tests for initialization, content checks and CLI exit codes."""

import contextlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from prepare import prepare
from self_check import check


class ToolTests(unittest.TestCase):
    """Use isolated temporary directories for every filesystem scenario."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.src, self.out = self.root / "input", self.root / "output"

    def run_check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return check(self.src, self.out)

    def test_initialize_and_preserve_205_files(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(prepare(self.src), 0)
            self.assertEqual(prepare(self.src, check_only=True), 0)
        self.assertEqual(len(list(self.src.iterdir())), 205)
        self.assertTrue((self.src / ".DS_Store").is_file())
        shutil.copytree(self.src, self.out)
        self.assertEqual(self.run_check(), 0)

    def test_missing_and_empty_directories_are_errors(self):
        with self.assertRaises(ValueError):
            self.run_check()
        self.src.mkdir()
        self.out.mkdir()
        with self.assertRaises(ValueError):
            self.run_check()

    def test_same_count_wrong_duplicate_multiplicity_fails(self):
        self.src.mkdir()
        self.out.mkdir()
        for name, payload in [("a", b"A"), ("a-copy", b"A"), ("b", b"B")]:
            (self.src / name).write_bytes(payload)
        for name, payload in [("a", b"A"), ("b", b"B"), ("b-copy", b"B")]:
            (self.out / name).write_bytes(payload)
        self.assertEqual(self.run_check(), 1)

    def test_broken_image_in_date_bucket_fails(self):
        self.src.mkdir()
        (self.out / "2025-06").mkdir(parents=True)
        (self.src / "fake.JPG").write_bytes(b"not a photo")
        (self.out / "2025-06/fake.JPG").write_bytes(b"not a photo")
        self.assertEqual(self.run_check(), 1)

    def test_existing_input_is_never_overwritten(self):
        with contextlib.redirect_stdout(io.StringIO()):
            prepare(self.src)
        path = self.src / "desktop.ini"
        path.write_bytes(b"my changes")
        with self.assertRaises(ValueError):
            prepare(self.src)
        self.assertEqual(path.read_bytes(), b"my changes")

    def test_modified_time_is_detected(self):
        with contextlib.redirect_stdout(io.StringIO()):
            prepare(self.src)
        path = self.src / "desktop.ini"
        os.utime(path, (1800000000, 1800000000))
        with self.assertRaises(ValueError):
            prepare(self.src, check_only=True)

    def test_check_only_does_not_create_input(self):
        with self.assertRaises(ValueError):
            prepare(self.src, check_only=True)
        self.assertFalse(self.src.exists())

    def test_nested_output_is_rejected(self):
        self.src.mkdir()
        with self.assertRaises(ValueError):
            check(self.src, self.src / "output")

    def run_cli(self, name, *args):
        """Run the real entry point using the same Python as the test suite."""
        script = Path(__file__).resolve().parents[1] / name
        return subprocess.run(
            [sys.executable, str(script), *map(str, args)],
            capture_output=True,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_cli_exit_codes_for_success_failure_and_missing_output(self):
        self.src.mkdir()
        self.out.mkdir()
        (self.src / "sample.txt").write_bytes(b"sample")
        (self.out / "sample.txt").write_bytes(b"sample")
        self.assertEqual(
            self.run_cli("self_check.py", self.src, self.out).returncode, 0
        )
        (self.out / "foreign.txt").write_bytes(b"foreign")
        self.assertEqual(
            self.run_cli("self_check.py", self.src, self.out).returncode, 1
        )
        self.assertEqual(
            self.run_cli(
                "self_check.py", self.src, self.root / "missing"
            ).returncode,
            2,
        )

    def test_cli_check_only_missing_input_does_not_write(self):
        result = self.run_cli("prepare.py", self.src, "--check")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.src.exists())
        self.assertIn("ERROR", result.stderr)

    def test_corrupt_archive_is_rejected_before_output_creation(self):
        data = Path(__file__).resolve().parents[1] / "data"
        damaged = self.root / "damaged-data"
        shutil.copytree(data, damaged)
        (damaged / "photos.zip").write_bytes(b"corrupt archive")
        with self.assertRaisesRegex(ValueError, "checksum"):
            prepare(self.src, data_dir=damaged)
        self.assertFalse(self.src.exists())


if __name__ == "__main__":
    unittest.main()
