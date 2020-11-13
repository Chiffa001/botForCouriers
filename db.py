import os
from typing import List, Dict

import sqlite3

conn = sqlite3.connect(os.path.join("db", "deliveries.db"))
cursor = conn.cursor()


def fetch_all(table: str, columns: List[str]) -> List[Dict]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


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
