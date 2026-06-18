from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from sem2_de.config import database_url, load_config, mart_dir, mart_table_name, project_root
from sem2_de.dq import run_dq, summarize


def _mart_metrics() -> dict:
    files = sorted(mart_dir().glob("mart_daily_*.csv"))
    if not files:
        raise FileNotFoundError("No mart file for LLM context")
    df = pd.read_csv(files[-1], parse_dates=["date"])
    return {
        "rows": len(df),
        "period_min": str(df["date"].min().date()),
        "period_max": str(df["date"].max().date()),
        "t_mean_avg": round(float(df["T_mean"].mean()), 2),
        "p_sum_total": round(float(df["P_sum"].sum()), 2),
        "wind_max_peak": round(float(df["wind_max"].max()), 2),
        "rainy_hours_total": int(df["rainy_hours"].sum()),
        "top_wind_days": df.nsmallest(3, "wind_rank")[["date", "wind_max"]].to_dict("records"),
    }


def build_context(cfg: dict | None = None) -> str:
    cfg = cfg or load_config()
    metrics = _mart_metrics()
    dq_path = project_root() / "data" / "dq_report.json"
    dq_status = "UNKNOWN"
    if dq_path.exists():
        summary = json.loads(dq_path.read_text(encoding="utf-8")).get("summary", {})
        if summary.get("FAIL", 0) > 0:
            dq_status = "FAIL"
        elif summary.get("WARNING", 0) > 0:
            dq_status = "WARNING"
        else:
            dq_status = "PASS"

    lines = [
        f"Dataset: mart_variant_03 variant={cfg['variant_id']} source=Open-Meteo {cfg['entity']['city_name']}",
        f"Grain: 1 row = 1 day x city_id",
        f"Period: {metrics['period_min']} .. {metrics['period_max']} rows={metrics['rows']}",
        f"T_mean_avg={metrics['t_mean_avg']} C",
        f"P_sum_total={metrics['p_sum_total']} mm",
        f"wind_max_peak={metrics['wind_max_peak']} km/h",
        f"rainy_hours_total={metrics['rainy_hours_total']}",
        f"Quality: dq {dq_status}",
        "Constraints: do not invent numbers; use only metrics above.",
    ]
    return "\n".join(lines)


def _template_summary(context: str, metrics: dict) -> str:
    top = metrics["top_wind_days"]
    top_lines = "\n".join(
        f"- {row['date']}: wind_max={row['wind_max']} km/h" for row in top
    )
    return f"""# LLM Summary — variant 03 (template mode)

> Generated without external API. All numbers copied from computed context.

## Context
```
{context}
```

## Interpretation (rule-based)
- Средняя дневная температура за период: **{metrics['t_mean_avg']} °C**.
- Суммарные осадки: **{metrics['p_sum_total']} мм** за {metrics['rows']} дней.
- Пик ветра: **{metrics['wind_max_peak']} км/ч**.
- Дождливых часов (сумма по дням): **{metrics['rainy_hours_total']}**.

## Top wind days
{top_lines}

## Risks / next checks
- Сверить единицы ветра (км/ч) с Data Contract.
- При расширении периода пересчитать DQ и обновить watermark.
"""


def _call_openai(prompt: str) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    if not api_key:
        return None
    try:
        import urllib.request

        body = json.dumps(
            {
                "model": os.getenv("LLM_MODEL", "gpt-4o-mini"),
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a data analyst. Do not invent numbers.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]
    except Exception as exc:
        print(f"[WARN] LLM API call failed: {exc}")
        return None


def verify_numbers(summary: str, metrics: dict) -> list[str]:
    """Ensure key metrics appear in summary (anti-hallucination check)."""
    issues = []
    for key in ("t_mean_avg", "p_sum_total", "wind_max_peak"):
        val = str(metrics[key])
        if val not in summary and val.rstrip("0").rstrip(".") not in summary:
            issues.append(f"missing verified metric {key}={val}")
    return issues


def run_llm_summary() -> Path:
    cfg = load_config()
    metrics = _mart_metrics()
    context = build_context(cfg)
    prompt = (
        "Summarize the weather mart using ONLY the metrics below. "
        "Do not invent numbers. If uncertain, say uncertain.\n\n"
        + context
    )

    llm_text = _call_openai(prompt)
    if llm_text:
        summary = f"# LLM Summary — variant 03\n\n## Context\n```\n{context}\n```\n\n## LLM response\n{llm_text}\n"
        mode = "api"
    else:
        summary = _template_summary(context, metrics)
        mode = "template"

    issues = verify_numbers(summary, metrics)
    if issues:
        summary += "\n\n## Verification WARN\n" + "\n".join(f"- {i}" for i in issues)
    else:
        summary += "\n\n## Verification\n- PASS: key metrics found in summary text.\n"

    out_dir = project_root() / "docs" / "llm"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "summary.md"
    out_path.write_text(summary, encoding="utf-8")
    print(f"[OK] llm summary mode={mode} -> {out_path}")
    return out_path


if __name__ == "__main__":
    run_llm_summary()
