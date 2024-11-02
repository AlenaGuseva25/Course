import logging
import datetime
import unittest
import pytest
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

def test_set_cards_dicts_valid_data(sample_data, tmp_path):
    # Создайте временный Excel файл для тестов
    excel_file_path = tmp_path / "test_cards.xlsx"
    sample_data.to_excel(excel_file_path, index=False)

    result = set_cards_dicts(str(excel_file_path))

    # Исправьте ожидаемое количество карт
    assert result["total_expenses"] == 450.0  # Убедитесь, что сумма трат корректная
    assert len(result["cards"]) == 1  # У вас одна карта с суммарными расходами 300
    assert result["cards"][0]["last_digits"] == "3456"  # Последние цифры карты
    assert result["cards"][0]["total_spent"] == 300.0
    assert result["cards"][0]["cashback"] == 3.0

def test_set_cards_dicts_no_data(tmp_path):
    # Создайте пустой Excel файл
    excel_file_path = tmp_path / "empty_test_cards.xlsx"
    pd.DataFrame(columns=["Номер карты", "Сумма операции"]).to_excel(excel_file_path, index=False)

    result = set_cards_dicts(str(excel_file_path))

    assert result["total_expenses"] == 0.0
    assert len(result["cards"]) == 0

def test_set_cards_dicts_invalid_file():
    result = set_cards_dicts("invalid_file_path.xlsx")

    assert "error" in result
    assert result["error"] == "Ошибка чтения файла"