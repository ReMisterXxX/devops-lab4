import os

import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", 5432)),
        dbname=os.getenv("POSTGRES_DB", "lab4"),
        user=os.getenv("POSTGRES_USER", "lab4"),
        password=os.getenv("POSTGRES_PASSWORD", "lab4pass"),
    )


def init_db():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id SERIAL PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN NOT NULL DEFAULT FALSE)"
        )


def check_db():
    init_db()
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM tasks")
        return True


def list_tasks():
    with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
        return [dict(r) for r in cur.fetchall()]


def add_task(title):
    with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, done", (title,))
        return dict(cur.fetchone())
