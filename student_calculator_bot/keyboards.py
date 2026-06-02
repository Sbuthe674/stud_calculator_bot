from telegram import ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    [
        ["📊 GPA", "📈 Средний балл"],
        ["📝 Рейтинг допуска", "🎯 Прогноз оценки"],
        ["📂 История"]
    ],
    resize_keyboard=True
)
