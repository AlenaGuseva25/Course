import json
import logging
from src.utils import filter_data, group_by_category

def analyze_cashback(data: pd.DataFrame, year: int, month: int) -> str:
    """Анализирует кешбэк по категориям"""
    filtered_data = filter_data(data, year, month)
    cashback_by_category = group_by_category(filtered_data)
    cashback_json = json.dumps(cashback_by_category, ensure_ascii=False)
    return cashback_json