# Implementation Plan — вариант 03

## 1. Краткое описание задачи
Архив погоды для Новосибирска из Open-Meteo Archive API: загрузка JSON (raw), приведение к почасовой таблице (normalized), дневная витрина с KPI (mart) и справочником городов.

## 2. Цель и ожидаемый результат
- Файлы: `data/raw/variant_03/*.json`, `data/normalized/variant_03/*.csv`, `data/mart/variant_03/mart_daily_*.csv`
- KPI: T_mean, P_sum, rainy_hours, топ-5 дней по ветру (wind_max / wind_rank)
- Далее: Postgres, BI, DQ, Airflow (недели 5–14)

## 3. Контуры системы (high level)
Open-Meteo API → RAW (JSON) → Normalize (CSV hourly) → Mart (CSV daily + reference) → Postgres → Metabase → DQ → Airflow → LLM summary

## 4. Схема данных
### 4.1 Raw слой
- **Файл:** `data/raw/variant_03/open_meteo_<timestamp>.json`
- **Ключи:** `_meta.city_id`, `hourly.time[]`
- **Пример:** вложенный объект `hourly` с массивами полей API

### 4.2 Normalized слой
- **Таблица:** почасовые наблюдения (см. `docs/Data_Contract.md`)
- **Поля:** ts, temperature_2m, relative_humidity_2m, precipitation, wind_speed_10m, city_id

### 4.3 Mart слой (агрегаты)
- **Таблица:** `mart_daily_*`
- **Периодичность:** 1 строка на день
- **KPI:** T_mean, P_sum, rainy_hours, wind_max, wind_rank (топ-5 по ветру)

## 5. Data Quality (DQ)
- NOT NULL: ts, city_id
- Диапазоны температуры/влажности/осадков (в `normalize.py`)
- Уникальность (city_id, ts)
- Referential: join `reference/cities.csv` с `validate='many_to_one'`
- Freshness: `_meta.fetched_at_utc` в raw

## 6. Инкрементальность и идемпотентность
- Каждый запуск создаёт новый файл с timestamp в имени
- Дедупликация по (city_id, ts) при normalize
- Повторный запуск не перезаписывает старые артефакты

## 7. План тестирования
- `broken_env.py` — smoke после setup
- `broken_pandas_read.py` — sep и пропуски
- `broken_merge.py` — many-to-many
- Ручной прогон `scripts\run_pipeline.bat`

## 8. План-график (по неделям)
| Неделя | Что делаю | Артефакт/ссылка |
|---|---|---|
| 1 | Структура, conda, setup_env.bat | `scripts/setup_env.bat`, `broken_env.py` |
| 2 | Extract Open-Meteo | `src/sem2_de/extract.py`, `data/raw/` |
| 3 | Normalize + EDA | `normalize.py`, `notebooks/week3_eda.ipynb` |
| 4 | Mart + reference join | `mart.py`, `data/mart/` |
| 5 | Postgres load | TBD |
| 6 | Full pipeline | TBD |
| 7 | Визуализация | TBD |
| 8 | DQ checks | TBD |
| 9 | Data Contract финал | `docs/Data_Contract.md` |
| 10 | Docker + Metabase | TBD |
| 11 | Airflow DAG | TBD |
| 12 | Incremental | TBD |
| 13 | ML / anomalies | TBD |
| 14 | LLM summary | TBD |

## 9. Риски и ограничения
- Лимиты и доступность Open-Meteo API
- Часовой пояс Asia/Novosibirsk при агрегации по дням
- Пропуски в hourly (null) — учитываются в агрегатах

## 10. Что использую из LLM
- Помощь в структуре репозитория и шаблонах кода
- Проверяю руками: API-ответ, типы полей, результаты CSV
- Не делегирую LLM секреты и финальную сдачу без проверки
