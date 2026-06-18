# Data Contract — вариант 03 (Open-Meteo, Новосибирск)

## 1. Источник
- **Название:** Open-Meteo Archive API
- **Endpoint:** `GET https://archive-api.open-meteo.com/v1/archive`
- **Параметры:** `latitude`, `longitude`, `timezone`, `start_date`, `end_date`, `hourly` (список полей)
- **Ключ API:** не требуется
- **Частота обновления:** по расписанию пайплайна (ручной/батник на неделях 2–4)

## 2. Владение и ответственность
- **Owner:** студент (вариант 03)
- **Consumer:** витрина `mart_daily`, дашборд (недели 7+)
- **SLA:** best-effort для учебного проекта

## 3. Схема (normalized)
**Grain:** одна строка = одно часовое наблюдение для `city_id`.

| Поле | Тип | Nullable | Описание | Пример |
|---|---|---|---|---|
| ts | timestamp | NO | Локальное время (Asia/Novosibirsk) | 2025-01-01 00:00:00 |
| temperature_2m | float | YES | Температура на 2 м, °C | -12.3 |
| relative_humidity_2m | float | YES | Относительная влажность, % | 78.0 |
| precipitation | float | YES | Осадки, мм | 0.1 |
| wind_speed_10m | float | YES | Скорость ветра, км/ч | 15.2 |
| city_id | string | NO | Ключ справочника городов | RU_NSK |

**Файл:** `data/normalized/variant_03/YYYY-MM-DD_HH-MM-SS.csv`

## 4. Допущения и единицы измерения
- Температура: **°C** (как в Open-Meteo)
- Время: **локальное** (`Asia/Novosibirsk`), не UTC
- Осадки: мм; ветер: км/ч (единицы API)

## 5. Правила качества
- **Uniqueness:** уникальность `(city_id, ts)`
- **Completeness:** `ts` и `city_id` NOT NULL
- **Validity:** `temperature_2m` ∈ [-80; 60]; `relative_humidity_2m` ∈ [0; 100]; `precipitation` ≥ 0
- **Freshness:** метка `_meta.fetched_at_utc` в raw JSON
- **Consistency:** `city_id` должен существовать в `reference/cities.csv`

## 6. Mart (daily)
**Grain:** один день × город.

| Поле | Тип | Описание |
|---|---|---|
| city_id | string | Ключ города |
| date | date | Календарный день |
| T_mean | float | Средняя температура за день |
| P_sum | float | Сумма осадков за день |
| wind_max | float | Максимальная скорость ветра за день |
| rainy_hours | int | Число часов с осадками > 0 |
| obs_hours | int | Число часовых наблюдений в дне |
| city_name, country_code, ... | из reference | Атрибуты из `cities.csv` |
| wind_rank | float | Ранг дня по `wind_max` (1 = самый ветреный) |

**Файл:** `data/mart/variant_03/mart_daily_YYYY-MM-DD_HH-MM-SS.csv`

## 7. Версионирование
- **Версия контракта:** 1.0 (неделя 3–4)
- Изменения фиксируются коммитами в `docs/Data_Contract.md` и `configs/variant_03.yml`
