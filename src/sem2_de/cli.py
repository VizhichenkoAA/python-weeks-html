from __future__ import annotations

import argparse
from pathlib import Path

from sem2_de.extract import run_extract
from sem2_de.load import run_load
from sem2_de.mart import run_mart
from sem2_de.normalize import run_normalize


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
    sub.add_parser("pipeline", help="extract + normalize + mart")

    args = parser.parse_args()
    if args.command == "extract":
        run_extract()
    elif args.command == "normalize":
        run_normalize(args.raw)
    elif args.command == "mart":
        run_mart(args.normalized)
    elif args.command == "load":
        run_load(args.mart)
    elif args.command == "pipeline":
        raw = run_extract()
        norm = run_normalize(raw)
        run_mart(norm)


if __name__ == "__main__":
    main()
