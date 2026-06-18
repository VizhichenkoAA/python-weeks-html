from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Literal

import pandas as pd

from sem2_de.config import load_config, mart_dir, normalized_dir, project_root
from sem2_de.mart import build_daily_mart, latest_normalized_file
from sem2_de.normalize import NORMALIZED_COLUMNS, normalize_payload

Status = Literal["PASS", "WARNING", "FAIL"]


@dataclass
class CheckResult:
    name: str
    layer: str
    status: Status
    reason: str
    details: dict[str, Any]


def _read_normalized(path: Path | None = None) -> pd.DataFrame:
    path = path or latest_normalized_file()
    return pd.read_csv(path, parse_dates=["ts"])


def _read_mart(path: Path | None = None) -> pd.DataFrame:
    base = mart_dir()
    files = sorted(base.glob("mart_daily_*.csv"))
    if path is None:
        if not files:
            raise FileNotFoundError(f"No mart CSV in {base}")
        path = files[-1]
    return pd.read_csv(path, parse_dates=["date"])


def check_non_empty(df: pd.DataFrame, layer: str) -> CheckResult:
    ok = len(df) > 0
    return CheckResult(
        "non_empty",
        layer,
        "PASS" if ok else "FAIL",
        "table has rows" if ok else "table is empty",
        {"rows": len(df)},
    )


def check_not_null(df: pd.DataFrame, cols: list[str], layer: str) -> CheckResult:
    bad = {c: int(df[c].isna().sum()) for c in cols if c in df.columns}
    ok = all(v == 0 for v in bad.values())
    return CheckResult(
        "not_null_critical",
        layer,
        "PASS" if ok else "FAIL",
        "no nulls in critical columns" if ok else "nulls found",
        {"null_counts": bad},
    )


def check_unique_key(df: pd.DataFrame, keys: list[str], layer: str) -> CheckResult:
    dup = int(df.duplicated(subset=keys, keep=False).sum())
    ok = dup == 0
    return CheckResult(
        "unique_business_key",
        layer,
        "PASS" if ok else "FAIL",
        "unique key" if ok else "duplicate keys",
        {"keys": keys, "duplicate_rows": dup},
    )


def check_numeric_range(
    df: pd.DataFrame,
    col: str,
    low: float,
    high: float,
    layer: str,
    severity: Status = "FAIL",
) -> CheckResult:
    if col not in df.columns:
        return CheckResult("range_" + col, layer, "FAIL", f"missing column {col}", {})
    series = pd.to_numeric(df[col], errors="coerce")
    bad = int(((series < low) | (series > high)).sum())
    ok = bad == 0
    return CheckResult(
        f"range_{col}",
        layer,
        "PASS" if ok else severity,
        f"{col} in [{low},{high}]" if ok else f"{bad} rows out of range",
        {"column": col, "bad_rows": bad, "low": low, "high": high},
    )


def check_non_negative(df: pd.DataFrame, col: str, layer: str) -> CheckResult:
    if col not in df.columns:
        return CheckResult(f"non_negative_{col}", layer, "FAIL", f"missing column {col}", {})
    bad = int((pd.to_numeric(df[col], errors="coerce") < 0).sum())
    ok = bad == 0
    return CheckResult(
        f"non_negative_{col}",
        layer,
        "PASS" if ok else "FAIL",
        "no negative values" if ok else "negative values found",
        {"column": col, "bad_rows": bad},
    )


def check_freshness(raw_meta_fetched: str | None, max_age_hours: int = 720) -> CheckResult:
    if not raw_meta_fetched:
        return CheckResult(
            "freshness",
            "raw",
            "WARNING",
            "no fetched_at_utc in raw meta",
            {},
        )
    fetched = datetime.fromisoformat(raw_meta_fetched.replace("Z", "+00:00"))
    age_h = (datetime.now(fetched.tzinfo) - fetched).total_seconds() / 3600
    ok = age_h <= max_age_hours
    return CheckResult(
        "freshness",
        "raw",
        "PASS" if ok else "WARNING",
        "raw is fresh enough" if ok else "raw may be stale",
        {"age_hours": round(age_h, 2), "max_age_hours": max_age_hours},
    )


def run_checks(
    normalized_file: Path | None = None,
    mart_file: Path | None = None,
    cfg: dict | None = None,
) -> list[CheckResult]:
    cfg = cfg or load_config()
    results: list[CheckResult] = []

    norm = _read_normalized(normalized_file)
    mart = _read_mart(mart_file)

    results.append(check_non_empty(norm, "normalized"))
    results.append(check_not_null(norm, ["ts", "city_id"], "normalized"))
    results.append(check_unique_key(norm, ["city_id", "ts"], "normalized"))
    results.append(check_numeric_range(norm, "temperature_2m", -80, 60, "normalized"))
    results.append(check_numeric_range(norm, "relative_humidity_2m", 0, 100, "normalized", "WARNING"))
    results.append(check_non_negative(norm, "precipitation", "normalized"))

    results.append(check_non_empty(mart, "mart"))
    results.append(check_not_null(mart, ["city_id", "date"], "mart"))
    results.append(check_unique_key(mart, ["city_id", "date"], "mart"))
    results.append(check_non_negative(mart, "P_sum", "mart"))
    results.append(
        check_numeric_range(mart, "obs_hours", 1, 24, "mart", "WARNING")
    )

    return results


def summarize(results: list[CheckResult]) -> dict[str, int]:
    out = {"PASS": 0, "WARNING": 0, "FAIL": 0}
    for r in results:
        out[r.status] += 1
    return out


def save_report(results: list[CheckResult], path: Path | None = None) -> Path:
    path = path or project_root() / "data" / "dq_report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "summary": summarize(results),
        "checks": [asdict(r) for r in results],
    }
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    return path


def run_dq(
    normalized_file: Path | None = None,
    mart_file: Path | None = None,
    cfg: dict | None = None,
    fail_on_error: bool = True,
) -> dict[str, Any]:
    results = run_checks(normalized_file, mart_file, cfg)
    summary = summarize(results)
    report_path = save_report(results)
    print(f"[INFO] dq_report: {report_path}")
    print(f"[INFO] dq checks: PASS={summary['PASS']} WARNING={summary['WARNING']} FAIL={summary['FAIL']}")
    for r in results:
        if r.status != "PASS":
            print(f"  [{r.status}] {r.layer}.{r.name}: {r.reason}")
    if fail_on_error and summary["FAIL"] > 0:
        raise RuntimeError(f"DQ FAIL: {summary['FAIL']} critical checks failed")
    return {"summary": summary, "report_path": str(report_path), "results": results}


def demo_break_check() -> list[CheckResult]:
    """Искусственно сломанные данные для демонстрации FAIL."""
    df = pd.DataFrame(
        {
            "city_id": ["RU_NSK", "RU_NSK"],
            "date": [date(2025, 1, 1), date(2025, 1, 1)],
            "P_sum": [-1.0, 2.0],
        }
    )
    return [
        check_unique_key(df, ["city_id", "date"], "mart"),
        check_non_negative(df, "P_sum", "mart"),
    ]


if __name__ == "__main__":
    run_dq()
