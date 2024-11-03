import pandas as pd
from src.utils import set_greeting
from src.utils import set_cards_dicts
from src.utils import set_five_trans_dicts
from src.utils import set_currency_rates_dicts
from src.utils import stock_prices
from src.views import main
from src.reports import get_average_spending_by_weekday
from src.services import analyze_cashback_categories

#if __name__ == "__main__":
 #   greeting_message = set_greeting()
  #  print(greeting_message)

#if __name__ == "__main__":
 #   excel_file_path = (r"C:\Users\Alena\my_1\Course_paper\data\operations.xlsx")
#
 #   summary = set_cards_dicts(excel_file_path)
  #  print(summary)

#if __name__ == "__main__":
 #   excel_file_path = r"C:\Users\Alena\my_1\Course_paper\data\operations.xlsx"
  #  top_5 = set_five_trans_dicts(excel_file_path)
   # print("ТОП 5 транзакций:", top_5)


#if __name__ == "__main__":
 #   info_currency = {"currency_rates": []}
  #  currency_info = set_currency_rates_dicts(info_currency)
   # print(currency_info)

#if __name__ == "__main__":
 #   updated_stock_info = stock_prices(stock_info)
  #  print(updated_stock_info)

#if __name__ == "__main__":
#    date_time_input = "2023-10-01 12:30:00"
#    excel_file_path = (r"C:\Users\Alena\my_1\Course_paper\data\operations.xlsx")
#    result_json = main(date_time_input, excel_file_path)
#   print(result_json)

excel_file_path = r"C:\Users\Alena\my_1\Course_paper\data\operations.xlsx"

transactions = pd.read_excel(excel_file_path)

#if __name__ == "__main__":
 #   category = "Супермаркеты"
  #  average_spending_report = get_average_spending_by_days(transactions, category)
   # print(average_spending_report)


#if __name__ == "__main__":
 #   average_spending_per_weekday = get_average_spending_by_weekday(transactions, "01.10.2021 00:00:00")
  #  print("Средние траты по дням недели:")
   # print(average_spending_per_weekday)

#if __name__ == "__main__":
 #   average_spending = get_average_spending_by_weekday(transactions)
  #  print("Средние траты по дням недели за последние 3 месяца:")
   # print(average_spending)

if __name__ == "__main__":
    year = 2021
    month = 12
    analysis = analyze_cashback_categories(transactions, year, month)
    print("Анализ кешбэка по категориям:")
    print(analysis)