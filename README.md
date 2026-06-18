# TP Сквозной проект — вариант 03

## Неделя 1 — окружение (Windows)

```bat
scripts\setup_env.bat
```

Скрипт создаёт conda-окружение `tp-v03`, ставит зависимости из `requirements.txt` и запускает smoke-тест:

```bat
conda run -n tp-v03 python broken_env.py
```

В конце `setup_env.bat` должно быть **`[OK]`**.

### Почему pip install может попасть не в тот Python?

На Windows часто несколько интерпретаторов (системный Python, Store, conda). Команда `pip install` привязана к тому `python.exe`, который первым в `PATH`. Если активировано не то окружение, пакеты ставятся мимо conda-env. Надёжнее: `conda run -n tp-v03 python -m pip install ...`.

## GitHub

Репозиторий: https://github.com/VizhichenkoAA/python-weeks-html

```bat
scripts\setup_git.bat
scripts\connect_github.bat
```

## Структура

`configs/`, `data/`, `docs/`, `notebooks/`, `scripts/`, `src/`, `tests/`
