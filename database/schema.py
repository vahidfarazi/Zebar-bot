"""
database/schema.py

PostgreSQL database schema initialization.
"""

from .connection import get_connection


def init_database() -> None:
    """
    Create all required database tables.
    """

    connection = get_connection()

    print("DATABASE INITIALIZED")

    try:

        with connection.cursor() as cursor:

            # -----------------------------
            # Users
            # -----------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                chat_id BIGINT PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                role TEXT DEFAULT 'USER',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # -----------------------------
            # Requests
            # -----------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests (

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

                closed_at TIMESTAMP,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # -----------------------------
            # Request Messages
            # -----------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS request_messages (

                id BIGSERIAL PRIMARY KEY,

                tracking_code TEXT NOT NULL,

                sender_type TEXT NOT NULL,

                sender_id BIGINT NOT NULL,

                message_type TEXT NOT NULL,

                message TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # -----------------------------
            # Request History
            # -----------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS request_history (

                id BIGSERIAL PRIMARY KEY,

                tracking_code TEXT NOT NULL,

                event_type TEXT NOT NULL,

                actor_type TEXT NOT NULL,

                actor_id BIGINT,

                description TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # -----------------------------
            # Tracking Sequences
            # -----------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracking_sequences (

                year TEXT NOT NULL,

                department_code TEXT NOT NULL,

                last_number INTEGER NOT NULL DEFAULT 0,

                PRIMARY KEY (
                    year,
                    department_code
                )
            )
            """)

            # -----------------------------
            # Experts
            # -----------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS experts (

                chat_id BIGINT PRIMARY KEY,

                name TEXT,

                username TEXT,

                department TEXT,

                is_active BOOLEAN DEFAULT TRUE
            )
            """)

            # -----------------------------
            # Admins
            # -----------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (

                chat_id BIGINT PRIMARY KEY
            )
            """)

            # -----------------------------
            # Settings
            # -----------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (

                key TEXT PRIMARY KEY,

                value TEXT
            )
            """)

            # -----------------------------
            # Holidays
            # -----------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS holidays (

                holiday_date TEXT PRIMARY KEY,

                enabled BOOLEAN DEFAULT TRUE
            )
            """)

            # -----------------------------
            # System Logs
            # -----------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (

                id BIGSERIAL PRIMARY KEY,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                level TEXT NOT NULL,

                module TEXT NOT NULL,

                action TEXT NOT NULL,

                description TEXT
            )
            """)

            # -----------------------------
            # Default Admin
            # -----------------------------
            cursor.execute(
                """
                INSERT INTO admins(chat_id)
                VALUES (%s)
                ON CONFLICT (chat_id) DO NOTHING
                """,
                (93686674,),
            )

            connection.commit()

    finally:

        connection.close()
