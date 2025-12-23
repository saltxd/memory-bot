"""
SQLite + FTS5 database module for memory-bot.
Single file, no ORM, just clean SQL.
"""

import sqlite3
import os
from datetime import datetime, timezone
from typing import Optional
from zoneinfo import ZoneInfo

DB_PATH = os.getenv("DB_PATH", "/data/memory.db")
TIMEZONE = os.getenv("TIMEZONE", "America/Denver")


def get_tz() -> ZoneInfo:
    """Get configured timezone."""
    try:
        return ZoneInfo(TIMEZONE)
    except Exception:
        return ZoneInfo("UTC")


def connect() -> sqlite3.Connection:
    """Get a connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Initialize database schema.
    Creates tables and FTS5 virtual table if they don't exist.
    Safe to call multiple times.
    """
    conn = connect()

    # Main memories table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_id TEXT NOT NULL,
            channel_id TEXT,
            content TEXT NOT NULL
        )
    """)

    # FTS5 virtual table for fast full-text search
    # We use content="" for an external content table (contentless)
    # and manually keep it in sync
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
            content,
            content='memories',
            content_rowid='id'
        )
    """)

    # Triggers to keep FTS in sync with main table
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
            INSERT INTO memories_fts(rowid, content) VALUES (new.id, new.content);
        END
    """)

    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
            INSERT INTO memories_fts(memories_fts, rowid, content)
            VALUES('delete', old.id, old.content);
        END
    """)

    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
            INSERT INTO memories_fts(memories_fts, rowid, content)
            VALUES('delete', old.id, old.content);
            INSERT INTO memories_fts(rowid, content) VALUES (new.id, new.content);
        END
    """)

    # Index for timestamp queries
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_memories_ts ON memories(timestamp)
    """)

    conn.commit()
    conn.close()


def add_memory(
    user_id: str,
    content: str,
    channel_id: Optional[str] = None
) -> int:
    """
    Store a new memory entry.
    Returns the row ID of the inserted memory.
    """
    now = datetime.now(timezone.utc).isoformat()
    conn = connect()
    cursor = conn.execute(
        "INSERT INTO memories (timestamp, user_id, channel_id, content) VALUES (?, ?, ?, ?)",
        (now, user_id, channel_id, content)
    )
    memory_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return memory_id


def search_memories(query: str, limit: int = 5) -> list[dict]:
    """
    Search memories using FTS5.
    Returns list of dicts with id, timestamp, user_id, content, snippet.
    """
    conn = connect()

    # FTS5 match query - escape special chars
    # Use * for prefix matching on last word
    words = query.strip().split()
    if words:
        # Quote each word and add prefix match to last word
        fts_query = " ".join(f'"{w}"' for w in words[:-1])
        if fts_query:
            fts_query += " "
        fts_query += f'"{words[-1]}"*'
    else:
        return []

    try:
        rows = conn.execute("""
            SELECT
                m.id,
                m.timestamp,
                m.user_id,
                m.content,
                snippet(memories_fts, 0, '**', '**', '...', 32) as snippet
            FROM memories_fts
            JOIN memories m ON memories_fts.rowid = m.id
            WHERE memories_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (fts_query, limit)).fetchall()
    except sqlite3.OperationalError:
        # If FTS query fails, fall back to LIKE
        rows = conn.execute("""
            SELECT
                id,
                timestamp,
                user_id,
                content,
                content as snippet
            FROM memories
            WHERE content LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (f"%{query}%", limit)).fetchall()

    conn.close()

    results = []
    tz = get_tz()
    for row in rows:
        ts = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
        local_ts = ts.astimezone(tz)
        results.append({
            "id": row["id"],
            "timestamp": row["timestamp"],
            "local_date": local_ts.strftime("%Y-%m-%d %H:%M"),
            "user_id": row["user_id"],
            "content": row["content"],
            "snippet": row["snippet"][:200] if row["snippet"] else ""
        })

    return results


def get_recent_memories(limit: int = 20) -> list[dict]:
    """Get most recent memories for context."""
    conn = connect()
    rows = conn.execute("""
        SELECT id, timestamp, user_id, content
        FROM memories
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()

    results = []
    tz = get_tz()
    for row in rows:
        ts = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
        local_ts = ts.astimezone(tz)
        results.append({
            "id": row["id"],
            "timestamp": row["timestamp"],
            "local_date": local_ts.strftime("%Y-%m-%d %H:%M"),
            "user_id": row["user_id"],
            "content": row["content"]
        })

    return results


def get_memory_count() -> int:
    """Get total number of memories stored."""
    conn = connect()
    count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    conn.close()
    return count
