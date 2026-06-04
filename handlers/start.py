from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu

router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(
        "Добро пожаловать в <b>Студенческий калькулятор</b> 🎓\n\n"
        "Я помогу посчитать GPA автоматически на основе ваших оценок,\n"
        "а также рассчитать средний балл, рейтинг допуска, прогноз экзамена и ответить на студенческие вопросы.",
        reply_markup=main_menu,
    )
