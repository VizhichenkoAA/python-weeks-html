# LLM Usage Log

| Дата | Задача | Инструмент | Что сделал LLM | Что проверил вручную |
|---|---|---|---|---|
| 2026-06-18 | Недели 1–4: scaffold, extract, normalize, mart | LLM (Claude) | Структура репо, bat-скрипты, Python-модули, docs | Запуск setup_env.bat и pipeline, сверка с variant_03.yml и API |
| 2026-06-18 | Неделя 5: Postgres load | LLM | load.py, docker-compose, sql_checks | run_postgres + run_load, SQL count |
| 2026-06-18 | Недели 6–14: pipeline, DQ, BI, Airflow, ML, LLM | LLM | pipeline, dq, figures, DAGs, llm_summary | pytest, pipeline full/incremental, dq_report, artifacts in docs/ |

## Week 14 — пример записи LLM

| Дата | Цель | Контекст | Промпт | Ответ | Проверка | Итог |
|---|---|---|---|---|---|---|
| 2026-06-18 | Сводка по mart | min/max/mean из `llm_summary.py` | Summarize using ONLY provided metrics | template summary | Числа сверены с mart CSV | PASS |

## Правила использования
- Секреты (токены) — только в `.env`, не в репозитории
- Код API и схемы данных — сверка с `configs/variant_03.yml`
- Артефакты data/* — проверка выборочно в Excel/pandas
