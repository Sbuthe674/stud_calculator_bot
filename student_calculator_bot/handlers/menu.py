from telegram import Update
from telegram.ext import ContextTypes

from database import get_history


async def menu_handler(update: Update,
                       context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📊 GPA":
        await update.message.reply_text(
            "📊 Расчёт GPA\n\n"
            "Функция находится в разработке.\n"
            "Скоро здесь можно будет вводить предметы, кредиты и оценки."
        )

    elif text == "📈 Средний балл":
        await update.message.reply_text(
            "📈 Расчёт среднего балла\n\n"
            "Введите оценки через пробел.\n\n"
            "Пример:\n"
            "80 75 90 100"
        )

    elif text == "📝 Рейтинг допуска":
        await update.message.reply_text(
            "📝 Рейтинг допуска\n\n"
            "Введите РК1 и РК2 через пробел.\n\n"
            "Пример:\n"
            "85 90"
        )

    elif text == "🎯 Прогноз оценки":
        await update.message.reply_text(
            "🎯 Прогноз итоговой оценки\n\n"
            "Введите рейтинг допуска и желаемую итоговую оценку.\n\n"
            "Пример:\n"
            "82 90"
        )

    elif text == "📂 История":

        user_id = update.effective_user.id
        history = get_history(user_id)

        if not history:
            await update.message.reply_text(
                "📂 История пока пуста."
            )
            return

        message = "📂 История расчётов:\n\n"

        for i, item in enumerate(history, start=1):
            calc_type, result = item
            message += f"{i}. {calc_type}: {result}\n"

        await update.message.reply_text(message)

    else:
        await update.message.reply_text(
            "Используйте кнопки меню ниже 👇"
        )
