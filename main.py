import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description, date_format
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Запись успешно добавлена!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE, parse_dates=["date"], date_format="%d-%m-%Y")
        df["date"] = pd.to_datetime(df["date"], format=date_format)
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask].sort_values("date")

        if filtered_df.empty:
            print("Нет транзакций за указанный период.")
        else:
            print()
            print(
                f"Транзакции за период с {start_date.strftime(date_format)} по {end_date.strftime(date_format)}:"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(date_format)}
                )
            )
            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()
            print("\nИтого:")
            print(f"Доход: {total_income:.2f}")
            print(f"Расход: {total_expense:.2f}")
            print(f"Итого баланс: {(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Введите дату в формате DD-MM-YYYY: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 6))
    plt.plot(income_df.index, income_df["amount"], label="Доход", color="green")
    plt.plot(expense_df.index, expense_df["amount"], label="Расход", color="red")
    plt.xlabel("Дата")
    plt.ylabel("Сумма")
    plt.title("График доходов и расходов")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\nВыберите действие:")
        print("1. Добавить транзакцию")
        print("2. Получить список транзакций за период")
        print("3. Выход")

        choice = input("Введите номер действия(1/2/3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Введите начальную дату в формате DD-MM-YYYY: ")
            end_date = get_date("Введите конечную дату в формате DD-MM-YYYY: ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Показать график? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 3.")


if __name__ == "__main__":
    main()
