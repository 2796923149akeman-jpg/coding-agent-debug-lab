import contextlib
import io
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from prepare import prepare
from self_check import check


class ToolTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.src, self.out = self.root / 'input', self.root / 'output'

    def run_check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return check(self.src, self.out)

    def test_initialize_and_preserve_205_files(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(prepare(self.src), 0)
            self.assertEqual(prepare(self.src, check_only=True), 0)
        self.assertEqual(len(list(self.src.iterdir())), 205)
        self.assertTrue((self.src / '.DS_Store').is_file())
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
        for name, payload in [('a', b'A'), ('a-copy', b'A'), ('b', b'B')]:
            (self.src / name).write_bytes(payload)
        for name, payload in [('a', b'A'), ('b', b'B'), ('b-copy', b'B')]:
            (self.out / name).write_bytes(payload)
        self.assertEqual(self.run_check(), 1)

    def test_broken_image_in_date_bucket_fails(self):
        self.src.mkdir()
        (self.out / '2025-06').mkdir(parents=True)
        (self.src / 'fake.JPG').write_bytes(b'not a photo')
        (self.out / '2025-06/fake.JPG').write_bytes(b'not a photo')
        self.assertEqual(self.run_check(), 1)

    def test_existing_input_is_never_overwritten(self):
        with contextlib.redirect_stdout(io.StringIO()):
            prepare(self.src)
        path = self.src / 'desktop.ini'
        path.write_bytes(b'my changes')
        with self.assertRaises(ValueError):
            prepare(self.src)
        self.assertEqual(path.read_bytes(), b'my changes')

    def test_modified_time_is_detected(self):
        with contextlib.redirect_stdout(io.StringIO()):
            prepare(self.src)
        path = self.src / 'desktop.ini'
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
            check(self.src, self.src / 'output')


if __name__ == '__main__':
    unittest.main()
