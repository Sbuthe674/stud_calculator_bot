from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📊 Рассчитать GPA", callback_data="menu:gpa"),
        InlineKeyboardButton(text="📈 Средняя оценка", callback_data="menu:average"),
    ],
    [
        InlineKeyboardButton(text="📝 Рейтинг допуска", callback_data="menu:admission_rating"),
        InlineKeyboardButton(text="🎯 Прогноз экзамена", callback_data="menu:exam_forecast"),
    ],
    [
        InlineKeyboardButton(text="📂 История расчётов", callback_data="menu:history"),
        InlineKeyboardButton(text="🤖 ИИ-помощник", callback_data="menu:assistant"),
    ],
    [
        InlineKeyboardButton(text="❓ Помощь", callback_data="menu:help"),
    ],
])

back_to_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="↩️ Главное меню", callback_data="menu:main")],
])

history_controls = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Очистить историю", callback_data="history:clear")],
    [InlineKeyboardButton(text="↩️ Главное меню", callback_data="menu:main")],
])
