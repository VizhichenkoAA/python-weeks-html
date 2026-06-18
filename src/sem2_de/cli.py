from __future__ import annotations

import argparse
from pathlib import Path

from sem2_de.dq import run_dq
from sem2_de.extract import run_extract
from sem2_de.load import run_load
from sem2_de.mart import run_mart
from sem2_de.normalize import run_normalize
from sem2_de.pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="TP variant 03 pipeline CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("extract", help="HTTP extract -> data/raw")
    p_norm = sub.add_parser("normalize", help="raw JSON -> normalized CSV")
    p_norm.add_argument("--raw", type=Path, default=None)
    p_mart = sub.add_parser("mart", help="normalized CSV -> mart daily")
    p_mart.add_argument("--normalized", type=Path, default=None)
    p_load = sub.add_parser("load", help="mart CSV -> Postgres")
    p_load.add_argument("--mart", type=Path, default=None)
    p_load.add_argument("--start", dest="start_date", default=None)
    p_load.add_argument("--end", dest="end_date", default=None)
    p_load.add_argument("--mode", choices=["replace", "period"], default="replace")
    sub.add_parser("dq", help="run DQ checks -> data/dq_report.json")
    p_pipe = sub.add_parser("pipeline", help="extract + normalize + mart (legacy)")
    p_pipe.add_argument("--with-load", action="store_true")
    p_full = sub.add_parser("run", help="full ETL pipeline (week6+)")
    p_full.add_argument("--config", type=Path, default=None)
    p_full.add_argument("--mode", choices=["full", "incremental"], default="full")
    p_full.add_argument("--start", dest="start_date", default=None)
    p_full.add_argument("--end", dest="end_date", default=None)
    p_full.add_argument("--skip-load", action="store_true")
    p_full.add_argument("--skip-dq", action="store_true")
    p_full.add_argument("--dq-after-load", action="store_true")

    args = parser.parse_args()
    if args.command == "extract":
        run_extract()
    elif args.command == "normalize":
        run_normalize(args.raw)
    elif args.command == "mart":
        run_mart(args.normalized)
    elif args.command == "load":
        run_load(args.mart, start_date=args.start_date, end_date=args.end_date, mode=args.mode)
    elif args.command == "dq":
        run_dq()
    elif args.command == "pipeline":
        raw = run_extract()
        norm = run_normalize(raw)
        run_mart(norm)
        if args.with_load:
            run_load()
    elif args.command == "run":
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
