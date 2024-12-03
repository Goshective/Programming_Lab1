"""Номер заказа;Набор прродуктов;ФИО заказчика;Адрес доставки;Номер телефона;Приоритет доставки

31987;Сыр, Колбаса, Сыр, Макароны, Колбаса;Петрова Анна;Россия. Ленинградская область. Санкт-Петербург. набережная реки Фонтанки;+7-921-456-78-90;MIDDLE

87459;Молоко, Яблоки, Хлеб, Яблоки, Молоко;Иванов Иван Иванович;Россия. Московская область. Москва. улица Пушкина;+7-912-345-67-89;MAX

31987;Сыр, Колбаса, Макароны, Сыр, Колбаса;Петрова Анна Сергеевна;Франция. Иль-де-Франс. Париж. Шанз-Элизе;+3-214-020-50-50;MIDDLE

56342;Хлеб, Молоко, Хлеб, Молоко;Смирнова Мария Леонидовна;Германия. Бавария. Мюнхен. Мариенплац;+4-989-234-56;LOW (невалидный номер телефона)

48276;Яблоки, Макароны, Яблоки;Алексеев Алексей Алексеевич;Италия. Лацио. Рим. Колизей;+3-061-234-56-78;MAX

65829;Сок, Вода, Сок, Вода;Белова Екатерина Михайловна;Испания. Каталония. Барселона. Рамбла;+34-93-1234-567;LOW (невалидный номер телефона)

72901;Чай, Кофе, Чай, Кофе;Михайлов Сергей Петрович;Великобритания. Англия. Лондон. Бейкер-стрит;+4-207-946-09-58;LOW

84756;Печенье, Сыр, Печенье, Сыр;Васильева Анна Владимировна;Япония. Шибуя. Шибуя-кроссинг;+8-131-234-5678;MAX (невалидный адрес доставки и номер телефона)

90385;Макароны, Сыр, Макароны, Сыр;Николаев Николай;;+1-416-123-45-67;LOW (невалидный адрес доставки)"""


import os
import csv
from typing import Tuple, Set, List


INPUT_FILENAME = "orders.txt"
OUPUT_FILENAME = "order_country.txt"
PATH = os.path.dirname(os.path.abspath(__file__))


class Utils:
    def is_valid_address(row):
        if not row['Адрес доставки']:
            return 1, "no data"
        parsed_address = row['Адрес доставки'].split('. ')
        if len(parsed_address) != 4:
            return 1, row['Адрес доставки']
        return 0, None
    
    def is_valid_phone(row):
        template = "+x-xxx-xxx-xx-xx"
        phone = row['Номер телефона']
        if len(phone) == 0:
            return 2, "no data"
        if len(phone) != len(template):
            return 2, phone

        for i in range(len(template)):
            if template[i] in ('+', '-') and phone[i] != template[i]:
                return 2, phone
            elif template[i] == 'x' and not phone[i].isnumeric():
                return 2, phone
        return 0, None
        
    def parse_row(row):
        pass

    def main_read_file():
        with open(os.path.join(PATH, INPUT_FILENAME), 'r', encoding='utf-8') as input_file:
            # Номер заказа, Набор прродуктов, ФИО заказчика, Адрес доставки, Номер телефона, Приоритет доставки
            reader = csv.DictReader(input_file, delimiter=";")
            not_valid_list = []
            orders_list = []
            for row in reader:
                address_code, address_error_string = Utils.is_valid_address(row)
                if address_code == 1:
                    not_valid_list.append((row['Номер заказа'], address_error_string))

                phone_code, phone_error_string = Utils.is_valid_phone(row)
                if phone_code == 2:
                    not_valid_list.append((row['Номер заказа'], phone_error_string))

                if address_code == 0 and phone_code == 0:
                    orders_list.append(row)
            
            return not_valid_list, orders_list


def main():
    not_valid_list, orders_list = Utils.main_read_file()
    print(not_valid_list)
    print(orders_list)

if __name__ == "__main__":
    main()