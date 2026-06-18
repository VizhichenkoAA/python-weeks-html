from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import yaml
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_config(path: Path | None = None) -> dict:
    cfg_path = path or project_root() / "configs" / "variant_03.yml"
    with cfg_path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_env() -> None:
    load_dotenv(project_root() / ".env")


def database_url() -> str:
    load_env()
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL не задан. Скопируйте .env.example в .env и запустите Postgres."
        )
    return url


def mart_table_name(cfg: dict | None = None) -> str:
    cfg = cfg or load_config()
    return cfg.get("postgres", {}).get("table", "mart_variant_03")


def raw_dir() -> Path:
    return project_root() / "data" / "raw" / "variant_03"


def normalized_dir() -> Path:
    return project_root() / "data" / "normalized" / "variant_03"


def mart_dir() -> Path:
    return project_root() / "data" / "mart" / "variant_03"


def reference_dir() -> Path:
    return project_root() / "reference"
