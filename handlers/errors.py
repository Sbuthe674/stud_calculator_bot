import logging

from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()


@router.errors()
async def global_error_handler(event: ErrorEvent) -> bool:
    logging.exception("Unexpected error: %s", event.exception)

    update = event.update
    if update.callback_query:
        query = update.callback_query
        if query.message:
            await query.message.answer(
                "Произошла ошибка. Пожалуйста, повторите действие или используйте /start."
            )
        else:
            await query.answer("Произошла ошибка.", show_alert=True)
    elif update.message:
        await update.message.answer(
            "Произошла ошибка. Попробуйте снова или перезапустите бота командой /start."
        )

    return True
