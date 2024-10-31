import json
import os
import datetime
import logging
import requests
from dotenv import load_dotenv
logger = logging.getLogger(__name__)


load_dotenv()
api_key = os.getenv("API_KEY")

import pandas as pd


def set_greeting() -> str:
    """Функция формирует строку приветствия и вносит значение по ключу greeting"""
    current_hour = datetime.datetime.now().hour
    greeting = ""

    if 0 <= current_hour < 6:
        greeting = "Доброй ночи"
    elif 6 <= current_hour < 12:
        greeting = "Доброе утро"
    elif 12 <= current_hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    logging.info(f"Текущее время: {current_hour} часов. Выбрано приветствие: '{greeting}'")

    return greeting


def set_cards_dicts(exsel_file_path):
    """Функция формирует словарь по картам пользователя и вносит значение по ключу cards"""
    logging.info("Обработка файла: %d", exsel_file_path)

    try:
        df = pd.read_excel(exsel_file_path)
        logging.info("Файл прочитан. Найдено %d строк.", len(df))
    except Exception as e:
        logging.error("Ошибка чтения файла: %d", e)
        return {"error": "Ошибка чтения файла"}

    cards_summary = []
    total_expenses = 0.0

    for index, row in df.iterrows():
        try:
            last_digits = str(row["Номер карты"])[-4:]
            total_spent = float(row["Сумма операции"])
            cashback = total_spent / 100.0

            cards_info = {
                "last_digits": last_digits,
                "total_spent": total_spent,
                "cashback": cashback
            }

            cards_summary.append(cards_info)
            total_expenses += total_spent
            logging.debug("Добавлена информация о карте: %d", cards_info)


        except KeyError as e:
            logging.error("Ошибка: отсутствует столбец %s в строке %d", e, index)
        except Exception as e:
            logging.error("Ошибка при обработке строки %d: %s", index, e)


    logging.info("Обработка завершена. Найдено %d карт.", len(cards_summary))
    return {"cards": cards_summary, "total_expenses" : total_expenses}



def set_five_trans_dicts(excel_file_path):
    """Функция формирует ТОП 5 словарей (по сумме платежа) по ключу top_transactions"""
    df = pd.read_excel(excel_file_path)

    top5_transactions = []

    for index, row in df.iterrows():
        date = str(row["Дата платежа"])
        amount = float(row["Сумма операции"])
        category = str(row["Категория"])
        description = str(row["Описание"])

        info_top5 = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        top5_transactions.append(info_top5)

    top5_transactions = sorted(top5_transactions, key=lambda x: x["amount"], reverse=True)[:5]

    return top5_transactions


def set_currency_rates_dicts(info_currency):
    """Функция курса валют, формирует словари по ключу currency_rates_dicts"""
    try:
        logger.info("Запрос курсов валют USD и EUR...")

        api_key = os.getenv("API_KEY")
        headers_curr = {"apikey": api_key}

        url_usd = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD"
        result_usd = requests.get(url_usd, headers=headers_curr)
        result_usd.raise_for_status()
        new_amount_usd = result_usd.json()

        url_eur = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=EUR"
        result_eur = requests.get(url_eur, headers=headers_curr)
        result_eur.raise_for_status()
        new_amount_eur = result_eur.json()

        if 'rates' in new_amount_usd and 'RUB' in new_amount_usd['rates']:
            info_currency["currency_rates"].append({
                "currency": "USD",
                "rate": new_amount_usd['rates']['RUB']
            })
        else:
            logger.error("Ошибка в ответе для USD: %s", new_amount_usd)
            return None

        if 'rates' in new_amount_eur and 'RUB' in new_amount_eur['rates']:
            info_currency["currency_rates"].append({
                "currency": "EUR",
                "rate": new_amount_eur['rates']['RUB']
            })
        else:
            logger.error("Ошибка в ответе для EUR: %s", new_amount_eur)
            return None

        logger.info("Курсы валют успешно получены.")
        return info_currency

    except Exception as e:
        logger.error("Everybody has problems with currency now...")
        print(f"We have a problem with currency, Watson: {e}")



def set_stock_prices_dicts():
    """Функция стоимости акций, формирует словари по ключу stock_prices"""
    pass