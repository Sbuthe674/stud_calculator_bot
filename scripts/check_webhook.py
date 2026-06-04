import asyncio
import sys
import os
from aiogram import Bot

# Ensure project root is on sys.path when running from scripts/
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import BOT_TOKEN

async def main():
    assert BOT_TOKEN is not None, "BOT_TOKEN missing in .env"
    bot = Bot(token=BOT_TOKEN)
    try:
        me = await bot.get_me()
        info = await bot.get_webhook_info()
        print("BOT:", me)
        print("WEBHOOK_INFO:", info)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
