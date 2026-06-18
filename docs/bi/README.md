# BI — неделя 10 (вариант 03)

## Запуск Metabase

```bat
scripts\run_postgres.bat
docker compose up -d metabase
```

- Metabase UI: http://localhost:3000
- Postgres из контейнера Metabase: host `postgres`, port `5432`, db `tp_variant_03`, user `tp_pass`
- С хоста Windows: `localhost:5433`

## Дашборд (минимум 3 визуализации)

1. Временной ряд `T_mean`
2. Bar `P_sum` или ranking по `wind_max`
3. KPI card: `COUNT(*)`, `AVG(T_mean)`, `SUM(P_sum)`

Скриншоты для сдачи: `dashboard_overview.png`, `chart_timeseries.png`, `chart_ranking.png`.
