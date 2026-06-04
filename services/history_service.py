from __future__ import annotations

from datetime import datetime

from database.db import get_db
from database.models import User, CalculationRecord


async def ensure_user(user_id: int, username: str | None, first_name: str | None, last_name: str | None) -> User:
    db = await get_db()
    now = datetime.utcnow().isoformat()
    await db.execute(
        "INSERT OR IGNORE INTO users(user_id, username, first_name, last_name, last_interaction) VALUES (?, ?, ?, ?, ?)",
        (user_id, username, first_name, last_name, now),
    )
    await db.execute(
        "UPDATE users SET username = ?, first_name = ?, last_name = ?, last_interaction = ? WHERE user_id = ?",
        (username, first_name, last_name, now, user_id),
    )
    await db.commit()
    return User(user_id=user_id, username=username, first_name=first_name, last_name=last_name, last_interaction=now)


async def save_calculation(user_id: int, calc_type: str, input_data: str, result: str) -> None:
    db = await get_db()
    created_at = datetime.utcnow().isoformat()
    await db.execute(
        "INSERT INTO calculations_history(user_id, calc_type, input_data, result, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, calc_type, input_data, result, created_at),
    )
    await db.commit()


async def get_user_history(user_id: int, limit: int = 20) -> list[CalculationRecord]:
    db = await get_db()
    cursor = await db.execute(
        "SELECT id, user_id, calc_type, input_data, result, created_at FROM calculations_history WHERE user_id = ? ORDER BY id DESC LIMIT ?",
        (user_id, limit),
    )
    rows = await cursor.fetchall()
    return [CalculationRecord(**dict(row)) for row in rows]


async def delete_history_item(user_id: int, record_id: int) -> bool:
    db = await get_db()
    cursor = await db.execute(
        "DELETE FROM calculations_history WHERE id = ? AND user_id = ?",
        (record_id, user_id),
    )
    await db.commit()
    return cursor.rowcount > 0


async def clear_user_history(user_id: int) -> None:
    db = await get_db()
    await db.execute("DELETE FROM calculations_history WHERE user_id = ?", (user_id,))
    await db.commit()
