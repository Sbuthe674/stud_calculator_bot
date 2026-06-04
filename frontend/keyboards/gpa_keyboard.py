from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


gpa_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔄 Повторить расчет", callback_data="gpa:repeat")],
    [InlineKeyboardButton(text="↩️ Назад в меню", callback_data="menu:main")],
    [InlineKeyboardButton(text="❓ Помощь", callback_data="menu:help")],
])
