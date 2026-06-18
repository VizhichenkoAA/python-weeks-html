# LLM Summary — variant 03 (template mode)

> Generated without external API. All numbers copied from computed context.

## Context
```
Dataset: mart_variant_03 variant=03 source=Open-Meteo Новосибирск
Grain: 1 row = 1 day x city_id
Period: 2025-01-01 .. 2025-01-14 rows=14
T_mean_avg=-7.6 C
P_sum_total=19.7 mm
wind_max_peak=26.0 km/h
rainy_hours_total=91
Quality: dq PASS
Constraints: do not invent numbers; use only metrics above.
```

## Interpretation (rule-based)
- Средняя дневная температура за период: **-7.6 °C**.
- Суммарные осадки: **19.7 мм** за 14 дней.
- Пик ветра: **26.0 км/ч**.
- Дождливых часов (сумма по дням): **91**.

## Top wind days
- 2025-01-02 00:00:00: wind_max=26.0 km/h
- 2025-01-03 00:00:00: wind_max=25.9 km/h
- 2025-01-10 00:00:00: wind_max=25.5 km/h

## Risks / next checks
- Сверить единицы ветра (км/ч) с Data Contract.
- При расширении периода пересчитать DQ и обновить watermark.


## Verification
- PASS: key metrics found in summary text.
