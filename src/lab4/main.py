import os
import csv


INPUT_FILENAME = "orders.txt"
OUPUT_FILENAME = "order_country.txt"
ERROR_FILENAME = "non_valid_orders.txt"
PATH = os.path.dirname(os.path.abspath(__file__))


class Validation:
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


class OrderParsing:
    def generate_products_string(products_amount):
        res = []
        product_names = products_amount.keys()
        for name in sorted(product_names):
            product_number = products_amount[name]
            if product_number == 1:
                res.append(name)
            else:
                res.append(f'{name} x{product_number}')
        
        return ", ".join(res)
        

    def update_row_info(row):
        products_amount = {}
        keys = []
        for product_name in row['Набор продуктов'].split(', '):
            if product_name not in products_amount:
                products_amount[product_name] = 1
                keys.append(product_name)
            else:
                products_amount[product_name] += 1

        row['Набор продуктов'] = OrderParsing.generate_products_string(products_amount)

    def orders_sorting_function(product):
        country = product['Адрес доставки'].split('. ')[0]
        if country.lower() in ('россия', 'российская федерация'):
            # make the lowest for sorting
            country = "А"
        priorities = {"MAX": 0, "MIDDLE": 1, "LOW": 2}
        priority = priorities[product['Приоритет доставки']]
        return (country, priority)
        



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


def main():
    not_valid_list = []
    orders_list = []
    all_orders_list = FileManager.read_file()
    for row in all_orders_list:
        address_code, address_error_string = Validation.is_valid_address(row)
        if address_code == 1:
            not_valid_list.append((row['Номер заказа'], address_code, address_error_string))

        phone_code, phone_error_string = Validation.is_valid_phone(row)
        if phone_code == 2:
            not_valid_list.append((row['Номер заказа'], phone_code, phone_error_string))

        elif address_code == 0 and phone_code == 0:
            OrderParsing.update_row_info(row)
            orders_list.append(row)

    orders_list.sort(key=OrderParsing.orders_sorting_function)

    FileManager.write_errors(not_valid_list)
    FileManager.write_orders(orders_list)


if __name__ == "__main__":
    main()