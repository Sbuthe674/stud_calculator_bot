from __future__ import annotations

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


def convert_grade_to_gpa(grade: str) -> float:
    grade = grade.strip().upper()
    if grade in GRADE_MAP:
        return GRADE_MAP[grade]

    try:
        value = float(grade)
    except ValueError:
        return 0.0

    if value > 100:
        value = 100.0
    if value < 0:
        value = 0.0

    if value >= 95:
        return 4.0
    if value >= 90:
        return 3.67
    if value >= 85:
        return 3.33
    if value >= 80:
        return 3.0
    if value >= 75:
        return 2.67
    if value >= 70:
        return 2.33
    if value >= 65:
        return 2.0
    if value >= 60:
        return 1.67
    if value >= 55:
        return 1.33
    if value >= 50:
        return 1.0
    return 0.0


def calculate_gpa(subjects: list[tuple[str, float, str]]) -> tuple[float, float, list[str]]:
    total_weight = 0.0
    weighted_points = 0.0
    lines: list[str] = []

    for name, credits, grade in subjects:
        gpa_value = convert_grade_to_gpa(grade)
        weighted_points += gpa_value * credits
        total_weight += credits
        lines.append(f"{name.strip()} — {credits} кр. — {grade.strip()} → {gpa_value}")

    if total_weight == 0:
        return 0.0, 0.0, lines

    final_gpa = round(weighted_points / total_weight, 2)
    return final_gpa, total_weight, lines


def calculate_integral_gpa(
    agpa: float,
    iros: float,
    ssci: float,
    da: float,
    dn: float,
    ds: float,
) -> tuple[float, str]:
    if da < 0 or dn < 0 or ds < 0:
        return 0.0, "Коэффициенты Da, Dn и Ds должны быть неотрицательными."

    weight_sum = da + dn + ds
    if weight_sum == 0:
        return 0.0, "Сумма коэффициентов Da, Dn и Ds должна быть больше нуля."

    normalized_da = da / weight_sum
    normalized_dn = dn / weight_sum
    normalized_ds = ds / weight_sum

    result = normalized_da * agpa + normalized_dn * iros + normalized_ds * ssci
    result = round(result, 2)
    note = (
        f"Коэффициенты нормированы так, чтобы их сумма была 1: Da={normalized_da:.2f}, "
        f"Dn={normalized_dn:.2f}, Ds={normalized_ds:.2f}."
    )
    return result, note


def calculate_average(scores: list[float]) -> tuple[float, float]:
    if not scores:
        return 0.0, 0.0
    average = round(sum(scores) / len(scores), 2)
    percent = round(min(max(average, 0.0), 100.0), 2)
    return average, percent


def calculate_admission_rating(current_score: float, checkpoint_score: float) -> float:
    rating = round((current_score + checkpoint_score) / 2, 2)
    return rating


def calculate_exam_forecast(current_rating: float, target_score: float) -> tuple[float, str]:
    if target_score < 0 or target_score > 100:
        return 0.0, "Желаемый результат должен быть в диапазоне от 0 до 100."

    if current_rating >= target_score:
        return 0.0, "Ваш текущий рейтинг уже позволяет достигнуть желаемой итоговой оценки."

    required = round((target_score - current_rating * 0.6) / 0.4, 2)
    if required > 100:
        return required, (
            "Цель скорее всего недостижима: минимальный балл на экзамене больше 100."
        )
    if required <= 0:
        return 0.0, "Для достижения цели достаточно текущего рейтинга."

    return required, f"Минимально необходимый балл на экзамене: {required}."
