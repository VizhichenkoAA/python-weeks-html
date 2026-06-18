"""Generate week13 ML artifacts (anomaly detection on mart)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sem2_de.config import mart_dir, project_root

ML_DIR = project_root() / "docs" / "ml"


def zscore_anomalies(series: pd.Series, threshold: float = 2.0) -> pd.Series:
    mu = series.mean()
    sigma = series.std(ddof=0)
    if sigma == 0:
        return pd.Series(False, index=series.index)
    z = (series - mu) / sigma
    return z.abs() > threshold


def main() -> None:
    files = sorted(mart_dir().glob("mart_daily_*.csv"))
    df = pd.read_csv(files[-1], parse_dates=["date"]).sort_values("date")
    df["is_anomaly"] = zscore_anomalies(df["T_mean"], threshold=1.5)

    ML_DIR.mkdir(parents=True, exist_ok=True)
    anomalies = df[df["is_anomaly"]].copy()
    anomalies.to_csv(ML_DIR / "anomalies_top.csv", index=False)

    plt.figure(figsize=(9, 4))
    plt.plot(df["date"], df["T_mean"], marker="o", label="T_mean")
    if not anomalies.empty:
        plt.scatter(
            anomalies["date"],
            anomalies["T_mean"],
            color="red",
            s=80,
            label="anomaly (|z|>1.5)",
            zorder=5,
        )
    plt.title("Аномалии T_mean (Z-score)")
    plt.xlabel("Дата")
    plt.ylabel("T_mean, °C")
    plt.legend()
    plt.tight_layout()
    plt.savefig(ML_DIR / "metrics.png", dpi=120)
    plt.close()

    summary = f"""# Week 13 — anomaly summary (variant 03)

## Method
- Z-score on daily `T_mean`, threshold |z| > 1.5

## Results
- Days in mart: {len(df)}
- Anomalies flagged: {len(anomalies)}

## Interpretation
Аномальные дни — кандидаты на ручную проверку (погодное событие vs ошибка данных).
Модель не использовалась; эвристика достаточна для учебного объёма данных.

## Artifacts
- `metrics.png` — график с выделением аномалий
- `anomalies_top.csv` — таблица подозрительных дней
"""
    (ML_DIR / "week13_summary.md").write_text(summary, encoding="utf-8")
    print(f"[OK] week13 artifacts -> {ML_DIR}")


if __name__ == "__main__":
    main()
