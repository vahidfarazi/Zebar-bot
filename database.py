import sqlite3


DB_NAME = "azarakhsh.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_database():

    conn = get_connection()
    cur = conn.cursor()

    # کاربران
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        chat_id INTEGER PRIMARY KEY,
        state TEXT,
        first_name TEXT,
        last_name TEXT,
        username TEXT
    )
    """)

    # درخواست ها
    cur.execute("""
    CREATE TABLE IF NOT EXISTS requests(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tracking_code TEXT UNIQUE,

        chat_id INTEGER,

        service TEXT,

        sub_service TEXT,

        identifier_type TEXT,

        identifier_value TEXT,

        status TEXT,

        answer TEXT,

        expert_id INTEGER,

        created_at TEXT,

        answered_at TEXT,

        closed_at TEXT

    )
    """)

    conn.commit()
    conn.close()


init_database()
