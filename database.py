import sqlite3
from datetime import datetime

DB_NAME = "azarakhsh.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():

    conn = get_connection()
    cur = conn.cursor()

    # کاربران
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        chat_id INTEGER PRIMARY KEY,

        state TEXT,

        service TEXT,

        sub_service TEXT,

        first_name TEXT,

        last_name TEXT,

        username TEXT,

        created_at TEXT,

        last_activity TEXT

    )
    """)

    # درخواست‌ها
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

    # کارشناسان
    cur.execute("""
    CREATE TABLE IF NOT EXISTS experts(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        username TEXT,

        active INTEGER DEFAULT 1

    )
    """)

    # لاگ
    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        chat_id INTEGER,

        action TEXT,

        created_at TEXT

    )
    """)

    conn.commit()
    conn.close()


# ---------------- USERS ----------------

def get_user(chat_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE chat_id=?",
        (chat_id,)
    )

    user = cur.fetchone()

    conn.close()

    return user


def create_user(chat_id, first_name="", last_name="", username=""):

    now = datetime.now().isoformat()

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    INSERT OR IGNORE INTO users(

        chat_id,

        state,

        service,

        sub_service,

        first_name,

        last_name,

        username,

        created_at,

        last_activity

    )

    VALUES(?,?,?,?,?,?,?,?,?)

    """, (

        chat_id,

        "MAIN_MENU",

        "",

        "",

        first_name,

        last_name,

        username,

        now,

        now

    ))

    conn.commit()

    conn.close()


def update_state(chat_id, state):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        "UPDATE users SET state=?,last_activity=? WHERE chat_id=?",

        (

            state,

            datetime.now().isoformat(),

            chat_id

        )

    )

    conn.commit()

    conn.close()


def update_service(chat_id, service, sub_service=""):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    UPDATE users

    SET

        service=?,

        sub_service=?,

        last_activity=?

    WHERE chat_id=?

    """, (

        service,

        sub_service,

        datetime.now().isoformat(),

        chat_id

    ))

    conn.commit()

    conn.close()


def write_log(chat_id, action):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    INSERT INTO logs(

        chat_id,

        action,

        created_at

    )

    VALUES(?,?,?)

    """, (

        chat_id,

        action,

        datetime.now().isoformat()

    ))

    conn.commit()

    conn.close()


init_database()
# ---------------- REQUESTS ----------------

def request_exists(service, identifier_value):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM requests

    WHERE

        service=?

        AND identifier_value=?

        AND status<>'CLOSED'

    ORDER BY id DESC

    LIMIT 1

    """, (

        service,

        identifier_value

    ))

    row = cur.fetchone()

    conn.close()

    return row


def create_request(

    tracking_code,

    chat_id,

    service,

    sub_service,

    identifier_type,

    identifier_value

):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    INSERT INTO requests(

        tracking_code,

        chat_id,

        service,

        sub_service,

        identifier_type,

        identifier_value,

        status,

        created_at

    )

    VALUES(?,?,?,?,?,?,?,?)

    """, (

        tracking_code,

        chat_id,

        service,

        sub_service,

        identifier_type,

        identifier_value,

        "NEW",

        datetime.now().isoformat()

    ))

    conn.commit()

    conn.close()


def get_last_request():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT tracking_code

    FROM requests

    ORDER BY id DESC

    LIMIT 1

    """)

    row = cur.fetchone()

    conn.close()

    return row
