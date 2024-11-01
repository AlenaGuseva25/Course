from typing import Dict, List, Any
import os
import datetime
import logging
import requests
import pandas as pd
from dotenv import load_dotenv
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


load_dotenv()
api_key = os.getenv("API_KEY")

exsel_file_path = (r"C:\Users\Alena\my_1\Course_paper\data\operations.xlsx")


def set_greeting() -> str:
    """Функция формирует строку приветствия и логирует текущее время и дату"""
    current_time = datetime.datetime.now()  # Получаем текущее время и дату
    current_hour = current_time.hour
    greeting = ""

    if 0 <= current_hour < 6:
        greeting = "Доброй ночи"
    elif 6 <= current_hour < 12:
        greeting = "Доброе утро"
    elif 12 <= current_hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    logging.info(
        f"Текущая дата и время: {current_time.strftime('%Y-%m-%d %H:%M:%S')}. Выбрано приветствие: '{greeting}'")

    result_message: str = f"{greeting} (Текущая дата и время: {current_time.strftime('%Y-%m-%d %H:%M:%S')})"

    return result_message


def set_cards_dicts(excel_file_path: str) -> Dict[str, Any]:
    """Функция формирует словарь по картам пользователя и вносит значение по ключу cards"""
    logging.info("Обработка файла: %s", excel_file_path)

    try:
        df = pd.read_excel(excel_file_path)
        logging.info("Файл прочитан. Найдено %d строк.", len(df))
    except Exception as e:
        logging.error("Ошибка чтения файла: %s", e)
        return {"error": "Ошибка чтения файла"}

    cards_summary: Dict[str, Dict[str, Any]] = {}

    for index, row in df.iterrows():
        try:
            last_digits = str(row["Номер карты"])[-4:]
            total_spent = float(row["Сумма операции"])

            if last_digits in cards_summary:
                cards_summary[last_digits]["total_spent"] += total_spent
                cards_summary[last_digits]["cashback"] += total_spent / 100.0
            else:
                cards_summary[last_digits] = {
                    "last_digits": last_digits,
                    "total_spent": total_spent,
                    "cashback": total_spent / 100.0
                }

            logging.debug("Обновлена информация о карте: %s", cards_summary[last_digits])

        except KeyError as e:
            logging.error("Ошибка: отсутствует столбец %s в строке %d", e, index)
        except Exception as e:
            logging.error("Ошибка при обработке строки %d: %s", index, e)

    if cards_summary:
        first_card = next(iter(cards_summary.values()))
        return {
            "cards": [first_card],
            "total_expenses": first_card["total_spent"]
        }
    else:
        return {
            "cards": [],
            "total_expenses": 0.0
        }


def set_five_trans_dicts(excel_file_path: str) -> List[Dict[str, Any]]:
    """Функция формирует ТОП 5 словарей (по сумме платежа) по ключу top_transactions"""
    try:
        df = pd.read_excel(excel_file_path)

        required_columns = ["Дата платежа", "Сумма операции", "Категория", "Описание"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Отсутствуют необходимые столбцы в данных")

        transactions = df[required_columns].copy()
        transactions["Сумма операции"] = transactions["Сумма операции"].astype(float)

        top5_transactions = transactions.nlargest(5, "Сумма операции")

        result = [
            {
                "date": row["Дата платежа"].strftime("%d.%m.%Y") if isinstance(row["Дата платежа"], pd.Timestamp) else
                str(row["Дата платежа"]),
                "amount": round(row["Сумма операции"], 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
            for index, row in top5_transactions.iterrows()
        ]

        return result

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


def set_currency_rates_dicts(info_currency: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Функция курса валют, формирует словари по ключу currency_rates"""
    try:
        logging.info("Запрос курсов валют USD и EUR...")

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
            logging.error("Ошибка в ответе для USD: %s", new_amount_usd)
            return None

        if 'rates' in new_amount_eur and 'RUB' in new_amount_eur['rates']:
            info_currency["currency_rates"].append({
                "currency": "EUR",
                "rate": new_amount_eur['rates']['RUB']
            })
        else:
            logging.error("Ошибка в ответе для EUR: %s", new_amount_eur)
            return None

        logging.info("Курсы валют успешно получены.")
        return info_currency["currency_rates"]

    except Exception as e:
        logging.error("Ошибка получения курсов валют.")
        print(f"Проблема с курсами валют: {e}")
        return []


def stock_prices() -> List[Dict[str, Any]]:
    """Функция стоимости акций, формирует словари по ключу stock_prices"""
    info_stocks = {"stock_prices": []}
    try:
        logging.info("Получение информации о ценах на акции")

        data_json = {
            "data": {
                "trends": [
                    {"name": "AAPL", "price": 150.12},
                    {"name": "AMZN", "price": 3173.18},
                    {"name": "GOOGL", "price": 2742.39},
                    {"name": "MSFT", "price": 296.71},
                    {"name": "TSLA", "price": 1007.08},
                ]
            }
        }

        info_stocks["stock_prices"] = [
            {"stock": trend["name"], "price": trend["price"]}
            for trend in data_json["data"]["trends"]
        ]

        return info_stocks["stock_prices"]

    except Exception as e:
        logging.error("Ошибка при получении цен на акции.")
        print(f"Проблема с акциями: {e}")
        return []
