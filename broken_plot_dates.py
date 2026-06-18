"""Неделя 7, часть 0: даты как строки ломают временной график."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

FIG_DIR = Path("docs/figures")


def broken_plot(out: Path) -> None:
    df = pd.DataFrame(
        {
            "date": ["2025-01-10", "2025-01-2", "2025-01-3"],
            "value": [10, 2, 3],
        }
    )
    df = df.sort_values("date")
    plt.figure(figsize=(7, 4))
    plt.plot(df["date"], df["value"], marker="o")
    plt.xticks(rotation=45)
    plt.title("BUG: string sort on date axis")
    plt.xlabel("date (string)")
    plt.ylabel("value")
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"[BROKEN] saved {out} order={list(df['date'])}")


def fixed_plot(out: Path) -> None:
    df = pd.DataFrame(
        {
            "date": ["2025-01-10", "2025-01-2", "2025-01-3"],
            "value": [10, 2, 3],
        }
    )
    df["date"] = pd.to_datetime(df["date"], format="mixed")
    df = df.sort_values("date")
    plt.figure(figsize=(7, 4))
    plt.plot(df["date"], df["value"], marker="o")
    plt.xticks(rotation=45)
    plt.title("FIX: datetime sort")
    plt.xlabel("date")
    plt.ylabel("value")
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"[FIX] saved {out} order={list(df['date'].dt.strftime('%Y-%m-%d'))}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["broken", "fixed", "both"], default="both", nargs="?")
    args = parser.parse_args()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    if args.mode in ("broken", "both"):
        broken_plot(FIG_DIR / "week7_part0_broken.png")
    if args.mode in ("fixed", "both"):
        fixed_plot(FIG_DIR / "week7_part0_fixed.png")


if __name__ == "__main__":
    main()
