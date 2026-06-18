"""Generate week7 visualization figures from mart CSV."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from sem2_de.config import mart_dir

FIG_DIR = Path(__file__).resolve().parents[1] / "docs" / "figures"


def main() -> None:
    files = sorted(mart_dir().glob("mart_daily_*.csv"))
    if not files:
        raise FileNotFoundError("Run pipeline first to create mart CSV")
    df = pd.read_csv(files[-1], parse_dates=["date"])
    df = df.sort_values("date")
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Time series — temperature
    plt.figure(figsize=(9, 4))
    plt.plot(df["date"], df["T_mean"], marker="o", color="#2f7dff")
    plt.title("Средняя температура по дням — Новосибирск")
    plt.xlabel("Дата")
    plt.ylabel("T_mean, °C")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "week7_timeseries.png", dpi=120)
    plt.close()

    # 2) Distribution — wind_max
    plt.figure(figsize=(7, 4))
    plt.hist(df["wind_max"], bins=8, color="#59a8ff", edgecolor="white")
    plt.title("Распределение максимальной скорости ветра")
    plt.xlabel("wind_max, км/ч")
    plt.ylabel("Число дней")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "week7_distribution.png", dpi=120)
    plt.close()

    # 3) Ranking — top days by wind
    top = df.nsmallest(5, "wind_rank").sort_values("wind_max", ascending=True)
    plt.figure(figsize=(8, 4))
    plt.barh(top["date"].dt.strftime("%Y-%m-%d"), top["wind_max"], color="#26c281")
    plt.title("Топ дней по скорости ветра")
    plt.xlabel("wind_max, км/ч")
    plt.ylabel("Дата")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "week7_ranking.png", dpi=120)
    plt.close()

    print(f"[OK] saved figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
