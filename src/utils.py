import datetime
import logging
import json
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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


if __name__ == "__main__":
    greeting_message = set_greeting()
    print(greeting_message)


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


if __name__ == "__main__":
    excel_file_path = (r"C:\Users\Alena\my_1\Course_paper\data\operations.xlsx")

    summary = set_cards_dicts(excel_file_path)
    print(summary)







def set_five_trans_dicts():
    """Функция формирует ТОП 5 словарей (по сумме платежа) по ключу top_transactions"""
    pass


def set_currency_rates_dicts():
    """Функция курса валют, формирует словари по ключу currency_rates_dicts"""
    pass


def set_stock_prices_dicts():
    """Функция стоимости акций, формирует словари по ключу stock_prices"""
    pass