"""一个用于课堂演示的简单成绩统计程序。"""

import csv
import sys


def summarize_scores(csv_path):
    """读取成绩表，返回平均分和未填写数量。"""
    scores = []
    missing = 0

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            score_text = row["score"].strip()
            scores.append(float(score_text))

    average = round(sum(scores) / len(scores), 2)
    return {"average": average, "missing": missing}


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/scores.csv"
    result = summarize_scores(csv_path)

    if result["average"] is None:
        print("目前没有可统计的成绩")
    else:
        print(f"平均分：{result['average']}")
    print(f"未填写：{result['missing']} 人")


if __name__ == "__main__":
    main()
