import pandas as pd
import datetime
import logging
from typing import Optional


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
reports_logger = logging.getLogger(__name__)


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

