from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    last_interaction: str | None = None


@dataclass
class CalculationRecord:
    id: int
    user_id: int
    calc_type: str
    input_data: str
    result: str
    created_at: str
