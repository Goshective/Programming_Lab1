import os
import sys


PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH)

from file_utils import FileManager, INPUT_HEADERS

ID_NAME = INPUT_HEADERS[0]
PRODUCTS_NAME = INPUT_HEADERS[1]
ADDRESS_NAME = INPUT_HEADERS[3]
PHONE_NAME = INPUT_HEADERS[4]
PRIORITY_NAME = INPUT_HEADERS[5]


class Validation:
    '''
    Contains functions for validation of address and phone in the orders
    '''
    def is_valid_address(row):
        '''
        Validates address in order 

            Parameters:
                    row (dict[str, str]): order to check

            Returns:
                    address_code (int): 2 if address is wrong, otherwise - 0
                    address_error_string (str): wrong address from order or None if there is no mistakes
        '''
        if not row[ADDRESS_NAME]:
            return 1, "no data"
        parsed_address = row[ADDRESS_NAME].split('. ')
        if len(parsed_address) != 4:
            return 1, row[ADDRESS_NAME]
        return 0, None
    
    def is_valid_phone(row):
        '''
        Validates phone number in order

            Parameters:
                    row (dict[str, str]): order to check

            Returns:
                    phone_code (int): 2 if phone number is wrong, otherwise - 0
                    phone_error_string (str): wrong phone number from order or None if there is no mistakes
        '''
        template = "+x-xxx-xxx-xx-xx"
        phone = row[PHONE_NAME]
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
    '''
    Contains functions to work with orders (sort and update)
    '''
    def generate_products_string(products_amount):
        '''
        Generate simplified string in products column of order 

            Parameters:
                    products_amount (dict[str, int]): distribution of product names

            Returns:
                    res (str): string in format (A x2, B, C x105, e.t.c)
        '''
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
        '''
        Counts distribution of product names and updates row 

            Parameters:
                    row (dict[str, str]): order to update

            Returns:
                    None
        '''
        products_amount = {}
        keys = []
        for product_name in row[PRODUCTS_NAME].split(', '):
            if product_name not in products_amount:
                products_amount[product_name] = 1
                keys.append(product_name)
            else:
                products_amount[product_name] += 1

        row[PRODUCTS_NAME] = OrderParsing.generate_products_string(products_amount)

    def orders_sorting_function(order):
        '''
        Generates possible-to-compare tuple from order data

            Parameters:
                    row (dict[str, str]): order to compare

            Returns:
                    country (str): Country name for lexicographic compare
                    priority (int): Priority of order in terms of (LOW, MIDDLE, MAX)
        '''
        country = order[ADDRESS_NAME].split('. ')[0]
        if country.lower() in ('россия', 'российская федерация'):
            # make the lowest for sorting
            country = "А"
        priorities = {"MAX": 0, "MIDDLE": 1, "LOW": 2}
        priority = priorities[order[PRIORITY_NAME]]
        return (country, priority)


def main():
    '''Manages the main loop of program and calling functions'''

    not_valid_list = []
    orders_list = []
    all_orders_list = FileManager.read_file()
    for row in all_orders_list:
        address_code, address_error_string = Validation.is_valid_address(row)
        if address_code == 1:
            not_valid_list.append((row[ID_NAME], address_code, address_error_string))

        phone_code, phone_error_string = Validation.is_valid_phone(row)
        if phone_code == 2:
            not_valid_list.append((row[ID_NAME], phone_code, phone_error_string))

        elif address_code == 0 and phone_code == 0:
            OrderParsing.update_row_info(row)
            orders_list.append(row)

    orders_list.sort(key=OrderParsing.orders_sorting_function)

    FileManager.write_errors(not_valid_list)
    FileManager.write_orders(orders_list)


if __name__ == "__main__":
    main()