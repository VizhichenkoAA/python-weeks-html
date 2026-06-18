from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sem2_de.config import load_config, project_root


def state_path() -> Path:
    return project_root() / "data" / "state.json"


def default_state(cfg: dict | None = None) -> dict[str, Any]:
    cfg = cfg or load_config()
    return {
        "variant_id": cfg["variant_id"],
        "source_type": cfg.get("source_type", "open_meteo"),
        "watermark": None,
        "last_success_utc": None,
    }


def load_state(cfg: dict | None = None) -> dict[str, Any]:
    path = state_path()
    if not path.exists():
        return default_state(cfg)
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def save_state(state: dict[str, Any]) -> Path:
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)
    return path


def touch_success(state: dict[str, Any], watermark: str | None) -> dict[str, Any]:
    state["watermark"] = watermark
    state["last_success_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    save_state(state)
    return state
