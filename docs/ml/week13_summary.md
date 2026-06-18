# Week 13 — anomaly summary (variant 03)

## Method
- Z-score on daily `T_mean`, threshold |z| > 1.5

## Results
- Days in mart: 14
- Anomalies flagged: 3

## Interpretation
Аномальные дни — кандидаты на ручную проверку (погодное событие vs ошибка данных).
Модель не использовалась; эвристика достаточна для учебного объёма данных.

## Artifacts
- `metrics.png` — график с выделением аномалий
- `anomalies_top.csv` — таблица подозрительных дней
