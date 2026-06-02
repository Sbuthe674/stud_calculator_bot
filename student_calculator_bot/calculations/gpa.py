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
    "F": 0.0
}


def percent_to_gpa(percent):

    percent = float(percent)

    if percent >= 95:
        return 4.0

    elif percent >= 90:
        return 3.67

    elif percent >= 85:
        return 3.33

    elif percent >= 80:
        return 3.0

    elif percent >= 75:
        return 2.67

    elif percent >= 70:
        return 2.33

    elif percent >= 65:
        return 2.0

    elif percent >= 60:
        return 1.67

    elif percent >= 55:
        return 1.33

    elif percent >= 50:
        return 1.0

    return 0.0


def convert_grade(grade):

    grade = grade.strip().upper()

    if grade.replace(".", "").isdigit():
        return percent_to_gpa(float(grade))

    return GRADE_MAP.get(grade, 0)
