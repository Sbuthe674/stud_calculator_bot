import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

try:
    from dotenv import load_dotenv  # type: ignore
except Exception:
    def load_dotenv(*args, **kwargs):
        return None

load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-mini")
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/history.db")

if BOT_TOKEN is None:
    raise RuntimeError("Требуется переменная окружения BOT_TOKEN для запуска бота.")
