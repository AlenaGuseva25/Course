import pandas as pd
import json
import datetime


def analyze_cashback_categories(transactions, year, month):
    """Анализ выгодности категорий повышенного кешбэка"""
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    filtered_data = transactions[(transactions["Дата операции"].dt.year == year) & (transactions["Дата операции"].dt.month == month)]

    cashback_by_category = filtered_data.groupby("Категория")["Кэшбэк"].sum()

    analysis = {}
    for category, cashback in cashback_by_category.items():
        analysis[category] = cashback

    return json.dumps(analysis, ensure_ascii=False)

