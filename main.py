if __name__ == "__main__":
    greeting_message = set_greeting()
    print(greeting_message)

if __name__ == "__main__":
    excel_file_path = (r"C:\Users\Alena\my_1\Course_paper\data\operations.xlsx")

    summary = set_cards_dicts(excel_file_path)
    print(summary)

if __name__ == "__main__":
    excel_file_path = r"C:\Users\Alena\my_1\Course_paper\data\operations.xlsx"
    top_5 = set_five_trans_dicts(excel_file_path)  # Получаем только ТОП 5 транзакций
    print("ТОП 5 транзакций:", top_5)  # Выводим ТОП 5 транзакций