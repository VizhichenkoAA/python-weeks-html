"""Неделя 4, часть 0: many-to-many merge и исправление."""

from __future__ import annotations

import pandas as pd


def broken_merge() -> pd.DataFrame:
    left = pd.DataFrame({"id": [1, 1, 2], "value": [10, 11, 20]})
    right = pd.DataFrame({"id": [1, 1, 2], "name": ["A", "A_dup", "B"]})
    merged = left.merge(right, on="id", how="left")
    print("=== Broken merge ===")
    print(len(left), "->", len(merged))
    print(merged)
    return merged


def fixed_merge() -> pd.DataFrame:
    left = pd.DataFrame({"id": [1, 1, 2], "value": [10, 11, 20]})
    right = pd.DataFrame({"id": [1, 1, 2], "name": ["A", "A_dup", "B"]})
    right_unique = right.drop_duplicates(subset=["id"], keep="first")
    merged = left.merge(right_unique, on="id", how="left", validate="many_to_one")
    print("=== Fixed merge (unique reference + validate) ===")
    print(len(left), "->", len(merged))
    print(merged)
    return merged


if __name__ == "__main__":
    broken_merge()
    fixed_merge()
