from typing import cast

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from services.history_service import get_user_history, delete_history_item, clear_user_history

router = Router()


def build_history_markup(entries):
    buttons = []
    for entry in entries:
        buttons.append([
            InlineKeyboardButton(
                text=f"Удалить #{entry.id}",
                callback_data=f"history:delete:{entry.id}",
            )
        ])
    buttons.append([
        InlineKeyboardButton(text="Очистить историю", callback_data="history:clear")
    ])
    buttons.append([
        InlineKeyboardButton(text="↩️ Главное меню", callback_data="menu:main")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(lambda callback: callback.data == "menu:history")
async def show_history(callback: CallbackQuery) -> None:
    await callback.answer()
    assert callback.message is not None
    callback_message = cast(Message, callback.message)
    entries = await get_user_history(callback.from_user.id)
    if not entries:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="↩️ Главное меню", callback_data="menu:main")]
        ])
        await callback_message.edit_text(
            "📂 Ваша история расчётов пустая.", reply_markup=keyboard
        )
        return

    history_text = "📂 <b>История расчетов</b>:\n\n"
    history_text += "\n".join(
        f"#{entry.id} {entry.calc_type} — {entry.result} ({entry.created_at[:19]})"
        for entry in entries
    )

    await callback_message.edit_text(
        history_text,
        parse_mode="HTML",
        reply_markup=build_history_markup(entries),
    )


@router.callback_query(lambda callback: callback.data is not None and callback.data.startswith("history:delete:"))
async def delete_history_entry(callback: CallbackQuery) -> None:
    assert callback.message is not None
    callback_message = cast(Message, callback.message)
    assert callback.data is not None
    record_id = int(callback.data.split(":", 2)[2])
    deleted = await delete_history_item(callback.from_user.id, record_id)
    await callback.answer("Запись удалена." if deleted else "Не удалось удалить запись.")

    entries = await get_user_history(callback.from_user.id)
    if not entries:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="↩️ Главное меню", callback_data="menu:main")]
        ])
        await callback_message.edit_text(
            "📂 История пуста.", reply_markup=keyboard
        )
        return

    history_text = "📂 <b>Обновлённая история</b>:\n\n"
    history_text += "\n".join(
        f"#{entry.id} {entry.calc_type} — {entry.result} ({entry.created_at[:19]})"
        for entry in entries
    )

    await callback_message.edit_text(
        history_text,
        parse_mode="HTML",
        reply_markup=build_history_markup(entries),
    )
    return


@router.callback_query(lambda callback: callback.data == "history:clear")
async def clear_history_callback(callback: CallbackQuery) -> None:
    await clear_user_history(callback.from_user.id)
    assert callback.message is not None
    callback_message = cast(Message, callback.message)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Главное меню", callback_data="menu:main")]
    ])
    await callback_message.edit_text(
        "📂 История очищена.", reply_markup=keyboard
    )
