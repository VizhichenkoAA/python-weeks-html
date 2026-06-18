from pathlib import Path

import pandas as pd

from sem2_de.normalize import normalize_payload


def test_normalize_grain_and_columns():
    payload = {
        "hourly": {
            "time": ["2025-01-01T00:00", "2025-01-01T01:00"],
            "temperature_2m": [1.0, 2.0],
            "relative_humidity_2m": [50.0, 55.0],
            "precipitation": [0.0, 0.1],
            "wind_speed_10m": [10.0, 12.0],
        }
    }
    df = normalize_payload(payload, "RU_NSK")
    assert len(df) == 2
    assert list(df.columns) == [
        "ts",
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
        "city_id",
    ]
