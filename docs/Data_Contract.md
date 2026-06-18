# Data Contract — вариант 03 (Open-Meteo)

## 1. Источник
- **Название:** Open-Meteo Archive API
- **Endpoint:** `GET https://archive-api.open-meteo.com/v1/archive`
- **Ключ API:** не требуется

## 3. Схема (normalized)
**Grain:** одна строка = одно часовое наблюдение для `city_id`.

| Поле | Тип | Описание |
|---|---|---|
| ts | timestamp | Локальное время |
| temperature_2m | float | Температура, °C |
| relative_humidity_2m | float | Влажность, % |
| precipitation | float | Осадки, мм |
| wind_speed_10m | float | Ветер, км/ч |
| city_id | string | Ключ справочника |

**Файл:** `data/normalized/variant_03/YYYY-MM-DD_HH-MM-SS.csv`
