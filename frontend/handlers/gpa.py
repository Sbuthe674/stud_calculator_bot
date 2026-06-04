from typing import cast

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from backend.services.gpa_service import (
    GRADE_MAP,
    VALID_GRADES,
    calculate_gpa_from_grades,
    format_grades,
    interpret_gpa,
    split_grade_tokens,
    validate_grades,
)
from frontend.keyboards.gpa_keyboard import gpa_keyboard
from frontend.states.gpa_states import GPAStates
from keyboards.main_menu import back_to_main

router = Router()


@router.callback_query(lambda callback: callback.data == "menu:gpa")
async def start_gpa(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    assert callback.message is not None
    callback_message = cast(Message, callback.message)

    await callback_message.edit_text(
        "<b>Рассчитать GPA</b>\n\n"
        "Введите ваши оценки по предметам через пробел 👇\n\n"
        "Например:\n"
        "A A- B+ B C\n\n"
        "Я автоматически переведу оценки в баллы и посчитаю итоговый GPA.",
        parse_mode="HTML",
        reply_markup=back_to_main,
    )
    await state.set_state(GPAStates.waiting_for_grades)


@router.message(StateFilter(GPAStates.waiting_for_grades))
async def calculate_gpa(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    grades = split_grade_tokens(text)

    if not grades:
        await message.answer(
            "Пожалуйста, введите оценки через пробел.\n"
            "Например: A A- B+ B C",
            reply_markup=gpa_keyboard,
        )
        return

    normalized, invalid = validate_grades(grades)
    if invalid is not None:
        await message.answer(
            f"❌ Оценка '{invalid}' не распознана.\n"
            f"Используйте оценки:\n{VALID_GRADES}",
            reply_markup=gpa_keyboard,
        )
        return

    final_gpa = calculate_gpa_from_grades(normalized)
    result = interpret_gpa(final_gpa)
    grades_text = format_grades(normalized)
    count = len(normalized)

    await state.clear()
    await message.answer(
        "📊 <b>Ваш GPA</b>\n\n"
        f"Оценки:\n{grades_text}\n\n"
        f"Количество предметов: {count}\n\n"
        f"<b>Итоговый GPA:</b>\n{final_gpa:.2f}\n\n"
        f"<b>Интерпретация:</b> {result}",
        parse_mode="HTML",
        reply_markup=gpa_keyboard,
    )


@router.callback_query(lambda callback: callback.data == "gpa:repeat")
async def repeat_gpa(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    assert callback.message is not None
    callback_message = cast(Message, callback.message)

    await callback_message.edit_text(
        "<b>Рассчитать GPA</b>\n\n"
        "Введите ваши оценки по предметам через пробел 👇\n\n"
        "Например:\n"
        "A A- B+ B C\n\n"
        "Я автоматически переведу оценки в баллы и посчитаю итоговый GPA.",
        parse_mode="HTML",
        reply_markup=back_to_main,
    )
    await state.set_state(GPAStates.waiting_for_grades)
