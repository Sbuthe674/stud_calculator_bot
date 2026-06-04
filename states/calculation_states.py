from aiogram.fsm.state import State, StatesGroup


class GPAStates(StatesGroup):
    waiting_for_agpa = State()
    waiting_for_iros = State()
    waiting_for_ssci = State()
    waiting_for_weights = State()


class AverageStates(StatesGroup):
    waiting_for_scores = State()


class AdmissionRatingStates(StatesGroup):
    waiting_for_current_score = State()
    waiting_for_checkpoint_score = State()


class ExamForecastStates(StatesGroup):
    waiting_for_current_rating = State()
    waiting_for_target_score = State()


class AssistantStates(StatesGroup):
    waiting_for_question = State()
