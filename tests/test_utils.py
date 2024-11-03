import logging
import datetime
import unittest
import pytest
import requests
import pandas as pd
from unittest.mock import patch
from freezegun import freeze_time



from src.utils import set_greeting, set_cards_dicts, set_five_trans_dicts, set_currency_rates_dicts, stock_prices

def test_set_greeting_morning():
    with freeze_time("2023-01-01 08:00:00"):
        with patch("logging.info") as mock_logging:
            result = set_greeting()
            assert result == "Доброе утро (Текущая дата и время: 2023-01-01 08:00:00)"
            mock_logging.assert_called_once_with(
                "Текущая дата и время: 2023-01-01 08:00:00. Выбрано приветствие: 'Доброе утро'"
            )

def test_set_greeting_day():
    with freeze_time("2023-01-01 14:00:00"):
        with patch("logging.info") as mock_logging:
            result = set_greeting()
            assert result == "Добрый день (Текущая дата и время: 2023-01-01 14:00:00)"
            mock_logging.assert_called_once_with(
                "Текущая дата и время: 2023-01-01 14:00:00. Выбрано приветствие: 'Добрый день'"
            )

def test_set_greeting_evening():
    with freeze_time("2023-01-01 19:00:00"):
        with patch("logging.info") as mock_logging:
            result = set_greeting()
            assert result == "Добрый вечер (Текущая дата и время: 2023-01-01 19:00:00)"
            mock_logging.assert_called_once_with(
                "Текущая дата и время: 2023-01-01 19:00:00. Выбрано приветствие: 'Добрый вечер'"
            )

def test_set_greeting_night():
    with freeze_time("2023-01-01 02:00:00"):
        with patch("logging.info") as mock_logging:
            result = set_greeting()
            assert result == "Доброй ночи (Текущая дата и время: 2023-01-01 02:00:00)"
            mock_logging.assert_called_once_with(
                "Текущая дата и время: 2023-01-01 02:00:00. Выбрано приветствие: 'Доброй ночи'"
            )


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Номер карты": ["1234567890123456", "1234567890123456", "9876543210123456"],
        "Сумма операции": [100.0, 200.0, 150.0]
    })


def test_set_cards_dicts_no_data(tmp_path):
    excel_file_path = tmp_path / "empty_test_cards.xlsx"
    pd.DataFrame(columns=["Номер карты", "Сумма операции"]).to_excel(excel_file_path, index=False)

    result = set_cards_dicts(str(excel_file_path))

    assert result["total_expenses"] == 0.0
    assert len(result["cards"]) == 0

def test_set_cards_dicts_invalid_file():
    result = set_cards_dicts("invalid_file_path.xlsx")

    assert "error" in result
    assert result["error"] == "Ошибка чтения файла"


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"Error: {self.status_code}")

class TestSetCurrencyRatesDicts(unittest.TestCase):

    @patch('src.utils.requests.get')
    @patch('src.utils.logging')
    def test_set_currency_rates_dicts_success(self, mock_logging, mock_get):
        # Настройка фиктивного ответа для USD
        mock_get.side_effect = [
            MockResponse({"rates": {"RUB": 74.0}}, 200),  # Ответ для USD
            MockResponse({"rates": {"RUB": 88.0}}, 200)   # Ответ для EUR
        ]

        # Подготовка входных данных
        info_currency = {"currency_rates": []}

        # Вызов тестируемой функции
        result = set_currency_rates_dicts(info_currency)

        # Проверка результатов
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {"currency": "USD", "rate": 74.0})
        self.assertEqual(result[1], {"currency": "EUR", "rate": 88.0})
        mock_logging.info.assert_called_with("Курсы валют успешно получены.")

    @patch('src.utils.requests.get')
    @patch('src.utils.logging')
    def test_set_currency_rates_dicts_error_usd(self, mock_logging, mock_get):
        # Настройка фиктивного ответа для USD с ошибкой
        mock_get.side_effect = [
            MockResponse({}, 500),  # Ошибка для USD
            MockResponse({"rates": {"RUB": 88.0}}, 200)  # Ответ для EUR
        ]

        # Подготовка входных данных
        info_currency = {"currency_rates": []}

        # Вызов тестируемой функции
        result = set_currency_rates_dicts(info_currency)

        # Проверка результатов
        self.assertEqual(result, [])
        mock_logging.error.assert_called_with("Ошибка получения курсов валют.")

    @patch('src.utils.requests.get')
    @patch('src.utils.logging')
    def test_set_currency_rates_dicts_error_eur(self, mock_logging, mock_get):
        # Настройка фиктивного ответа для USD
        mock_get.side_effect = [
            MockResponse({"rates": {"RUB": 74.0}}, 200),  # Ответ для USD
            MockResponse({}, 200)  # Ошибка для EUR
        ]

        # Подготовка входных данных
        info_currency = {"currency_rates": []}

        # Вызов тестируемой функции
        result = set_currency_rates_dicts(info_currency)

        # Проверка результатов
        self.assertEqual(result, None)
        mock_logging.error.assert_called_with("Ошибка в ответе для EUR: %s", {})

if __name__ == '__main__':
    unittest.main()