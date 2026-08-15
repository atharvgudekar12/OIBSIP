def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)


def get_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"