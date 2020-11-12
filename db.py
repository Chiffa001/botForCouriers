import os

import sqlite3

conn = sqlite3.connect(os.path.join("db", "deliveries.db"))
cursor = conn.cursor()


def get_cursor():
    return cursor


def _init_db():
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exist():
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='delivery'")
    is_table_exist = cursor.fetchall()
    if is_table_exist:
        return
    _init_db()


check_db_exist()
