# TP Сквозной проект — вариант 03

Пайплайн: **API → RAW → NORMALIZED → MART → …**

## Неделя 1 — окружение

```bat
scripts\setup_env.bat
conda run -n tp-v03 python broken_env.py
```

### Почему pip install может попасть не в тот Python?

На Windows несколько интерпретаторов; `pip` в PATH может относиться к другому Python. Используйте `conda run -n tp-v03 python -m pip install ...`.

## Неделя 2 — Extract (Open-Meteo)

```bat
scripts\run_extract.bat
```

Артефакт: `data/raw/variant_03/open_meteo_*.json`

Конфиг: `configs/variant_03.yml`

## GitHub

https://github.com/VizhichenkoAA/python-weeks-html
