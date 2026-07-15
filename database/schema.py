"""
database/schema.py

PostgreSQL database schema initialization.
"""

from .connection import get_connection


# -------------------------------------------------
# Migration Helper
# -------------------------------------------------

def add_column_if_missing(
    cursor,
    table: str,
    column: str,
    definition: str,
):

    cursor.execute(
        """
        SELECT column_name

        FROM information_schema.columns

        WHERE table_schema='public'

        AND table_name=%s

        AND column_name=%s
        """,
        (
            table,
            column,
        ),
    )

    exists = cursor.fetchone()

    if not exists:

        cursor.execute(
            f"""
            ALTER TABLE {table}

            ADD COLUMN {column}
            {definition}
            """
        )


# -------------------------------------------------
# Create Tables
# -------------------------------------------------

def init_database() -> None:

    connection = get_connection()

    try:

        with connection.cursor() as cursor:


            # -----------------------------
            # Users
            # -----------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users
                (
                    chat_id BIGINT PRIMARY KEY,

                    username TEXT,

                    full_name TEXT,

                    role TEXT DEFAULT 'USER',

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )


            # -----------------------------
            # Requests
            # -----------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS requests
                (

                    id BIGSERIAL PRIMARY KEY,

                    tracking_code TEXT UNIQUE NOT NULL,

                    chat_id BIGINT NOT NULL,

                    service TEXT NOT NULL,

                    sub_service TEXT,

                    status TEXT DEFAULT 'OPEN',

                    priority TEXT DEFAULT 'NORMAL',

                    expert_id BIGINT,

                    expert_chat_id BIGINT,

                    expert_message_id BIGINT,

                    assigned_at TIMESTAMP,

                    transferred_at TIMESTAMP,

                    first_response_at TIMESTAMP,

                    closed_at TIMESTAMP,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                )
                """
            )


            # -----------------------------
            # Messages
            # -----------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS request_messages
                (

                    id BIGSERIAL PRIMARY KEY,

                    tracking_code TEXT NOT NULL,

                    sender_type TEXT NOT NULL,

                    sender_id BIGINT NOT NULL,

                    message_type TEXT NOT NULL,

                    message TEXT NOT NULL,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                )
                """
            )


            # -----------------------------
            # History
            # -----------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS request_history
                (

                    id BIGSERIAL PRIMARY KEY,

                    tracking_code TEXT NOT NULL,

                    event_type TEXT NOT NULL,

                    actor_type TEXT NOT NULL,

                    actor_id BIGINT,

                    description TEXT,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                )
                """
            )


            # -----------------------------
            # Experts
            # -----------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS experts
                (

                    chat_id BIGINT PRIMARY KEY,

                    name TEXT,

                    username TEXT,

                    department TEXT,

                    phone TEXT,

                    is_active BOOLEAN DEFAULT TRUE,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                )
                """
            )


            # -----------------------------
            # Admins
            # -----------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS admins
                (

                    chat_id BIGINT PRIMARY KEY,

                    active BOOLEAN DEFAULT TRUE

                )
                """
            )


            # -----------------------------
            # Settings
            # -----------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS settings
                (

                    key TEXT PRIMARY KEY,

                    value TEXT

                )
                """
            )


            # -----------------------------
            # Holidays
            # -----------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS holidays
                (

                    holiday_date TEXT PRIMARY KEY,

                    enabled BOOLEAN DEFAULT TRUE

                )
                """
            )


            # -----------------------------
            # Tracking Sequence
            # -----------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tracking_sequences
                (

                    year TEXT NOT NULL,

                    department_code TEXT NOT NULL,

                    last_number INTEGER DEFAULT 0,

                    PRIMARY KEY
                    (
                        year,
                        department_code
                    )

                )
                """
            )


            # -----------------------------
            # Logs
            # -----------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS system_logs
                (

                    id BIGSERIAL PRIMARY KEY,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    level TEXT NOT NULL,

                    module TEXT NOT NULL,

                    action TEXT NOT NULL,

                    description TEXT

                )
                """
            )


            # -----------------------------
            # Migration Existing Requests
            # -----------------------------

            add_column_if_missing(
                cursor,
                "requests",
                "assigned_at",
                "TIMESTAMP",
            )

            add_column_if_missing(
                cursor,
                "requests",
                "transferred_at",
                "TIMESTAMP",
            )

            add_column_if_missing(
                cursor,
                "requests",
                "first_response_at",
                "TIMESTAMP",
            )


            add_column_if_missing(
                cursor,
                "admins",
                "active",
                "BOOLEAN DEFAULT TRUE",
            )


            # -----------------------------
            # Indexes
            # -----------------------------

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_requests_tracking

                ON requests(tracking_code)
                """
            )


            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_requests_chat

                ON requests(chat_id)
                """
            )


            connection.commit()


        print(
            "DATABASE INITIALIZED"
        )


    finally:

        connection.close()



# -------------------------------------------------
# Compatibility Alias
# -------------------------------------------------

def create_tables():

    init_database()
