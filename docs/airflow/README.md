# Airflow — недели 11–12

## Запуск

```bat
scripts\run_airflow.bat
```

UI: http://localhost:8080 — `airflow` / `airflow`

## DAG-файлы

| Файл | Назначение |
|---|---|
| `airflow/dags/broken_dag.py` | Part 0 week 11 — сломанный start_date |
| `airflow/dags/demo_fixed_dag.py` | Исправленный demo DAG |
| `airflow/dags/etl_variant_03.py` | Основной ETL: extract → transform → dq → load |

Порядок week 11 (`load >> dq`): `set TP_DQ_AFTER_LOAD=1` в env контейнера.

## Период (week 12)

DAG передаёт `{{ ds }}` в extract/load для дневного интервала.  
Load: `delete period + insert` — retry-safe.

Скриншоты UI: положите в `docs/airflow/` (graph view, successful run, task logs).
