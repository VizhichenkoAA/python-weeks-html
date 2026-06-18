from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import requests

from sem2_de.config import load_config, raw_dir


def build_url(cfg: dict) -> str:
    api = cfg["api"]
    entity = cfg["entity"]
    extract = cfg["extract"]
    hourly = ",".join(api["params"]["hourly"])
    params = {
        "latitude": entity["latitude"],
        "longitude": entity["longitude"],
        "timezone": entity["timezone"],
        "start_date": extract["start_date"],
        "end_date": extract["end_date"],
        "hourly": hourly,
    }
    return f"{api['base_url']}?{urlencode(params)}"


def fetch_open_meteo(cfg: dict | None = None) -> dict[str, Any]:
    cfg = cfg or load_config()
    url = build_url(cfg)
    timeout = cfg["api"].get("timeout_sec", 60)
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    payload["_meta"] = {
        "fetched_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "request_url": url,
        "variant_id": cfg["variant_id"],
        "city_id": cfg["entity"]["city_id"],
    }
    return payload


def save_raw(payload: dict[str, Any], out_dir: Path | None = None) -> Path:
    out_dir = out_dir or raw_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = out_dir / f"open_meteo_{stamp}.json"
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    return path


def run_extract(cfg: dict | None = None) -> Path:
    cfg = cfg or load_config()
    payload = fetch_open_meteo(cfg)
    path = save_raw(payload)
    print(f"[OK] saved raw: {path}")
    return path


if __name__ == "__main__":
    run_extract()
