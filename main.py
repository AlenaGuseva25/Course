import json
import logging

import pandas as pd
from src.utils import set_greeting
from src.utils import set_cards_dicts
from src.utils import set_five_trans_dicts
from src.utils import set_currency_rates_dicts
from src.utils import stock_prices
from src.views import main
from src.reports import get_average_spending_by_weekday
from src.services import analyze_cashback_categories

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main(date_time_str: str, excel_file_path: str) -> str:
    """Главная функция, принимающая дату и время, и возвращающая JSON-ответ"""
    response = {}

    logging.info("Запуск главной функции с параметрами: date_time_str=%s, excel_file_path=%s", date_time_str, excel_file_path)

    response["greeting"] = set_greeting()
    logging.info("Приветствие установлено")

    logging.info("Установка данных по картам из файла: %s", excel_file_path)
    response["cards"] = set_cards_dicts(excel_file_path)
    logging.info("Данные по картам успешно установлены")

    logging.info("Установка топ-5 транзакций")
    response["top_transactions"] = set_five_trans_dicts(excel_file_path)
    logging.info("Топ-5 транзакций успешно установлены")

    logging.info("Установка курсов валют")
    response["currency_rates"] = set_currency_rates_dicts({"currency_rates": []})
    logging.info("Курсы валют успешно установлены")

    logging.info("Получение цен на акции для: ['AAPL', 'GOOGL', 'MSFT']")
    response["stock_prices"] = stock_prices(["AAPL", "GOOGL", "MSFT"])  # Пример акций, можно изменить
    logging.info("Цены на акции успешно получены")

    # Анализ кэшбэка
    logging.info("Чтение транзакций из Excel-файла для анализа кэшбэка")
    transactions_df = pd.read_excel(excel_file_path)  # Чтение транзакций из Excel
    response["cashback_analysis"] = analyze_cashback_categories(transactions_df, 2023, 1)
    logging.info("Анализ кэшбэка завершен")

    # Получение средних трат по дням недели
    logging.info("Получение средних трат по дням недели")
    response["average_spending_by_weekday"] = get_average_spending_by_weekday(transactions_df, date_time_str)
    logging.info("Средние траты по дням недели успешно получены")

    logging.info("Завершение функции, возвращение JSON-ответа")
    return json.dumps(response, ensure_ascii=False, indent=4)