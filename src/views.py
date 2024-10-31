import json

from src.utils import set_greeting, set_cards_dicts, set_five_trans_dicts, set_currency_rates_dicts, stock_prices

exsel_file_path = (r"C:\Users\Alena\my_1\Course_paper\data\operations.xlsx")


def main(date_time_str: str, excel_file_path: str) -> str:
    """Главная функция, принимающая дату и время, и возвращающая JSON-ответ"""
    response = {}

    response["greeting"] = set_greeting()

    response["cards"] = set_cards_dicts(excel_file_path)

    response["top_transactions"] = set_five_trans_dicts(excel_file_path)

    response["currency_rates"] = set_currency_rates_dicts({"currency_rates": []})

    response["stock_prices"] = stock_prices()

    return json.dumps(response, ensure_ascii=False, indent=4)
