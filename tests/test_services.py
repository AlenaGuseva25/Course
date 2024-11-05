import unittest
import pandas as pd
import json
from src.services import analyze_cashback_categories


class TestAnalyzeCashbackCategories(unittest.TestCase):

    def setUp(self):
        # Общие данные для тестов
        self.transactions_data = {
            "Дата операции": [
                "01.01.2023 10:00:00",
                "15.01.2023 11:30:00",
                "20.01.2023 14:45:00",
                "05.02.2023 09:00:00",
                "10.02.2023 12:30:00",
            ],
            "Категория": ["Еда", "Транспорт", "Развлечения", "Еда", "Транспорт"],
            "Кэшбэк": [100, 50, 200, 150, 75],
        }
        self.transactions_df = pd.DataFrame(self.transactions_data)

    def test_analyze_cashback_categories_success(self):
        # Тест успешного анализа кешбэка
        result = analyze_cashback_categories(self.transactions_df, 2023, 1)
        expected_result = {"Еда": 100, "Транспорт": 50, "Развлечения": 200}
        self.assertEqual(json.loads(result), expected_result)

    def test_analyze_cashback_categories_no_transactions(self):
        # Тест, когда нет транзакций за указанный месяц и год
        result = analyze_cashback_categories(self.transactions_df, 2023, 3)
        expected_result = {}
        self.assertEqual(json.loads(result), expected_result)
