from database.consts import DATABASE_NAME, DEFAULT_QUERY_PATH
import sqlite3


def open_sql_query(query_name):
    query_path = f"{DEFAULT_QUERY_PATH}/{query_name}.sql"

    with open(query_path, "r") as f:
        sql_queries = f.read()

    return sql_queries

def get_table_columns(table_name: str) -> list:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()

    return [column_info[1] for column_info in columns_info]


