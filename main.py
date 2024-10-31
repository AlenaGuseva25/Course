from src.utils import set_greeting
from src.utils import set_cards_dicts
from src.utils import set_five_trans_dicts
from src.utils import set_currency_rates_dicts

if __name__ == "__main__":
    greeting_message = set_greeting()
    print(greeting_message)

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