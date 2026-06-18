"""Create BI placeholder screenshots for week 10 (matplotlib mockups)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from sem2_de.config import mart_dir, project_root

BI_DIR = project_root() / "docs" / "bi"


def main() -> None:
    files = sorted(mart_dir().glob("mart_daily_*.csv"))
    df = pd.read_csv(files[-1], parse_dates=["date"]).sort_values("date")
    BI_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    fig.suptitle("TP v03 — Metabase-style dashboard (mockup)")

    axes[0, 0].plot(df["date"], df["T_mean"], marker="o")
    axes[0, 0].set_title("T_mean по дням")
    axes[0, 0].set_ylabel("°C")

    axes[0, 1].bar(df["date"].dt.strftime("%m-%d"), df["P_sum"], color="#59a8ff")
    axes[0, 1].set_title("Осадки P_sum")
    axes[0, 1].set_ylabel("мм")

    axes[1, 0].hist(df["wind_max"], bins=6, color="#26c281")
    axes[1, 0].set_title("Распределение wind_max")

    top = df.nsmallest(5, "wind_rank").sort_values("wind_max")
    axes[1, 1].barh(top["date"].dt.strftime("%Y-%m-%d"), top["wind_max"])
    axes[1, 1].set_title("Топ дней по ветру")

    plt.tight_layout()
    fig.savefig(BI_DIR / "dashboard_overview.png", dpi=120)
    plt.close()

    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["T_mean"], marker="o")
    plt.title("chart_timeseries — T_mean")
    plt.xlabel("date")
    plt.ylabel("°C")
    plt.tight_layout()
    plt.savefig(BI_DIR / "chart_timeseries.png", dpi=120)
    plt.close()

    top = df.nsmallest(5, "wind_rank").sort_values("wind_max", ascending=True)
    plt.figure(figsize=(8, 4))
    plt.barh(top["date"].dt.strftime("%Y-%m-%d"), top["wind_max"])
    plt.title("chart_ranking — wind_max")
    plt.xlabel("км/ч")
    plt.tight_layout()
    plt.savefig(BI_DIR / "chart_ranking.png", dpi=120)
    plt.close()

    readme = """# BI — неделя 10 (вариант 03)

## Запуск Metabase

```bat
scripts\\run_postgres.bat
docker compose up -d metabase
```

- Metabase UI: http://localhost:3000
- Postgres из контейнера Metabase: host `postgres`, port `5432`, db `tp_variant_03`, user `tp_pass`
- С хоста Windows: `localhost:5433`

## Дашборд (минимум 3 визуализации)

1. Временной ряд `T_mean`
2. Bar `P_sum` или ranking по `wind_max`
3. KPI card: `COUNT(*)`, `AVG(T_mean)`, `SUM(P_sum)`

Скриншоты для сдачи: `dashboard_overview.png`, `chart_timeseries.png`, `chart_ranking.png`.
"""
    (BI_DIR / "README.md").write_text(readme, encoding="utf-8")
    print(f"[OK] BI artifacts -> {BI_DIR}")


if __name__ == "__main__":
    main()
