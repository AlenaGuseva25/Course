import logging
import pandas as pd
import requests
import os
import datetime
import json

from src.utils import set_greeting, set_cards_dicts, set_five_trans_dicts, set_currency_rates_dicts, stock_prices

exsel_file_path = (r"C:\Users\Alena\my_1\Course_paper\data\operations.xlsx")


def main(date_time_str: str, excel_file_path: str) -> str:
    """Главная функция, принимающая дату и время, и возвращающая JSON-ответ"""
    response = {}

    # Установка приветствия
    response["greeting"] = set_greeting()

    # Получение информации о картах
    response["cards"] = set_cards_dicts(excel_file_path)

    # Получение топ-5 транзакций
    response["top_transactions"] = set_five_trans_dicts(excel_file_path)

    # Получение курсов валют
    response["currency_rates"] = set_currency_rates_dicts({"currency_rates": []})

    # Получение цен акций
    response["stock_prices"] = stock_prices()

    # Преобразование в JSON
    return json.dumps(response, ensure_ascii=False, indent=4)

