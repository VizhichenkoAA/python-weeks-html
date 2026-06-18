from __future__ import annotations

from pathlib import Path

from sem2_de.mart import run_mart
from sem2_de.normalize import run_normalize


def run_transform(
    raw_file: Path | None = None,
    cfg: dict | None = None,
    normalized_file: Path | None = None,
) -> tuple[Path, Path]:
    """Transform: raw JSON -> normalized CSV -> mart daily CSV."""
    norm = normalized_file or run_normalize(raw_file, cfg)
    mart = run_mart(norm, cfg)
    print(f"[OK] transform done: normalized={norm.name} mart={mart.name}")
    return norm, mart


if __name__ == "__main__":
    run_transform()
