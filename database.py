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

        current_request TEXT

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

        priority TEXT DEFAULT 'NORMAL',

        expert_id INTEGER,

        created_at TEXT,

        updated_at TEXT,

        closed_at TEXT

        CREATE TABLE IF NOT EXISTS request_messages(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    request_id INTEGER,

    sender_type TEXT,

    sender_id INTEGER,

    message TEXT,

    attachment TEXT,

    created_at TEXT

)

    )
    """)

    # کارشناسان
    cur.execute("""
    CREATE TABLE IF NOT EXISTS experts(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        chat_id INTEGER,

        name TEXT,

        username TEXT,

        department TEXT,

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
    # ---------------- REQUESTS ----------------

def get_request_by_tracking(tracking_code):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM requests WHERE tracking_code=?",
        (tracking_code,)
    )

    row = cur.fetchone()

    conn.close()

    return row


def get_request_by_id(request_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM requests WHERE id=?",
        (request_id,)
    )

    row = cur.fetchone()

    conn.close()

    return row


def update_request_status(request_id, status):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        UPDATE requests

        SET

            status=?,

            updated_at=?

        WHERE id=?

    """, (

        status,

        datetime.now().isoformat(),

        request_id

    ))

    conn.commit()
    conn.close()


def assign_expert(request_id, expert_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        UPDATE requests

        SET

            expert_id=?,

            updated_at=?

        WHERE id=?

    """, (

        expert_id,

        datetime.now().isoformat(),

        request_id

    ))

    conn.commit()
    conn.close()


# ---------------- REQUEST MESSAGES ----------------

def add_request_message(

    request_id,

    sender_type,

    sender_id,

    message,

    attachment=None

):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        INSERT INTO request_messages(

            request_id,

            sender_type,

            sender_id,

            message,

            attachment,

            created_at

        )

        VALUES(?,?,?,?,?,?)

    """, (

        request_id,

        sender_type,

        sender_id,

        message,

        attachment,

        datetime.now().isoformat()

    ))

    conn.commit()
    conn.close()


def get_request_messages(request_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM request_messages

        WHERE request_id=?

        ORDER BY id ASC

    """, (

        request_id,

    ))

    rows = cur.fetchall()

    conn.close()

    return rows


# ---------------- ADMINS ----------------

def is_admin(chat_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(

        """

        SELECT *

        FROM admins

        WHERE chat_id=?

        AND active=1

        """,

        (chat_id,)

    )

    row = cur.fetchone()

    conn.close()

    return row is not None


def add_admin(chat_id, name, role="ADMIN"):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        INSERT OR IGNORE INTO admins(

            chat_id,

            name,

            role,

            active

        )

        VALUES(?,?,?,1)

    """, (

        chat_id,

        name,

        role

    ))

    conn.commit()
    conn.close()


# ---------------- SETTINGS ----------------

def get_setting(key):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(

        "SELECT value FROM settings WHERE key=?",

        (key,)

    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row["value"]

    return None


def set_setting(key, value):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        INSERT INTO settings(

            key,

            value

        )

        VALUES(?,?)

        ON CONFLICT(key)

        DO UPDATE SET

        value=excluded.value

    """, (

        key,

        str(value)

    ))

    conn.commit()
    conn.close()


# ---------------- HOLIDAYS ----------------

def add_holiday(date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        INSERT OR IGNORE INTO holidays(

            holiday_date,

            enabled

        )

        VALUES(?,1)

    """, (

        date,

    ))

    conn.commit()
    conn.close()


def remove_holiday(date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(

        "DELETE FROM holidays WHERE holiday_date=?",

        (date,)

    )

    conn.commit()
    conn.close()


def is_holiday(date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM holidays

        WHERE holiday_date=?

        AND enabled=1

    """, (

        date,

    ))

    row = cur.fetchone()

    conn.close()

    return row is not None


# ---------------- SYSTEM LOGS ----------------

def write_system_log(admin_id, action):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        INSERT INTO system_logs(

            admin_id,

            action,

            created_at

        )

        VALUES(?,?,?)

    """, (

        admin_id,

        action,

        datetime.now().isoformat()

    ))

        request_id = cur.lastrowid
 
        conn.commit()

        conn.close()

        return request_id
