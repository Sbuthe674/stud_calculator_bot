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


def percent_to_gpa(percent):
    percent = float(percent)
    if percent >= 95:
        return 4.0
    if percent >= 90:
        return 3.67
    if percent >= 85:
        return 3.33
    if percent >= 80:
        return 3.0
    if percent >= 75:
        return 2.67
    if percent >= 70:
        return 2.33
    if percent >= 65:
        return 2.0
    if percent >= 60:
        return 1.67
    if percent >= 55:
        return 1.33
    if percent >= 50:
        return 1.0
    return 0.0


def convert_grade(grade):
    grade = grade.strip().upper()
    if grade.replace(".", "").isdigit():
        return percent_to_gpa(float(grade))
    return GRADE_MAP.get(grade, 0.0)


def calculate_gpa(subjects):
    total_credits = sum(credit for _, credit in subjects)
    if total_credits <= 0:
        return 0.0, 0

    weighted_points = sum(convert_grade(score) * credit for score, credit in subjects)
    gpa = round(weighted_points / total_credits, 2)
    return gpa, total_credits
