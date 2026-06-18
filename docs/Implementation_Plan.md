# Implementation Plan — вариант 03

## 1. Краткое описание
Архив погоды Open-Meteo для Новосибирска: API → RAW → NORMALIZED → MART.

## 8. План-график
| Неделя | Что делаю | Артефакт |
|---|---|---|
| 1 | Структура, conda, setup_env.bat | `scripts/setup_env.bat`, `broken_env.py` |
| 2 | Extract Open-Meteo | `src/sem2_de/extract.py`, `data/raw/` |
| 3 | Normalize + EDA | `normalize.py`, `notebooks/week3_eda.ipynb` |
| 4 | Mart | TBD |
