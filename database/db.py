import os
from typing import Any

try:
    import aiosqlite  # type: ignore
except Exception:
    aiosqlite = None  # type: ignore

from config import DATABASE_PATH

conn: Any = None


async def get_db() -> Any:
    global conn
    if conn is None:
        os.makedirs(os.path.dirname(DATABASE_PATH) or ".", exist_ok=True)
        db = await aiosqlite.connect(DATABASE_PATH)  # type: ignore
        db.row_factory = aiosqlite.Row  # type: ignore
        await db.execute("PRAGMA foreign_keys = ON;")
        conn = db
    return conn


async def create_tables() -> None:
    db = await get_db()
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            last_interaction TEXT
        );

        CREATE TABLE IF NOT EXISTS calculations_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            calc_type TEXT NOT NULL,
            input_data TEXT,
            result TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """
    )
    await db.commit()
