from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {
    "I": "Income",
    "E": "Expense",
}


def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Неверный формат даты. Пожалуйста, введите дату в формате DD-MM-YYYY.")
        return get_date(prompt, allow_default)


def get_amount():
    try:
        amount = float(input("Введите сумму: "))
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля")
        return amount
    except ValueError:
        print("Неверный формат суммы. Пожалуйста, введите число.")
        return get_amount()


def get_category():
    category = input("Введите категорию ('I' - доход, 'E' - расход): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Неверный формат категории. Пожалуйста, введите 'I' или 'E'.")
    return get_category()


def get_description():
    return input("Введите описание (необязательно): ")
