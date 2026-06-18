"""Week 11, part 0: broken DAG (start_date in future / catchup issues)."""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator

# BUG: start_date в будущем — DAG-run не появляется как ожидалось
with DAG(
    dag_id="demo_broken",
    start_date=datetime.now() + timedelta(days=1),
    schedule="@daily",
    catchup=False,
    tags=["tp", "demo", "broken"],
) as dag:
    EmptyOperator(task_id="noop")
