"""Неделя 8, часть 0: assert без скобок у notna()."""

from __future__ import annotations

import pandas as pd


def broken_check() -> None:
    df = pd.DataFrame({"x": [1, None, 3]})
    # BUG: ссылка на метод, а не результат
    assert df["x"].notna, "x has nulls"
    print("[BROKEN] assert passed (wrong)")


def fixed_check() -> None:
    df = pd.DataFrame({"x": [1, None, 3]})
    assert df["x"].notna().all(), "x has nulls"
    print("[FIX] assert passed")


def main() -> None:
    print("--- broken (should pass incorrectly) ---")
    try:
        broken_check()
    except AssertionError as exc:
        print(f"[BROKEN] failed as expected: {exc}")

    print("--- fixed on data with NULL (should fail) ---")
    try:
        fixed_check()
    except AssertionError as exc:
        print(f"[FIX] caught nulls: {exc}")

    print("--- fixed on clean data ---")
    df = pd.DataFrame({"x": [1, 2, 3]})
    assert df["x"].notna().all(), "x has nulls"
    print("[FIX] clean data OK")


if __name__ == "__main__":
    main()
