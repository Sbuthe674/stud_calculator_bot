import sqlite3

conn = sqlite3.connect("data/history.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    calc_type TEXT,
    result TEXT
)
""")

conn.commit()


def save_history(user_id, calc_type, result):
    cursor.execute(
        "INSERT INTO history(user_id, calc_type, result) VALUES (?, ?, ?)",
        (user_id, calc_type, result)
    )
    conn.commit()


def get_history(user_id):
    cursor.execute(
        "SELECT calc_type, result FROM history WHERE user_id=?",
        (user_id,)
    )

    return cursor.fetchall()
