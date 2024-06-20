import sqlite3

from database.consts import DATABASE_NAME, SETUP_QUERY_PATH
from database.utils import open_sql_query

def init_database():
    conn = sqlite3.connect(DATABASE_NAME)

    setup_query = open_sql_query(SETUP_QUERY_PATH)

    conn.executescript(setup_query)
    conn.commit()
    conn.close()
