from typing import cast

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.main_menu import back_to_main
from services.calculator import calculate_average
from services.history_service import ensure_user, save_calculation
from states.calculation_states import AverageStates

router = Router()


@router.callback_query(lambda callback: callback.data == "menu:average")
async def choose_average(callback, state: FSMContext) -> None:
    await callback.answer()
    assert callback.message is not None
    callback_message = cast(Message, callback.message)
    await callback_message.edit_text(
        "Отправьте список оценок через пробел или запятую.\n"
        "Например: 4, 5, 4.5, 3",
        reply_markup=back_to_main,
    )
    await state.set_state(AverageStates.waiting_for_scores)


@router.message(StateFilter(AverageStates.waiting_for_scores))
async def collect_scores(message: Message, state: FSMContext) -> None:
    text = (message.text or "").replace(",", " ").strip()
    parts = [item for item in text.split() if item]

    if not parts:
        await message.answer(
            "Введите список оценок через пробел или запятую, например: 4, 5, 4.5"
        )
        return

    try:
        scores = [float(item) for item in parts]
    except ValueError:
        await message.answer("Каждая оценка должна быть числом.")
        return

    average, percent = calculate_average(scores)
    result_text = (
        f"📈 <b>Средний текущий балл</b>\n"
        f"Среднее: <b>{average}</b>\n"
        f"Оценка в процентах: <b>{percent}%</b>"
    )

    assert message.from_user is not None
    await ensure_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await save_calculation(
        user_id=message.from_user.id,
        calc_type="Средний балл",
        input_data=", ".join(parts),
        result=f"Среднее={average}, {percent}%",
    )

    await state.clear()
    await message.answer(result_text, parse_mode="HTML", reply_markup=back_to_main)
