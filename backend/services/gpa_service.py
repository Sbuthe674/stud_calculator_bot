from __future__ import annotations

from typing import Iterable

GRADE_MAP = {
    "A": 4.0,
    "A-": 3.67,
    "B+": 3.33,
    "B": 3.0,
    "B-": 2.67,
    "C+": 2.33,
    "C": 2.0,
    "C-": 1.67,
    "D+": 1.33,
    "D": 1.0,
    "F": 0.0,
}

VALID_GRADES = ", ".join(GRADE_MAP.keys())


def normalize_grade_token(token: str) -> str:
    token = token.strip().upper()
    token = token.replace("–", "-")
    token = token.replace("—", "-")
    token = token.replace(",", " ")
    token = token.replace(" ", "")
    filtered = "".join(ch for ch in token if ch.isalnum() or ch in "+-")
    return filtered


def split_grade_tokens(text: str) -> list[str]:
    cleaned = text.replace(",", " ")
    tokens = [token.strip() for token in cleaned.split() if token.strip()]
    return [normalize_grade_token(token) for token in tokens if normalize_grade_token(token)]


def validate_grades(tokens: Iterable[str]) -> tuple[list[str], str | None]:
    normalized: list[str] = []
    for token in tokens:
        if token not in GRADE_MAP:
            return [], token
        normalized.append(token)
    return normalized, None


def calculate_gpa_from_grades(grades: list[str]) -> float:
    if not grades:
        return 0.0

    total = sum(GRADE_MAP[grade] for grade in grades)
    average = total / len(grades)
    return round(average, 2)


def interpret_gpa(gpa: float) -> str:
    if gpa >= 3.5:
        return "Отлично"
    if gpa >= 3.0:
        return "Хорошо"
    if gpa >= 2.0:
        return "Удовлетворительно"
    return "Нужно подтянуть успеваемость"


def format_grades(grades: list[str]) -> str:
    return ", ".join(grades)
