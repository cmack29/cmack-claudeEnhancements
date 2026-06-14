"""
storage.py — Persist and retrieve messages using SQLite.
"""

import sqlite3
import threading
from contextlib import contextmanager

DB_PATH = "messages.db"
_lock = threading.Lock()


@contextmanager
def _get_conn():
    """Thread-safe SQLite connection context manager."""
    with _lock:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def init_db():
    """Create the messages table if it doesn't exist. Call once at startup."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id        TEXT PRIMARY KEY,
                sender    TEXT NOT NULL,
                recipient TEXT NOT NULL,
                body      TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                read      INTEGER DEFAULT 0
            )
        """)


def save_message(message: dict) -> dict:
    """Insert a validated message dict into the database. Returns it unchanged."""
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO messages VALUES (:id,:sender,:recipient,:body,:timestamp,:read)",
            message,
        )
    return message


def load_messages(recipient: str = None, unread_only: bool = False) -> list[dict]:
    """
    Fetch messages from the database.

    Args:
        recipient:   Filter to messages for this user. None returns all.
        unread_only: If True, only return messages where read=0.

    Returns:
        List of message dicts, ordered oldest-first.
    """
    query = "SELECT * FROM messages WHERE 1=1"
    params: list = []

    if recipient:
        query += " AND recipient = ?"
        params.append(recipient)
    if unread_only:
        query += " AND read = 0"

    query += " ORDER BY timestamp ASC"

    with _get_conn() as conn:
        rows = conn.execute(query, params).fetchall()

    return [dict(row) for row in rows]


def mark_as_read(message_id: str) -> bool:
    """
    Mark a single message as read.

    Returns:
        True if a row was updated, False if the ID wasn't found.
    """
    with _get_conn() as conn:
        cursor = conn.execute(
            "UPDATE messages SET read = 1 WHERE id = ?", (message_id,)
        )
    return cursor.rowcount > 0


def delete_message(message_id: str) -> bool:
    """
    Delete a message by ID.

    Returns:
        True if a row was deleted, False if the ID wasn't found.
    """
    with _get_conn() as conn:
        cursor = conn.execute(
            "DELETE FROM messages WHERE id = ?", (message_id,)
        )
    return cursor.rowcount > 0