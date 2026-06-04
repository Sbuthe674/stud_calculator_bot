import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.db import create_tables
from handlers import register_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


async def main() -> None:
    assert BOT_TOKEN is not None, "BOT_TOKEN должен быть указан в .env"

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    register_handlers(dp)
    await create_tables()

    logging.info("Запуск Telegram-бота Студенческий калькулятор")
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, allowed_updates=['message', 'callback_query'])
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
