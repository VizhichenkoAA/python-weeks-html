from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from sem2_de.config import load_config, mart_dir, reference_dir


def latest_normalized_file(norm_path: Path | None = None) -> Path:
    base = norm_path or (Path(__file__).resolve().parents[2] / "data" / "normalized" / "variant_03")
    files = sorted(base.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No normalized CSV in {base}")
    return files[-1]


def build_daily_mart(df: pd.DataFrame, cities: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["ts"] = pd.to_datetime(work["ts"])
    work["date"] = work["ts"].dt.date

    daily = (
        work.groupby(["city_id", "date"], as_index=False)
        .agg(
            T_mean=("temperature_2m", "mean"),
            P_sum=("precipitation", "sum"),
            wind_max=("wind_speed_10m", "max"),
            rainy_hours=("precipitation", lambda s: int((s.fillna(0) > 0).sum())),
            obs_hours=("ts", "count"),
        )
    )

    # Join reference cities (many-to-one)
    cities_ref = cities.drop_duplicates(subset=["city_id"], keep="first")
    mart = daily.merge(
        cities_ref,
        on="city_id",
        how="left",
        validate="many_to_one",
    )

    # KPI: топ-5 дней по ветру — ранг внутри city
    mart["wind_rank"] = mart.groupby("city_id")["wind_max"].rank(method="dense", ascending=False)
    mart = mart.sort_values(["date"]).reset_index(drop=True)
    return mart


def run_mart(normalized_file: Path | None = None, cfg: dict | None = None) -> Path:
    cfg = cfg or load_config()
    normalized_file = normalized_file or latest_normalized_file()
    cities_path = reference_dir() / "cities.csv"
    if not cities_path.exists():
        raise FileNotFoundError(f"Missing reference: {cities_path}")

    df = pd.read_csv(normalized_file, parse_dates=["ts"])
    cities = pd.read_csv(cities_path)
    mart = build_daily_mart(df, cities)

    out_dir = mart_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_path = out_dir / f"mart_daily_{stamp}.csv"
    mart.to_csv(out_path, index=False)

    top5 = mart.nsmallest(5, "wind_rank")[["date", "wind_max", "city_name"]]
    print(f"[OK] saved mart: {out_path} rows={len(mart)}")
    print("[INFO] top-5 wind days:")
    print(top5.to_string(index=False))
    return out_path


if __name__ == "__main__":
    run_mart()
