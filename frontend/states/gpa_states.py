from aiogram.fsm.state import State, StatesGroup


class GPAStates(StatesGroup):
    waiting_for_grades = State()
