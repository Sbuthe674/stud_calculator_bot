import logging
from typing import cast

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.main_menu import back_to_main
from services.gemini_service import ask_gemini, GeminiError
from states.calculation_states import AssistantStates

router = Router()


@router.callback_query(lambda callback: callback.data == "menu:assistant")
async def start_assistant(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    assert callback.message is not None
    callback_message = cast(Message, callback.message)
    await callback_message.edit_text(
        "🤖 Задайте свой учебный вопрос. Я обращусь к Gemini и отвечу вам.",
        reply_markup=back_to_main,
    )
    await state.set_state(AssistantStates.waiting_for_question)


@router.message(StateFilter(AssistantStates.waiting_for_question))
async def process_question(message: Message, state: FSMContext) -> None:
    question = (message.text or "").strip()
    if not question:
        await message.answer("Пожалуйста, сформулируйте вопрос.")
        return

    await message.answer("Ищу ответ... Подождите пожалуйста.")
    try:
        answer = await ask_gemini(question)
    except GeminiError as exc:
        logging.exception("Gemini error")
        await message.answer(str(exc), reply_markup=back_to_main)
        await state.clear()
        return
    except Exception as exc:
        logging.exception("Unexpected Gemini error")
        await message.answer(
            "Произошла ошибка при запросе к Gemini. Попробуйте позже.",
            reply_markup=back_to_main,
        )
        await state.clear()
        return

    await message.answer(answer, reply_markup=back_to_main)
    await state.clear()
