import os
import pandas as pd
import datetime
import logging
from typing import Optional


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
reports_logger = logging.getLogger(__name__)

def report_decorator(file_name=None):
    """Декоратор, который записывает результат функции-отчета в файл"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if file_name:
                file_path = file_name
            else:
                file_path = f"report_{func.__name__}_{datetime.date.today().isoformat()}.csv"
            result.to_csv(file_path, index=True)
            reports_logger.info(f"Отчет сохранен в файл {file_path}")
            return result
        return wrapper
    return decorator


def get_average_spending_by_days(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция вычисляет средние траты за последние 3 месяца от актуальной даты в заданной категории."""

    columns_to_drop = [
        "Дата платежа",
        "Номер карты",
        "Статус",
        "Валюта операции",
        "Сумма платежа",
        "Валюта платежа",
        "Кэшбэк",
        "MCC",
        "Описание",
        "Бонусы (включая кэшбэк)",
        "Округление на инвесткопилку",
        "Сумма операции с округлением",
    ]

    reports_logger.info("Удаление ненужных данных из DataFrame")
    edit_df = transactions.drop(columns=columns_to_drop, errors='ignore')

    reports_logger.info("Преобразование даты транзакции")
    edit_df["Дата операции"] = pd.to_datetime(edit_df["Дата операции"], format="%d.%m.%Y %H:%M:%S",
                                              errors='coerce').dt.date

    reports_logger.info(f"Доступные данные после преобразования: {edit_df.head()}")

    try:
        if date:
            reports_logger.info(f"Используется заданная дата {date}")
            end_date_obj = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S").date()
        else:
            end_date_obj = datetime.datetime.now().date()
            reports_logger.info("Заданная дата не указана, используется текущая дата.")

        start_date_obj = end_date_obj - datetime.timedelta(days=90)
        reports_logger.info(f"Диапазон дат: с {start_date_obj} по {end_date_obj}.")

        report_df = edit_df[
            (edit_df["Дата операции"] <= end_date_obj) &
            (edit_df["Дата операции"] >= start_date_obj) &
            (edit_df["Категория"] == category)
            ]

        reports_logger.info(f"Количество записей в выборке: {len(report_df)}")

        if report_df.empty:
            reports_logger.info("Нет записей для данной категории за указанный период.")
            return pd.DataFrame({})  # Возвращаем пустой DataFrame, если нет записей

        report_df["Дата операции"] = report_df["Дата операции"].astype(str)

    except ValueError as ve:
        reports_logger.error(f"Ошибка в выборке операций: {ve}")
        return pd.DataFrame({})
    except Exception as e:
        reports_logger.error(f"Произошла ошибка: {e}")
        return pd.DataFrame({})

    else:
        reports_logger.info("Выборка операций успешно завершена.")
        return report_df

    finally:
        reports_logger.info("Завершение работы программы.")


def get_average_spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.Series:
    """Функция вычисляет средние траты по дням недели за последние 3 месяца от заданной даты"""

    columns_to_drop = [
        "Дата платежа",
        "Номер карты",
        "Статус",
        "Валюта операции",
        "Сумма платежа",
        "Валюта платежа",
        "Кэшбэк",
        "MCC",
        "Описание",
        "Бонусы (включая кэшбэк)",
        "Округление на инвесткопилку",
        "Сумма операции с округлением",
    ]

    reports_logger.info("Удаление ненужных данных из DataFrame")
    edit_df = transactions.drop(columns=columns_to_drop, errors='ignore')

    reports_logger.info("Преобразование даты транзакции")
    edit_df["Дата операции"] = pd.to_datetime(edit_df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors='coerce')

    # Установка даты
    if date is None:
        end_date_obj = datetime.datetime.now().date()
        reports_logger.info("Дата не указана, используется текущая дата.")
    else:
        try:
            end_date_obj = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S").date()
            reports_logger.info(f"Используемая дата: {end_date_obj}")
        except ValueError as ve:
            reports_logger.error(f"Некорректный формат даты: {ve}")
            raise ValueError("Пожалуйста, введите дату в корректном формате (дд.мм.гггг чч:мм:сс)")

    start_date_obj = end_date_obj - datetime.timedelta(days=90)
    reports_logger.info(f"Диапазон дат: с {start_date_obj} по {end_date_obj}.")

    # Фильтрация по дате
    report_df = edit_df[(edit_df["Дата операции"].dt.date <= end_date_obj) &
                        (edit_df["Дата операции"].dt.date >= start_date_obj)]

    reports_logger.info(f"Количество записей в выборке: {len(report_df)}")

    if report_df.empty:
        reports_logger.info("Нет записей за указанный период.")
        return pd.Series(dtype=float).reindex(range(7)),

    report_df["День недели"] = report_df["Дата операции"].dt.dayofweek  # Пн = 0, Вс = 6
    average_spending = report_df.groupby("День недели")["Сумма операции"].mean().reindex(range(7), fill_value=0)

    reports_logger.info(f"Средние траты по дням недели:\n{average_spending}")
    return average_spending

