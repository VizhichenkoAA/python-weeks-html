"""Неделя 5, часть 0: почему таблица пустая (commit / не та БД)."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path


DB_PATH = Path("example.db")


def demo_without_commit() -> None:
    print("=== Без commit после INSERT ===")
    print("db file:", os.path.abspath(DB_PATH))

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("create table if not exists t(x int);")
    con.commit()
    cur.execute("delete from t;")
    con.commit()
    cur.execute("insert into t(x) values (1);")
    # BUG: забыли con.commit()
    con.close()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("select count(*) from t;")
    print("count =", cur.fetchone()[0])
    con.close()


def demo_with_commit() -> None:
    print("=== С commit после INSERT ===")
    print("db file:", os.path.abspath(DB_PATH))

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("create table if not exists t(x int);")
    con.commit()
    cur.execute("delete from t;")
    con.commit()
    cur.execute("insert into t(x) values (1);")
    con.commit()
    con.close()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("select count(*) from t;")
    print("count =", cur.fetchone()[0])
    con.close()


if __name__ == "__main__":
    demo_without_commit()
    demo_with_commit()
