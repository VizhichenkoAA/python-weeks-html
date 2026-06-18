# TP Сквозной проект — вариант 03

Пайплайн: **API → RAW → NORMALIZED → MART → …**

## Окружение

```bat
scripts\setup_env.bat
```

## Неделя 2 — Extract

```bat
scripts\run_extract.bat
```

Raw: `data/raw/variant_03/open_meteo_*.json`

## Неделя 3 — Normalize + EDA

```bat
scripts\run_normalize.bat
```

Normalized: `data/normalized/variant_03/*.csv`  
Ноутбук: `notebooks/week3_eda.ipynb`  
Контракт: `docs/Data_Contract.md`

## GitHub

https://github.com/VizhichenkoAA/python-weeks-html
