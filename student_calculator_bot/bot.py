from telegram.ext import (
    Application,
    CommandHandler
)

from config import TOKEN
from handlers.start import start


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    print("Bot started")

    app.run_polling()


if __name__ == "__main__":
    main()
