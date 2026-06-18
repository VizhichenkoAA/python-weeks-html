"""Неделя 3, часть 0: диагностика чтения CSV (sep, dtype, пропуски)."""

from __future__ import annotations

import pandas as pd
from io import StringIO


def demo_broken_read() -> None:
    csv_text = "id;value\n1;10\n2;20\n3;30\n"
    # BUG: sep не указан -> pandas ожидает запятую
    df = pd.read_csv(StringIO(csv_text))
    print("=== Broken read ===")
    print(df.dtypes)
    try:
        print(df["value"].mean())
    except KeyError as exc:
        print("KeyError:", exc)


def demo_fixed_read() -> None:
    csv_text = "id;value\n1;10\n2;20\n3;30\n"
    df = pd.read_csv(StringIO(csv_text), sep=";")
    print("=== Fixed read ===")
    print(df.head())
    print(df.dtypes)
    print("mean(value):", df["value"].mean())


def test_empty_row() -> None:
    csv_text_2 = "id;value\n1;10\n\n3;30\n"
    df = pd.read_csv(StringIO(csv_text_2), sep=";")
    print("=== Test 1: empty row ===")
    print("shape:", df.shape)
    print(df)


def test_missing_value() -> None:
    csv_text_3 = "id;value\n1;10\n2;\n3;30\n"
    df = pd.read_csv(StringIO(csv_text_3), sep=";")
    print("=== Test 2: missing value ===")
    print(df.dtypes)
    print("mean(skipna):", df["value"].mean())
    print(df)


if __name__ == "__main__":
    demo_broken_read()
    demo_fixed_read()
    test_empty_row()
    test_missing_value()
