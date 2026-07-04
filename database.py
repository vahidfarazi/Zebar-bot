import sqlite3
from datetime import datetime

DB_NAME = "azarakhsh.db"


# ==========================
# CONNECTION
# ==========================

def get_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================
# DATABASE
# ==========================

def init_database():

    conn = get_connection()

    cur = conn.cursor()

    # ---------------- USERS ----------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS users(

        chat_id INTEGER PRIMARY KEY,

        state TEXT,

        service TEXT,

        sub_service TEXT,

        current_request TEXT,

        first_name TEXT,

        last_name TEXT,

        username TEXT,

        created_at TEXT,

        last_activity TEXT

    )

    """)

    # ---------------- REQUESTS ----------------

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

    )

    """)

    # ---------------- REQUEST MESSAGES ----------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS request_messages(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        request_id INTEGER,

        sender_type TEXT,

        sender_id INTEGER,

        message TEXT,

        attachment TEXT,

        created_at TEXT

    )

    """)

    # ---------------- EXPERTS ----------------

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

    # ---------------- ADMINS ----------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS admins(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        chat_id INTEGER UNIQUE,

        name TEXT,

        role TEXT,

        active INTEGER DEFAULT 1

    )

    """)

    # ---------------- SETTINGS ----------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS settings(

        key TEXT PRIMARY KEY,

        value TEXT

    )

    """)

    # ---------------- HOLIDAYS ----------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS holidays(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        holiday_date TEXT UNIQUE,

        enabled INTEGER DEFAULT 1

    )

    """)

    # ---------------- LOGS ----------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        chat_id INTEGER,

        action TEXT,

        created_at TEXT

    )

    """)

    # ---------------- SYSTEM LOGS ----------------

    cur.execute("""

    CREATE TABLE IF NOT EXISTS system_logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        admin_id INTEGER,

        action TEXT,

        created_at TEXT

    )

    """)

    conn.commit()

    conn.close()
    
    # ==========================
# DEFAULT SETTINGS
# ==========================

def init_settings():

    defaults = {

        "system_mode": "NORMAL",

        "work_start": "7",

        "work_end": "13",

        "allow_new_request": "1",

        "allow_status": "1"

    }

    conn = get_connection()

    cur = conn.cursor()

    for key, value in defaults.items():

        cur.execute("""

            INSERT OR IGNORE INTO settings(

                key,

                value

            )

            VALUES(?,?)

        """, (

            key,

            value

        ))

    conn.commit()

    conn.close()


# ==========================
# USERS
# ==========================

def get_user(chat_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        "SELECT * FROM users WHERE chat_id=?",

        (chat_id,)

    )

    row = cur.fetchone()

    conn.close()

    return row


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

            current_request,

            first_name,

            last_name,

            username,

            created_at,

            last_activity

        )

        VALUES(?,?,?,?,?,?,?,?,?,?)

    """, (

        chat_id,

        "MAIN_MENU",

        "",

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

    cur.execute("""

        UPDATE users

        SET

            state=?,

            last_activity=?

        WHERE chat_id=?

    """, (

        state,

        datetime.now().isoformat(),

        chat_id

    ))

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


def set_current_request(chat_id, tracking_code):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        UPDATE users

        SET

            current_request=?

        WHERE chat_id=?

    """, (

        tracking_code,

        chat_id

    ))

    conn.commit()

    conn.close()


# ==========================
# LOGS
# ==========================

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

    conn.commit()

    conn.close()


# ==========================
# START DATABASE
# ==========================

init_database()

init_settings()
