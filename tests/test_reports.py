import unittest
from unittest.mock import patch
import pandas as pd
import datetime
from src.reports import get_average_spending_by_weekday


class TestGetAverageSpendingByWeekday(unittest.TestCase):

    def setUp(self):
        self.transactions_data = {
            "Дата операции": ["01.01.2023 10:00:00", "02.01.2023 11:30:00", "03.01.2023 14:45:00",
                             "04.01.2023 09:00:00", "05.01.2023 12:30:00", "06.01.2023 15:00:00"],
            "Сумма операции": [100, 200, 150, 300, 250, 400],
        }
        self.transactions_df = pd.DataFrame(self.transactions_data)

    def test_get_average_spending_by_weekday_success(self):
        user_date = "06.01.2023 15:00:00"
        result = get_average_spending_by_weekday(self.transactions_df, user_date)

        # Ожидаемое значение: средние траты по дням недели
        expected_average = pd.Series([100.0, 200.0, 150.0, 300.0, 250.0, 400.0, 0.0], index=range(7))
        pd.testing.assert_series_equal(result, expected_average)

    # Остальные тесты остаются без изменений

if __name__ == '__main__':
    unittest.main()