from typing import cast

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.main_menu import main_menu

router = Router()


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "❓ <b>Помощь</b>\n\n"
        "Используйте главное меню для выбора нужного расчета:\n"
        "- Рассчитать GPA\n"
        "- Средняя оценка\n"
        "- Рейтинг допуска\n"
        "- Прогноз экзамена\n"
        "- История расчетов\n"
        "- ИИ-помощник\n\n"
        "Если вы зашли в режим расчета, просто следуйте подсказкам бота.\n"
        "Кнопка '↩️ Главное меню' вернет вас обратно.",
        parse_mode="HTML",
        reply_markup=main_menu,
    )


@router.callback_query(lambda callback: callback.data == "menu:help")
async def help_menu(callback: CallbackQuery) -> None:
    await callback.answer()
    assert callback.message is not None
    callback_message = cast(Message, callback.message)
    await callback_message.edit_text(
        "❓ <b>Раздел помощи</b>\n\n"
        "Нажмите одну из кнопок меню, чтобы начать расчет.\n"
        "Если что-то пошло не так, используйте /help или нажмите \"↩️ Главное меню\".",
        parse_mode="HTML",
        reply_markup=main_menu,
    )


@router.callback_query(lambda callback: callback.data == "menu:main")
async def return_to_main(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    assert callback.message is not None
    callback_message = cast(Message, callback.message)
    await callback_message.edit_text(
        "Добро пожаловать в <b>Студенческий калькулятор</b> 🎓\n\n"
        "Я помогу посчитать GPA, средний балл, рейтинг допуска, прогноз экзамена и ответить на студенческие вопросы.",
        parse_mode="HTML",
        reply_markup=main_menu,
    )
