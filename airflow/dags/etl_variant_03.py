"""Week 11–12: ETL DAG for variant 03.

Order week 12 (DQ gate): extract >> transform >> dq >> load
Set env TP_DQ_AFTER_LOAD=1 for week 11 order (load >> dq).
"""

from __future__ import annotations

import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT = os.environ.get("TP_PROJECT_DIR", "/opt/airflow/project")
PYTHON = os.environ.get("TP_PYTHON", "python")
DQ_AFTER = os.environ.get("TP_DQ_AFTER_LOAD", "0") == "1"

default_args = {
    "owner": "tp-v03",
    "retries": 1,
}

with DAG(
    dag_id="etl_variant_03",
    description="Open-Meteo Novosibirsk: extract -> transform -> dq -> load",
    start_date=datetime(2025, 1, 1),
    schedule="*/30 * * * *",
    catchup=False,
    max_active_runs=1,
    tags=["tp", "variant_03"],
    default_args=default_args,
) as dag:
    common = f"cd {PROJECT} && PYTHONPATH=src"

    extract = BashOperator(
        task_id="extract",
        bash_command=(
            f"{common} {PYTHON} -c \""
            "from sem2_de.extract import run_extract; "
            "run_extract(start_date='{{ ds }}', end_date='{{ ds }}')\""
        ),
    )

    transform = BashOperator(
        task_id="transform",
        bash_command=f"{common} {PYTHON} -m sem2_de.transform",
    )

    dq = BashOperator(
        task_id="dq",
        bash_command=f"{common} {PYTHON} -m sem2_de.dq",
    )

    load = BashOperator(
        task_id="load",
        bash_command=(
            f"{common} {PYTHON} -c \""
            "from sem2_de.load import run_load; "
            "run_load(start_date='{{ ds }}', end_date='{{ ds }}', mode='period')\""
        ),
    )

    if DQ_AFTER:
        extract >> transform >> load >> dq
    else:
        extract >> transform >> dq >> load
