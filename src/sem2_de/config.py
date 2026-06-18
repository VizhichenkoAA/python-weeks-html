from __future__ import annotations

from pathlib import Path

import yaml


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_config(path: Path | None = None) -> dict:
    cfg_path = path or project_root() / "configs" / "variant_03.yml"
    with cfg_path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def raw_dir() -> Path:
    return project_root() / "data" / "raw" / "variant_03"


def normalized_dir() -> Path:
    return project_root() / "data" / "normalized" / "variant_03"


def mart_dir() -> Path:
    return project_root() / "data" / "mart" / "variant_03"


def reference_dir() -> Path:
    return project_root() / "reference"
