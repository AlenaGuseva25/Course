import json
import pytest
from unittest.mock import patch
from src.views import main

def test_main():
    date_time_str = "2023-10-10T10:00:00"
    excel_file_path = "path/to/excel_file.xlsx"

    with patch('src.views.set_greeting') as mock_set_greeting, \
            patch('src.views.set_cards_dicts') as mock_set_cards, \
            patch('src.views.set_five_trans_dicts') as mock_set_five_trans, \
            patch('src.views.set_currency_rates_dicts') as mock_set_currency_rates, \
            patch('src.views.stock_prices') as mock_stock_prices:

        mock_set_greeting.return_value = "Hello, User!"
        mock_set_cards.return_value = [{"id": 1, "name": "Card A"}, {"id": 2, "name": "Card B"}]
        mock_set_five_trans.return_value = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
        mock_set_currency_rates.return_value = {"USD": 1.0, "EUR": 0.85}
        mock_stock_prices.return_value = [{"stock": "AAPL", "price": 145.0}, {"stock": "MSFT", "price": 250.0}]

        result = main(date_time_str, excel_file_path)

        expected_response = {
            "greeting": "Hello, User!",
            "cards": [{"id": 1, "name": "Card A"}, {"id": 2, "name": "Card B"}],
            "top_transactions": [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}],
            "currency_rates": {"USD": 1.0, "EUR": 0.85},
            "stock_prices": [{"stock": "AAPL", "price": 145.0}, {"stock": "MSFT", "price": 250.0}]
        }

        # Преобразуем в JSON
        expected_json = json.dumps(expected_response, ensure_ascii=False, indent=4)

        # Сравниваем результат с ожидаемым
        assert result == expected_json

def test_main_without_cards():
    date_time_str = "2023-10-10T10:00:00"
    excel_file_path = "path/to/excel_file.xlsx"

    with patch('src.views.set_greeting') as mock_set_greeting, \
            patch('src.views.set_cards_dicts') as mock_set_cards, \
            patch('src.views.set_five_trans_dicts') as mock_set_five_trans, \
            patch('src.views.set_currency_rates_dicts') as mock_set_currency_rates, \
            patch('src.views.stock_prices') as mock_stock_prices:

        mock_set_greeting.return_value = "Hello, User!"
        mock_set_cards.return_value = []  # Пустой список карт
        mock_set_five_trans.return_value = [{"id": 1, "amount": 100}]
        mock_set_currency_rates.return_value = {"USD": 1.0, "EUR": 0.85}
        mock_stock_prices.return_value = [{"stock": "AAPL", "price": 145.0}]

        result = main(date_time_str, excel_file_path)

        expected_response = {
            "greeting": "Hello, User!",
            "cards": [],
            "top_transactions": [{"id": 1, "amount": 100}],
            "currency_rates": {"USD": 1.0, "EUR": 0.85},
            "stock_prices": [{"stock": "AAPL", "price": 145.0}]
        }

        expected_json = json.dumps(expected_response, ensure_ascii=False, indent=4)

        assert result == expected_json