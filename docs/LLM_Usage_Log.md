# LLM Usage Log

| Дата | Задача | Инструмент | Что сделал LLM | Что проверил вручную |
|---|---|---|---|---|
| 2026-06-18 | Недели 1–4: scaffold, extract, normalize, mart | LLM (Claude) | Структура репо, bat-скрипты, Python-модули, docs | Запуск setup_env.bat и pipeline, сверка с variant_03.yml и API |
| 2026-06-18 | Неделя 5: Postgres load | LLM | load.py, docker-compose, sql_checks | run_postgres + run_load, SQL count |

## Правила использования
- Секреты (токены) — только в `.env`, не в репозитории
- Код API и схемы данных — сверка с `configs/variant_03.yml`
- Артефакты data/* — проверка выборочно в Excel/pandas
