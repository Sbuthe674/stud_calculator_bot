#!/usr/bin/env python
import sys
import asyncio
import argparse

def runbot():
    # Import here so module-level code in bot.py can assume project root
    import bot
    try:
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
        return

def webinfo():
    # Show getMe and webhook info without starting polling
    from config import BOT_TOKEN
    from aiogram import Bot

    async def _info():
        bot = Bot(token=BOT_TOKEN)
        try:
            me = await bot.get_me()
            info = await bot.get_webhook_info()
            print('BOT:', me)
            print('WEBHOOK_INFO:', info)
        finally:
            await bot.session.close()

    asyncio.run(_info())

def main():
    parser = argparse.ArgumentParser(prog='manage.py')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('runbot')
    sub.add_parser('webinfo')

    args = parser.parse_args()
    if args.command == 'runbot':
        runbot()
    elif args.command == 'webinfo':
        webinfo()
    else:
        parser.print_help()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bot stopped by user.")
