def calculate_average(scores):
    return round(sum(scores) / len(scores), 2)


def calculate_average_with_percent(scores):
    average = calculate_average(scores)
    if all(score <= 5 for score in scores):
        percent = round(average * 20, 2)
    elif all(score <= 10 for score in scores):
        percent = round(average * 10, 2)
    else:
        percent = round(average, 2)

    return average, percent
