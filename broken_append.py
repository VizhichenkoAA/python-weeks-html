"""Неделя 6, часть 0: append без идемпотентности и исправление."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

OUT = Path("out_append_demo.csv")


def broken_append() -> None:
    df = pd.DataFrame({"id": [1, 2], "v": [10, 20]})
    # BUG: при каждом запуске дописываем в один файл
    df.to_csv(OUT, mode="a", header=not OUT.exists(), index=False)
    rows = len(pd.read_csv(OUT))
    print(f"[BROKEN] written append -> {OUT} rows={rows}")


def fixed_replace() -> None:
    df = pd.DataFrame({"id": [1, 2], "v": [10, 20]})
    df.to_csv(OUT, mode="w", header=True, index=False)
    rows = len(pd.read_csv(OUT))
    print(f"[FIX replace] -> {OUT} rows={rows}")


def fixed_dedup() -> None:
    df = pd.DataFrame({"id": [1, 2], "v": [10, 20]})
    if OUT.exists():
        old = pd.read_csv(OUT)
        merged = pd.concat([old, df], ignore_index=True)
        merged = merged.drop_duplicates(subset=["id"], keep="last")
    else:
        merged = df
    merged.to_csv(OUT, index=False)
    rows = len(merged)
    print(f"[FIX dedup] -> {OUT} rows={rows}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        choices=["broken", "replace", "dedup", "demo"],
        help="broken=append bug; replace/dedup=fixed strategies; demo=run broken twice then fix",
    )
    args = parser.parse_args()
    if args.mode == "broken":
        broken_append()
    elif args.mode == "replace":
        fixed_replace()
    elif args.mode == "dedup":
        fixed_dedup()
    elif args.mode == "demo":
        if OUT.exists():
            OUT.unlink()
        broken_append()
        broken_append()
        print("[DEMO] after 2x broken append rows=", len(pd.read_csv(OUT)))
        fixed_replace()
        fixed_replace()
        print("[DEMO] after 2x replace rows=", len(pd.read_csv(OUT)))


if __name__ == "__main__":
    main()
