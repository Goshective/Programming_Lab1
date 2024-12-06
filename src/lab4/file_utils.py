import os
import csv


INPUT_FILENAME = "orders.txt"
OUPUT_FILENAME = "order_country.txt"
ERROR_FILENAME = "non_valid_orders.txt"
PATH = os.path.dirname(os.path.abspath(__file__))


class FileManager:
    def read_file():
        with open(os.path.join(PATH, INPUT_FILENAME), 'r', encoding='utf-8') as input_file:
            # Номер заказа, Набор продуктов, ФИО заказчика, Адрес доставки, Номер телефона, Приоритет доставки
            reader = csv.DictReader(input_file, delimiter=";")
            all_orders_list = []
            for row in reader:
                all_orders_list.append(row)
            
            return all_orders_list
        
    def write_errors(not_valid_list):
        with open(os.path.join(PATH, ERROR_FILENAME), 'w', encoding='utf-8') as out_file:
            headers = ['Номер заказа', 'Тип ошибки', 'Значение атрибута с ошибкой']
            writer = csv.DictWriter(out_file, fieldnames=headers, delimiter=';')

            writer.writeheader()
            for row in not_valid_list:
                writer.writerow({'Номер заказа': row[0], 
                                 'Тип ошибки': row[1], 
                                 'Значение атрибута с ошибкой': row[2]}
                                 )

    def write_orders(parsed_orders_list):
        with open(os.path.join(PATH, OUPUT_FILENAME), 'w', encoding='utf-8') as out_file:
            headers = ['Номер заказа', 'Набор продуктов', 'ФИО заказчика', 'Адрес доставки', 'Номер телефона', 'Приоритет доставки']
            writer = csv.DictWriter(out_file, fieldnames=headers, delimiter=';')

            writer.writeheader()
            for row in parsed_orders_list:
                writer.writerow(row)