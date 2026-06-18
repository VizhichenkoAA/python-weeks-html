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


def load_mart_to_postgres(
    mart_file: Path | None = None,
    cfg: dict | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    mode: str = "replace",
) -> int:
    cfg = cfg or load_config()
    mart_file = mart_file or latest_mart_file()
    table = mart_table_name(cfg)

    df = pd.read_csv(mart_file, parse_dates=["date"])
    print(f"[INFO] mart file: {mart_file}")
    print(f"[INFO] shape: {df.shape}")

    if start_date and end_date:
        mask = (df["date"] >= pd.to_datetime(start_date)) & (
            df["date"] <= pd.to_datetime(end_date)
        )
        df = df.loc[mask].copy()
        print(f"[INFO] period filter {start_date}..{end_date} rows={len(df)}")

    engine = create_engine(database_url())
    with engine.begin() as conn:
        if mode == "replace":
            df.to_sql(table, conn, if_exists="replace", index=False, method="multi")
        elif mode == "period":
            if start_date and end_date:
                conn.execute(
                    text(
                        f"DELETE FROM {table} WHERE date >= :s AND date <= :e"
                    ),
                    {"s": start_date, "e": end_date},
                )
                print(f"[INFO] deleted period {start_date}..{end_date} from {table}")
            df.to_sql(table, conn, if_exists="append", index=False, method="multi")
        else:
            raise ValueError(f"Unknown load mode: {mode}")
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()

    print(f"[OK] loaded table={table} rows_in_table={count} inserted={len(df)} mode={mode}")
    return int(count)


def run_load(
    mart_file: Path | None = None,
    cfg: dict | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    mode: str = "replace",
) -> int:
    return load_mart_to_postgres(mart_file, cfg, start_date, end_date, mode)


if __name__ == "__main__":
    run_load()
