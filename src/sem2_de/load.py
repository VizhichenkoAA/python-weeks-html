from __future__ import annotations

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from sem2_de.config import database_url, load_config, mart_dir, mart_table_name


def latest_mart_file(mart_path: Path | None = None) -> Path:
    base = mart_path or mart_dir()
    files = sorted(base.glob("mart_daily_*.csv"))
    if not files:
        raise FileNotFoundError(f"No mart CSV in {base}")
    return files[-1]


def load_mart_to_postgres(mart_file: Path | None = None, cfg: dict | None = None) -> int:
    cfg = cfg or load_config()
    mart_file = mart_file or latest_mart_file()
    table = mart_table_name(cfg)

    df = pd.read_csv(mart_file, parse_dates=["date"])
    print(f"[INFO] mart file: {mart_file}")
    print(f"[INFO] shape: {df.shape}")
    print(f"[INFO] columns: {list(df.columns)}")
    print(df.dtypes)

    engine = create_engine(database_url())
    with engine.begin() as conn:
        df.to_sql(table, conn, if_exists="replace", index=False, method="multi")
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()

    print(f"[OK] loaded table={table} rows={count}")
    return int(count)


def run_load(mart_file: Path | None = None, cfg: dict | None = None) -> int:
    return load_mart_to_postgres(mart_file, cfg)


if __name__ == "__main__":
    run_load()
