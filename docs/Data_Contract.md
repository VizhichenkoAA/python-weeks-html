# Data Contract — вариант 03 (Open-Meteo, Новосибирск)

**Contract version:** 1.1  
**Last updated:** 2026-06-18

## Changelog
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-06-18 | Initial normalized + mart schema (weeks 3–4) |
| 1.1 | 2026-06-18 | Full column specs, units, DQ mapping, governance (week 9) |

---

## 1. Общие сведения
- **Проект / вариант:** TP сквозной проект, вариант 03
- **Источник:** Open-Meteo Archive API
- **Город:** Новосибирск (`RU_NSK`)
- **Часовой пояс:** `Asia/Novosibirsk` (локальное время в normalized/mart)
- **Гранулярность:** normalized — 1 час; mart — 1 день × город

## 2. Источник (raw)
- **Endpoint:** `GET https://archive-api.open-meteo.com/v1/archive`
- **Файл:** `data/raw/variant_03/open_meteo_{start}_{end}_{timestamp}.json`
- **Ключ API:** не требуется
- **Freshness:** `_meta.fetched_at_utc` в JSON

## 3. Normalized layer

**Grain:** 1 строка = 1 часовое наблюдение для `city_id`.

| column_name | dtype | nullable | unit | description |
|---|---|---|---|---|
| ts | timestamp | NO | local datetime | Время измерения (TZ города) |
| temperature_2m | float | YES | °C | Температура на 2 м |
| relative_humidity_2m | float | YES | % | Относительная влажность |
| precipitation | float | YES | mm | Осадки за час |
| wind_speed_10m | float | YES | km/h | Скорость ветра (единицы API) |
| city_id | string | NO | — | Ключ справочника городов |

**Файл:** `data/normalized/variant_03/{timestamp}.csv`

## 4. Mart layer

**Grain:** 1 строка = 1 календарный день × `city_id`.  
**Business key:** `(city_id, date)`

| column_name | dtype | nullable | unit | description | Как считается |
|---|---|---|---|---|---|
| city_id | string | NO | — | ID города | из normalized |
| date | date | NO | day | Календарный день | `ts.dt.date` |
| T_mean | float | YES | °C | Средняя T за день | `mean(temperature_2m)` |
| P_sum | float | YES | mm | Сумма осадков | `sum(precipitation)` |
| wind_max | float | YES | km/h | Макс. ветер | `max(wind_speed_10m)` |
| rainy_hours | int | NO | hours | Дождливые часы | count(precipitation > 0) |
| obs_hours | int | NO | hours | Число hourly строк | count(ts) |
| city_name | string | YES | text | Название | join `cities.csv` |
| country_code | string | YES | — | Страна | join `cities.csv` |
| latitude | float | YES | deg | Широта | join |
| longitude | float | YES | deg | Долгота | join |
| timezone | string | YES | IANA | TZ | join |
| wind_rank | float | YES | rank | Ранг по ветру | dense rank wind_max ASC=1 top |

**Файл:** `data/mart/variant_03/mart_daily_{timestamp}.csv`  
**Postgres:** `mart_variant_03` (port 5433 on host)

## 5. Data Quality
См. `docs/dq.md` и `configs/variant_03.yml` → `dq_rules`.

## 6. Governance
- Словарь данных: `docs/data_dictionary.md`
- Единицы фиксируются в контракте (вариант A); см. `broken_units.py`
- Версионирование: semver в шапке + changelog

## 7. Consumers
- BI (Metabase, week 10)
- Notebooks week 7, 13
- LLM summary (week 14) — только агрегаты из mart
