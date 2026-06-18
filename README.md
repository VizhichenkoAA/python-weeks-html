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

Параметры: `localhost:5432`, БД `tp_variant_03`, user `tp_user` (см. `docker-compose.yml`).

### 2. Подключение (секреты в `.env`)

```bat
copy .env.example .env
```

`DATABASE_URL=postgresql+psycopg2://tp_user:tp_pass@localhost:5432/tp_variant_03`

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

## Учебные скрипты (часть 0)

```bat
conda run -n tp-v03 python broken_env.py
conda run -n tp-v03 python broken_pandas_read.py
conda run -n tp-v03 python broken_merge.py
conda run -n tp-v03 python broken_sqlite_commit.py
```

---

## Структура репозитория

```
configs/          # variant_03.yml
data/raw|normalized|mart|state/
docs/             # Data_Contract, Implementation_Plan, LLM_Usage_Log
notebooks/        # week3_eda.ipynb
reference/        # cities, countries, ...
scripts/          # setup_env.bat, run_*.bat
src/sem2_de/      # extract, normalize, mart, load, cli
tests/
```

Документация: `docs/Data_Contract.md`, `docs/Implementation_Plan.md`
