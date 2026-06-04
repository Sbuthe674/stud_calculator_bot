from typing import cast

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.main_menu import back_to_main
from services.calculator import calculate_exam_forecast
from services.history_service import ensure_user, save_calculation
from states.calculation_states import ExamForecastStates

router = Router()


@router.callback_query(lambda callback: callback.data == "menu:exam_forecast")
async def choose_exam_forecast(callback, state: FSMContext) -> None:
    await callback.answer()
    assert callback.message is not None
    callback_message = cast(Message, callback.message)
    await callback_message.edit_text(
        "Введите текущий рейтинг, например: 65.0",
        reply_markup=back_to_main,
    )
    await state.set_state(ExamForecastStates.waiting_for_current_rating)


@router.message(StateFilter(ExamForecastStates.waiting_for_current_rating))
async def ask_target_score(message: Message, state: FSMContext) -> None:
    try:
        current_rating = float((message.text or "").strip())
    except ValueError:
        await message.answer("Введите число для текущего рейтинга, например 65.0.")
        return

    await state.update_data(current_rating=current_rating)
    await state.set_state(ExamForecastStates.waiting_for_target_score)
    assert message.from_user is not None
    await message.answer(
        "Введите желаемую итоговую оценку, например: 85",
        reply_markup=back_to_main,
    )


@router.message(StateFilter(ExamForecastStates.waiting_for_target_score))
async def calculate_forecast(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        target_score = float((message.text or "").strip())
    except ValueError:
        await message.answer("Введите число для желаемой оценки, например 85.")
        return

    current_rating = data.get("current_rating", 0.0)
    required_score, advise = calculate_exam_forecast(current_rating, target_score)

    result_text = (
        f"🎯 <b>Прогноз итоговой оценки</b>\n"
        f"Текущий рейтинг: <b>{current_rating}</b>\n"
        f"Желаемая оценка: <b>{target_score}</b>\n"
        f"{advise}"
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
        calc_type="Прогноз экзамена",
        input_data=f"Текущий {current_rating}, Цель {target_score}",
        result=f"Требуется {required_score}",
    )

    await state.clear()
    await message.answer(result_text, parse_mode="HTML", reply_markup=back_to_main)
