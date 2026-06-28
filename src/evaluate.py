from __future__ import annotations

import json
from pathlib import Path

from src.filter import classify


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "data" / "benchmark_100_vi.jsonl"


def iter_rows(path: Path = BENCHMARK):
    with path.open(encoding="utf-8") as file:
        for line in file:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    rows = list(iter_rows())
    total = len(rows)
    correct = 0
    false_positive = 0
    false_negative = 0
    blocked_by_category: dict[str, list[int]] = {}

    for row in rows:
        result = classify(row["text"])
        expected = row["expected_decision"]
        actual = result.decision
        correct += actual == expected
        false_positive += expected == "allow" and actual == "block"
        false_negative += expected == "block" and actual == "allow"

        category = row["category"]
        bucket = blocked_by_category.setdefault(category, [0, 0])
        bucket[0] += actual == "block"
        bucket[1] += 1

    print(f"total: {total}")
    print(f"accuracy: {correct / total:.1%}")
    print(f"false_positive: {false_positive}")
    print(f"false_negative: {false_negative}")
    print("block_rate_by_category:")
    for category, (blocked, count) in sorted(blocked_by_category.items()):
        print(f"  {category}: {blocked}/{count} ({blocked / count:.1%})")


if __name__ == "__main__":
    main()
