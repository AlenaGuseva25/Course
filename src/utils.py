import datetime
import logging
import json
import pandas as pd
from pathlib import Path


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
            logging.debug("Добавлена информация о карте: %d", cards_info)


        except KeyError as e:
            logging.error("Ошибка: отсутствует столбец %s в строке %d", e, index)
        except Exception as e:
            logging.error("Ошибка при обработке строки %d: %s", index, e)


    logging.info("Обработка завершена. Найдено %d карт.", len(cards_summary))
    return {"cards": cards_summary}



def set_five_trans_dicts(excel_file_path):
    """Функция формирует ТОП 5 словарей (по сумме платежа) по ключу top_transactions"""
    df = pd.read_excel(excel_file_path)

    top5_transactions = []

    # Сбор всех транзакций в список
    for index, row in df.iterrows():
        date = str(row["Дата платежа"])  # Используем правильное название столбца
        amount = float(row["Сумма операции"])  # Используем правильное название столбца
        category = str(row["Категория"])  # Используем правильное название столбца
        description = str(row["Описание"])  # Используем правильное название столбца

        info_top5 = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        top5_transactions.append(info_top5)

    # Сортировка транзакций по сумме и выбор ТОП 5
    top5_transactions = sorted(top5_transactions, key=lambda x: x["amount"], reverse=True)[:5]

    return top5_transactions










def set_currency_rates_dicts():
    """Функция курса валют, формирует словари по ключу currency_rates_dicts"""
    pass


def set_stock_prices_dicts():
    """Функция стоимости акций, формирует словари по ключу stock_prices"""
    pass