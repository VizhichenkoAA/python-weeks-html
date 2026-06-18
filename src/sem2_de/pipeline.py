from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path

from sem2_de.config import load_config
from sem2_de.dq import run_dq
from sem2_de.extract import run_extract
from sem2_de.load import run_load
from sem2_de.state import load_state, touch_success
from sem2_de.transform import run_transform

BUSINESS_KEY = ("city_id", "date")


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def _incremental_window(cfg: dict, state: dict) -> tuple[str, str]:
    extract = cfg["extract"]
    cfg_end = _parse_date(extract["end_date"])
    watermark = state.get("watermark")
    if watermark:
        start = _parse_date(watermark) + timedelta(days=1)
    else:
        start = _parse_date(extract["start_date"])
    if start > cfg_end:
        # уже обработали весь конфигурированный период — переигрываем последний день
        start = cfg_end
    end = min(start + timedelta(days=6), cfg_end)
    return start.isoformat(), end.isoformat()


def run_pipeline(
    mode: str = "full",
    config_path: Path | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    skip_load: bool = False,
    skip_dq: bool = False,
    dq_before_load: bool = True,
) -> dict:
    cfg = load_config(config_path)
    state = load_state(cfg)

    if mode == "full":
        sd = start_date or cfg["extract"]["start_date"]
        ed = end_date or cfg["extract"]["end_date"]
        load_mode = "replace"
    elif mode == "incremental":
        if start_date and end_date:
            sd, ed = start_date, end_date
        else:
            sd, ed = _incremental_window(cfg, state)
        load_mode = "period"
    else:
        raise ValueError(f"Unknown mode: {mode}")

    print(f"[PIPELINE] mode={mode} period={sd}..{ed} business_key={BUSINESS_KEY}")

    raw = run_extract(cfg, sd, ed)
    norm, mart = run_transform(raw, cfg)

    dq_summary = None
    if not skip_dq and dq_before_load:
        dq_summary = run_dq(norm, mart, cfg, fail_on_error=True)

    loaded_rows = 0
    if not skip_load:
        loaded_rows = run_load(mart, cfg, start_date=sd, end_date=ed, mode=load_mode)

    if not skip_dq and not dq_before_load:
        dq_summary = run_dq(norm, mart, cfg, fail_on_error=True)

    touch_success(state, ed)
    print(f"[OK] pipeline finished watermark={ed} loaded_rows={loaded_rows}")
    return {
        "mode": mode,
        "start_date": sd,
        "end_date": ed,
        "raw": str(raw),
        "mart": str(mart),
        "loaded_rows": loaded_rows,
        "dq": dq_summary["summary"] if dq_summary else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="TP variant 03 ETL pipeline")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--mode", choices=["full", "incremental"], default="full")
    parser.add_argument("--start", dest="start_date", default=None)
    parser.add_argument("--end", dest="end_date", default=None)
    parser.add_argument("--skip-load", action="store_true")
    parser.add_argument("--skip-dq", action="store_true")
    parser.add_argument(
        "--dq-after-load",
        action="store_true",
        help="week11 order: dq after load (default: dq before load, week12 gate)",
    )
    args = parser.parse_args()
    run_pipeline(
        mode=args.mode,
        config_path=args.config,
        start_date=args.start_date,
        end_date=args.end_date,
        skip_load=args.skip_load,
        skip_dq=args.skip_dq,
        dq_before_load=not args.dq_after_load,
    )


if __name__ == "__main__":
    main()
