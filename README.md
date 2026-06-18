# TP Сквозной проект — вариант 03

**Тема:** архив погоды Open-Meteo, Новосибирск (`RU_NSK`)

Пайплайн: **API → RAW → NORMALIZED → MART → Postgres → BI → DQ → Airflow → LLM**

GitHub: [python-weeks-html](https://github.com/VizhichenkoAA/python-weeks-html)

---

## Быстрый старт (Windows)

### 1. Инструменты

PowerShell **от администратора** (один раз):

```powershell
Set-ExecutionPolicy -Scope Process Bypass -Force
.\scripts\install_tools.ps1
```

Нужны: **Git**, **Miniconda**, **Docker Desktop** (Postgres — с недели 5).

### 2. Окружение Python (неделя 1)

```bat
scripts\setup_env.bat
```

Скрипт создаёт conda-окружение `tp-v03` (Python 3.11), ставит `requirements.txt` и запускает smoke-тест `broken_env.py`. В конце должно быть **`[OK]`**.

#### Почему `pip install` может попасть не в тот Python? (неделя 1, часть 0.3)

На Windows часто установлено несколько интерпретаторов (системный Python, Store, conda). Команда `pip install` привязана к тому `python.exe`, который первым в `PATH`. Если активировано не то окружение, пакеты ставятся «мимо» conda-env. Решение: использовать `conda run -n tp-v03 python -m pip install ...` или активировать env (`conda activate tp-v03`) перед pip.

### 3. Git + GitHub

```bat
scripts\setup_git.bat
```

Создайте пустой репозиторий на GitHub (сейчас: `python-weeks-html`), затем:

```bat
scripts\connect_github.bat
```

---

## Пайплайн (недели 2–4)

Из корня репозитория:

```bat
scripts\run_extract.bat
scripts\run_normalize.bat
scripts\run_mart.bat
```

Или целиком:

```bat
scripts\run_pipeline.bat
```

Переменная `PYTHONPATH=src` задаётся в bat-файлах; альтернатива:

```bat
set PYTHONPATH=src
conda run -n tp-v03 python -m sem2_de.cli pipeline
```

### Артефакты

| Слой | Путь |
|---|---|
| Raw | `data/raw/variant_03/open_meteo_*.json` |
| Normalized | `data/normalized/variant_03/*.csv` |
| Mart | `data/mart/variant_03/mart_daily_*.csv` |

Конфиг: `configs/variant_03.yml`  
Справочники: `reference/*.csv`

---

## Неделя 5 — Postgres + load

### 1. Поднять Postgres (Docker)

```bat
scripts\run_postgres.bat
docker ps
```

Параметры: `localhost:5433`, БД `tp_variant_03`, user `tp_user` (см. `docker-compose.yml`). Порт 5433 выбран, чтобы не конфликтовать с локальным Postgres на 5432.

### 2. Подключение (секреты в `.env`)

```bat
copy .env.example .env
```

`DATABASE_URL=postgresql+psycopg2://tp_user:tp_pass@localhost:5433/tp_variant_03`

### 3. Загрузка mart в Postgres

```bat
scripts\run_load.bat
```

Таблица: `mart_variant_03` (стратегия `replace`, идемпотентный повторный запуск).

SQL-проверки: `docs/sql_checks.md`

### Часть 0 (SQLite + commit)

```bat
conda run -n tp-v03 python broken_sqlite_commit.py
```

---

## Недели 6–14 — полный продукт

### Неделя 6 — pipeline + state

```bat
scripts\pipeline.bat full
scripts\pipeline.bat incremental
```

- `src/sem2_de/pipeline.py` — режимы `full` / `incremental`
- `data/state.json` — watermark
- Часть 0: `broken_append.py`

### Неделя 7 — визуализация

- `notebooks/week7_viz.ipynb`
- `docs/figures/week7_*.png`
- Часть 0: `broken_plot_dates.py`

### Неделя 8 — DQ

```bat
scripts\run_dq.bat
conda run -n tp-v03 pytest tests/test_dq.py
```

- `src/sem2_de/dq.py`, `data/dq_report.json`, `docs/dq.md`
- Часть 0: `broken_dq_assert.py`

### Неделя 9 — Data Governance

- `docs/Data_Contract.md` (v1.1 + changelog)
- `docs/data_dictionary.md`
- Часть 0: `broken_units.py`

### Неделя 10 — Docker + Metabase + BI

```bat
scripts\run_postgres.bat
docker compose up -d metabase
```

- Metabase: http://localhost:3000
- Postgres внутри Docker-сети: host `postgres`, с Windows: `localhost:5433`
- Скриншоты: `docs/bi/` (см. `scripts/generate_bi_screenshots.py`)

### Неделя 11 — Airflow

```bat
scripts\run_airflow.bat
```

- UI: http://localhost:8080 (`airflow` / `airflow`)
- DAG: `airflow/dags/etl_variant_03.py`
- Часть 0: `airflow/dags/broken_dag.py`

### Неделя 12 — инкремент + DQ gate

- DAG: `extract >> transform >> dq >> load`
- Load: delete period + insert (retry-safe)
- Период: `--start` / `--end` или `{{ ds }}` в Airflow

### Неделя 13 — ML / аномалии

- `notebooks/week13_ml.ipynb`
- `docs/ml/week13_summary.md`, `anomalies_top.csv`
- Часть 0: `broken_ml_leakage.py`

### Неделя 14 — LLM summary (финал)

```bat
scripts\run_llm_summary.bat
```

- `src/sem2_de/llm_summary.py` → `docs/llm/summary.md`
- Правила: `docs/LLM_Rules.md`
- API-ключ в `.env` (опционально; без ключа — template mode)

### Одна команда (full ETL + DQ + load)

```bat
scripts\pipeline.bat full
```

---

## Учебные скрипты (часть 0)

```bat
conda run -n tp-v03 python broken_env.py
conda run -n tp-v03 python broken_pandas_read.py
conda run -n tp-v03 python broken_merge.py
conda run -n tp-v03 python broken_sqlite_commit.py
conda run -n tp-v03 python broken_append.py demo
conda run -n tp-v03 python broken_plot_dates.py both
conda run -n tp-v03 python broken_dq_assert.py
conda run -n tp-v03 python broken_units.py
conda run -n tp-v03 python broken_ml_leakage.py
```

---

## Структура репозитория

```
configs/          # variant_03.yml
data/raw|normalized|mart|state/
data/dq_report.json
docs/             # Data_Contract, dq, bi, ml, llm, airflow
notebooks/        # week3_eda, week7_viz, week13_ml
airflow/dags/     # etl_variant_03.py
reference/        # cities, countries, ...
scripts/          # pipeline.bat, run_*.bat
src/sem2_de/      # extract, transform, mart, load, dq, pipeline, llm_summary
tests/
docker-compose.yml
docker-compose.airflow.yml
```

Документация: `docs/Implementation_Plan.md`, `docs/Data_Contract.md`, `docs/LLM_Usage_Log.md`
