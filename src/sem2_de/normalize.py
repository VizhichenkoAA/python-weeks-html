from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from sem2_de.config import load_config, normalized_dir


NORMALIZED_COLUMNS = [
    "ts",
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
    "city_id",
]


def latest_raw_file(raw_path: Path | None = None) -> Path:
    base = raw_path or (Path(__file__).resolve().parents[2] / "data" / "raw" / "variant_03")
    files = sorted(base.glob("open_meteo_*.json"))
    if not files:
        raise FileNotFoundError(f"No raw JSON in {base}")
    return files[-1]


def normalize_payload(payload: dict, city_id: str) -> pd.DataFrame:
    hourly = payload["hourly"]
    df = pd.DataFrame(
        {
            "ts": pd.to_datetime(hourly["time"]),
            "temperature_2m": hourly["temperature_2m"],
            "relative_humidity_2m": hourly["relative_humidity_2m"],
            "precipitation": hourly["precipitation"],
            "wind_speed_10m": hourly["wind_speed_10m"],
            "city_id": city_id,
        }
    )

    # 1) Удаляем строки без timestamp
    df = df.dropna(subset=["ts"])

    # 2) Приводим числовые поля к float, некорректные -> NaN
    for col in ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3) DQ-фильтры из контракта
    df = df[df["temperature_2m"].between(-80, 60, inclusive="both") | df["temperature_2m"].isna()]
    df = df[df["relative_humidity_2m"].between(0, 100, inclusive="both") | df["relative_humidity_2m"].isna()]
    df = df[df["precipitation"].ge(0) | df["precipitation"].isna()]

    # 4) Дедупликация по (city_id, ts)
    df = df.sort_values("ts").drop_duplicates(subset=["city_id", "ts"], keep="last")

    return df[NORMALIZED_COLUMNS]


def normalize_file(raw_file: Path, cfg: dict | None = None) -> Path:
    cfg = cfg or load_config()
    city_id = cfg["entity"]["city_id"]
    with raw_file.open(encoding="utf-8") as fh:
        payload = json.load(fh)
    df = normalize_payload(payload, city_id)
    out_dir = normalized_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_path = out_dir / f"{stamp}.csv"
    df.to_csv(out_path, index=False)
    print(f"[OK] saved normalized: {out_path} rows={len(df)}")
    return out_path


def run_normalize(raw_file: Path | None = None, cfg: dict | None = None) -> Path:
    raw_file = raw_file or latest_raw_file()
    return normalize_file(raw_file, cfg)


if __name__ == "__main__":
    run_normalize()
