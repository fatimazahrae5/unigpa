
def calculate_gpa(grades, credits):
    total_points = 0
    total_credits = 0

    for grade, credit in zip(grades, credits):
        total_points += grade * credit
        total_credits += credit

    if total_credits == 0:
        return 0

    return round(total_points / total_credits, 3)


# Example student grades
grades = [3.0, 3.7, 4.0]
credits = [3, 3, 3]

gpa = calculate_gpa(grades, credits)

print("Your GPA is:", gpa)
