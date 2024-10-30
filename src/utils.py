import datetime
import logging
import json


def set_greeting() -> str:
    """Функция формирует строку приветствия и вносит значение по ключу greeting"""
    current_hour = datetime.datetime.now().hour

    if 0 <= current_hour < 6:
        greeting = "Доброй ночи"
    elif 6 <= current_hour < 12:
        greeting = "Доброе утро"
    elif 12 <= current_hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    return greeting


if __name__ == "__main__":
    greeting_message = set_greeting()
    print(greeting_message)




def set_cards_dicts():
    """Функция формирует словарь по картам пользователя и вносит значение по ключу cards"""
    pass


def set_five_trans_dicts():
    """Функция формирует ТОП 5 словарей (по сумме платежа) по ключу top_transactions"""
    pass


def set_currency_rates_dicts():
    """Функция курса валют, формирует словари по ключу currency_rates_dicts"""
    pass


def set_stock_prices_dicts():
    """Функция стоимости акций, формирует словари по ключу stock_prices"""
    pass