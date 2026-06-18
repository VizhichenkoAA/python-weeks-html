"""Fixed demo DAG (week 11 part 0)."""

from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="demo_fixed",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["tp", "demo", "fixed"],
) as dag:
    EmptyOperator(task_id="noop")
