import unittest
import pandas as pd
from src.reports import get_average_spending_by_weekday


class TestGetAverageSpendingByWeekday(unittest.TestCase):

    def setUp(self):
        self.transactions_data = {
            "Дата операции": [
                "01.01.2023 10:00:00",
                "02.01.2023 11:30:00",
                "03.01.2023 14:45:00",
                "04.01.2023 09:00:00",
                "05.01.2023 12:30:00",
                "06.01.2023 15:00:00",
            ],
            "Сумма операции": [100, 200, 150, 300, 250, 400],
            "Номер карты": ["1234", "5678", "1234", "5678", "1234", "5678"],
            "Статус": ["Успешно", "Успешно", "Успешно", "Успешно", "Успешно", "Успешно"],
            "Валюта операции": ["RUB", "RUB", "RUB", "RUB", "RUB", "RUB"],
            "Кэшбэк": [10, 20, 15, 30, 25, 40],
            "MCC": ["123", "456", "789", "123", "456", "789"],
            "Описание": ["Покупка", "Покупка", "Покупка", "Покупка", "Покупка", "Покупка"],
            "Бонусы (включая кэшбэк)": [5, 10, 7, 15, 12, 20],
            "Округление на инвесткопилку": [0, 0, 0, 0, 0, 0],
            "Сумма платежа": [100, 200, 150, 300, 250, 400],
            "Валюта платежа": ["RUB", "RUB", "RUB", "RUB", "RUB", "RUB"],
        }
        self.transactions_df = pd.DataFrame(self.transactions_data)

    def test_get_average_spending_by_weekday_no_transactions(self):
        # Тест, когда нет транзакций за указанный период
        empty_data = {
            "Дата операции": [],
            "Сумма операции": [],
            "Номер карты": [],
            "Статус": [],
            "Валюта операции": [],
            "Кэшбэк": [],
            "MCC": [],
            "Описание": [],
            "Бонусы (включая кэшбэк)": [],
            "Округление на инвесткопилку": [],
            "Сумма платежа": [],
            "Валюта платежа": [],
        }
        empty_df = pd.DataFrame(empty_data)
        user_date = "06.01.2023 15:00:00"

        result = get_average_spending_by_weekday(empty_df, user_date)
        expected_average = (pd.Series(dtype=float).reindex(range(7)),)  # Пустая серия
        pd.testing.assert_series_equal(result[0], expected_average[0])

    def test_get_average_spending_by_weekday_invalid_date_format(self):
        # Тест некорректного формата даты
        user_date = "invalid_date_format"

        with self.assertRaises(ValueError) as context:
            get_average_spending_by_weekday(self.transactions_df, user_date)





