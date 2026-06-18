# LLM Usage Log

| Дата | Задача | Инструмент | Что сделал LLM | Что проверил вручную |
|---|---|---|---|---|
| 2026-06-18 | Недели 1–4: scaffold, extract, normalize, mart | LLM (Claude) | Структура репо, bat-скрипты, Python-модули, docs | Запуск setup_env.bat и pipeline, сверка с variant_03.yml и API |

## Правила использования
- Секреты (токены) — только в `.env`, не в репозитории
- Код API и схемы данных — сверка с `configs/variant_03.yml`
- Артефакты data/* — проверка выборочно в Excel/pandas
