# Implementation Plan — вариант 03

## 1. Краткое описание задачи
Архив погоды для Новосибирска из Open-Meteo: RAW → NORMALIZED → MART → Postgres → BI → DQ → Airflow → ML → LLM.

## 8. План-график (по неделям)

| Неделя | Что делаю | Артефакт |
|---|---|---|
| 1 | Conda, структура | `setup_env.bat`, `broken_env.py` |
| 2 | Extract | `extract.py`, `data/raw/` |
| 3 | Normalize + EDA | `normalize.py`, `week3_eda.ipynb` |
| 4 | Mart | `mart.py`, `data/mart/` |
| 5 | Postgres load | `load.py`, `docker-compose.yml`, `sql_checks.md` |
| 6 | Pipeline full/incremental | `pipeline.py`, `state.json`, `broken_append.py` |
| 7 | Визуализация | `week7_viz.ipynb`, `docs/figures/` |
| 8 | DQ | `dq.py`, `dq_report.json`, `tests/test_dq.py` |
| 9 | Governance | `Data_Contract.md`, `data_dictionary.md` |
| 10 | Docker BI | Metabase in compose, `docs/bi/` |
| 11 | Airflow DAG | `airflow/dags/etl_variant_03.py` |
| 12 | Period + DQ gate | period params, `dq >> load` |
| 13 | ML / anomalies | `week13_ml.ipynb`, `docs/ml/` |
| 14 | LLM summary | `llm_summary.py`, `docs/llm/summary.md` |

## 6. Инкрементальность и идемпотентность (week 6–12)

### Full mode
- Extract за весь период из конфига (`2025-01-01` … `2025-01-14`)
- Transform → normalized + mart (новые файлы с timestamp)
- Load: `if_exists=replace` в Postgres
- Повторный full: таблица пересоздаётся, дублей нет

### Incremental mode
- Watermark: `data/state.json` → поле `watermark` = последний успешно обработанный `end_date`
- Следующий запуск: `start = watermark + 1 day`, окно до 7 дней
- Load: **delete period + insert** по `(date)` — retry-safe
- Watermark обновляется только после успешного pipeline (включая load)

### Business key
`(city_id, date)` на mart — уникальность дня для города.

### State file
`data/state.json`: `variant_id`, `source_type`, `watermark`, `last_success_utc`

### Airflow period (week 12)
- Один DAG Run = один день `{{ ds }}`
- Extract/load с `--start {{ ds }} --end {{ ds }}`
- Порядок: `extract >> transform >> dq >> load`
- При DQ FAIL load не выполняется

### Retry safety
- Postgres load не использует слепой append без delete period
- Повтор DAG run за тот же `ds` перезаписывает тот же период

## Команды запуска

```bat
scripts\pipeline.bat full
scripts\pipeline.bat incremental
scripts\run_dq.bat
scripts\run_postgres.bat
scripts\run_load.bat
scripts\run_airflow.bat
scripts\run_llm_summary.bat
```
