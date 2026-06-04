from typing import cast

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.main_menu import back_to_main
from services.calculator import calculate_admission_rating
from services.history_service import ensure_user, save_calculation
from states.calculation_states import AdmissionRatingStates

router = Router()


@router.callback_query(lambda callback: callback.data == "menu:admission_rating")
async def choose_admission_rating(callback, state: FSMContext) -> None:
    await callback.answer()
    assert callback.message is not None
    callback_message = cast(Message, callback.message)
    await callback_message.edit_text(
        "Введите текущий рейтинг контроля, например 72.5",
        reply_markup=back_to_main,
    )
    await state.set_state(AdmissionRatingStates.waiting_for_current_score)


@router.message(StateFilter(AdmissionRatingStates.waiting_for_current_score))
async def ask_checkpoint_score(message: Message, state: FSMContext) -> None:
    try:
        current_score = float((message.text or "").strip())
    except ValueError:
        await message.answer("Введите число для текущего рейтинга, например 72.5.")
        return

    await state.update_data(current_score=current_score)
    await state.set_state(AdmissionRatingStates.waiting_for_checkpoint_score)
    await message.answer(
        "Введите рубежный контроль, например: 80",
        reply_markup=back_to_main,
    )


@router.message(StateFilter(AdmissionRatingStates.waiting_for_checkpoint_score))
async def calculate_rating(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    try:
        checkpoint_score = float((message.text or "").strip())
    except ValueError:
        await message.answer("Введите число для рубежного контроля, например 80.")
        return

    current_score = data.get("current_score", 0.0)
    rating = calculate_admission_rating(current_score, checkpoint_score)
    result_text = (
        f"📝 <b>Рейтинг допуска</b>\n"
        f"Текущий контроль: <b>{current_score}</b>\n"
        f"Рубежный контроль: <b>{checkpoint_score}</b>\n"
        f"Рейтинг допуска: <b>{rating}</b>"
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
        calc_type="Рейтинг допуска",
        input_data=f"Текущий {current_score}, Рубежный {checkpoint_score}",
        result=f"Рейтинг={rating}",
    )

    await state.clear()
    await message.answer(result_text, parse_mode="HTML", reply_markup=back_to_main)
