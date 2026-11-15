
GRADE_POINTS = {
    "A+": 4.3,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "E": 0.5,
    "F": 0.0
}


def calculate_gpa(grades, credits):
    total_points = 0
    total_credits = 0

    for grade, credit in zip(grades, credits):
        total_points += grade * credit
        total_credits += credit

    if total_credits == 0:
        return 0

    return round(total_points / total_credits, 3)


def convert_grades(letter_grades):
    return [GRADE_POINTS[grade] for grade in letter_grades]


if __name__ == "__main__":
    letter_grades = ["A", "B+", "A-"]
    credits = [3, 3, 3]

    grades = convert_grades(letter_grades)
    gpa = calculate_gpa(grades, credits)

    print("Your GPA is:", gpa)

