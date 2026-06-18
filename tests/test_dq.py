from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from sem2_de.dq import (
    check_non_empty,
    check_non_negative,
    check_not_null,
    check_unique_key,
    demo_break_check,
)


def test_check_not_null_pass():
    df = pd.DataFrame({"ts": pd.to_datetime(["2025-01-01"]), "city_id": ["RU_NSK"]})
    r = check_not_null(df, ["ts", "city_id"], "normalized")
    assert r.status == "PASS"


def test_check_not_null_fail():
    df = pd.DataFrame({"ts": [None], "city_id": ["RU_NSK"]})
    r = check_not_null(df, ["ts", "city_id"], "normalized")
    assert r.status == "FAIL"


def test_check_unique_key_boundary_single_row():
    df = pd.DataFrame({"city_id": ["RU_NSK"], "date": ["2025-01-01"]})
    r = check_unique_key(df, ["city_id", "date"], "mart")
    assert r.status == "PASS"


def test_check_non_negative_fail():
    df = pd.DataFrame({"P_sum": [-0.1, 1.0]})
    r = check_non_negative(df, "P_sum", "mart")
    assert r.status == "FAIL"


def test_demo_break_detects_issues():
    results = demo_break_check()
    assert any(r.status == "FAIL" for r in results)
