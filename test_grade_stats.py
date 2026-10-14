import csv
import tempfile
import unittest
from pathlib import Path

from grade_stats import summarize_scores


class GradeStatsTests(unittest.TestCase):
    def make_csv(self, rows):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "scores.csv"
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "score"])
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_all_scores_present(self):
        path = self.make_csv([
            {"name": "小王", "score": "80"},
            {"name": "小李", "score": "90"},
        ])
        self.assertEqual(
            summarize_scores(path),
            {"average": 85.0, "missing": 0},
        )

    def test_blank_score_is_skipped_and_counted(self):
        path = self.make_csv([
            {"name": "小王", "score": "80"},
            {"name": "小李", "score": ""},
            {"name": "小张", "score": "90"},
        ])
        self.assertEqual(
            summarize_scores(path),
            {"average": 85.0, "missing": 1},
        )

    def test_all_scores_blank(self):
        path = self.make_csv([
            {"name": "小王", "score": ""},
            {"name": "小李", "score": "   "},
        ])
        self.assertEqual(
            summarize_scores(path),
            {"average": None, "missing": 2},
        )


if __name__ == "__main__":
    unittest.main()
