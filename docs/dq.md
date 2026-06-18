# DQ rules — вариант 03

Модуль: `src/sem2_de/dq.py`  
Отчёт: `data/dq_report.json`

## Слои

| Проверка | Слой | Критичность |
|---|---|---|
| non_empty | normalized, mart | FAIL |
| not_null_critical | normalized (`ts`, `city_id`), mart (`city_id`, `date`) | FAIL |
| unique_business_key | normalized (`city_id`,`ts`), mart (`city_id`,`date`) | FAIL |
| range_temperature_2m | normalized | FAIL |
| range_relative_humidity_2m | normalized | WARNING |
| non_negative_precipitation | normalized | FAIL |
| non_negative_P_sum | mart | FAIL |
| range_obs_hours | mart | WARNING |

## Место в пайплайне

**Week 12 (DQ gate):** `extract → transform → dq → load`  
При `FAIL` load не выполняется.

Запуск вручную:

```bat
scripts\run_dq.bat
```

## Unit-тесты

`tests/test_dq.py` — позитивный, негативный, граничный сценарии.

Демонстрация ложного PASS: `broken_dq_assert.py`.
