import pandas as pd
import json


def analyze_cashback_categories(transactions, year, month):
    """Анализ выгодности категорий повышенного кешбэка"""
    try:
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    except Exception as e:
        raise ValueError("Ошибка при преобразовании даты: " + str(e))

    filtered_data = transactions[
        (transactions["Дата операции"].dt.year == year) & (transactions["Дата операции"].dt.month == month)
    ]

    if filtered_data.empty:
        return json.dumps({}, ensure_ascii=False)

    cashback_by_category = filtered_data.groupby("Категория")["Кэшбэк"].sum()

    analysis = cashback_by_category.to_dict()

    return json.dumps(analysis, ensure_ascii=False)
