import sys
import os
import unittest

PATH = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(PATH, '..', '..')
sys.path.insert(0, src_dir)

from src.lab4.main import (
    Validation,
    OrderParsing
)


class OrdersTestCase(unittest.TestCase):

    def test_valid_address(self):
        valid_func = Validation.is_valid_address

        self.assertIsNone(valid_func({'Адрес доставки': 'A. B. C. D.'})[1])
        
        self.assertEqual(valid_func({'Адрес доставки': 'A.B. C. D.'})[0], 1)
        
        self.assertEqual(valid_func({'Адрес доставки': 'A. B. D.'})[0], 1)
        
        self.assertEqual(valid_func({'Адрес доставки': ''})[1], 'no data')

    def test_valid_phone(self):
        valid_func = Validation.is_valid_phone

        self.assertIsNone(valid_func({'Номер телефона': '+0-000-000-00-00'})[1])
        
        self.assertEqual(valid_func({'Номер телефона': '+0-000-000-9999'})[0], 2)
        
        self.assertEqual(valid_func({'Номер телефона': '8-000-000-00-00'})[0], 2)
        
        self.assertEqual(valid_func({'Номер телефона': '+7 000 000 00 00'})[0], 2)
        
        self.assertEqual(valid_func({'Номер телефона': ''})[1], 'no data')

    def test_generate_products_string(self):
        parse_func = OrderParsing.generate_products_string

        self.assertEqual(parse_func(dict()), '')

        self.assertEqual(parse_func({'A': 1}), 'A')

        self.assertEqual(parse_func({'A': 2}), 'A x2')

        self.assertEqual(parse_func({'A': 1, 'B': 1}), 'A, B')

        self.assertEqual(parse_func({'A': 3, 'B': 12}), 'A x3, B x12')

    def test_simplify_products_string_in_order(self):
        parse_func = OrderParsing.update_row_info

        row = {'Набор продуктов': 'A'}
        parse_func(row)
        self.assertEqual(row, {'Набор продуктов': 'A'})

        row = {'Набор продуктов': 'A, B, A, B, B'}
        parse_func(row)
        self.assertEqual(row, {'Набор продуктов': 'A x2, B x3'})

        row = {'Набор продуктов': 'A, B, A, B, B'}
        parse_func(row)
        self.assertEqual(row, {'Набор продуктов': 'A x2, B x3'})

    def test_products_sorting_function(self):
        sort_func = OrderParsing.orders_sorting_function

        row1 = {'Адрес доставки': 'Россия', 'Приоритет доставки': 'LOW'}
        row2 = {'Адрес доставки': 'Россия', 'Приоритет доставки': 'MIDDLE'}
        self.assertTrue(sort_func(row1) > sort_func(row2))

        row1 = {'Адрес доставки': 'Россия', 'Приоритет доставки': 'MIDDLE'}
        row2 = {'Адрес доставки': 'Россия', 'Приоритет доставки': 'MAX'}
        self.assertTrue(sort_func(row1) > sort_func(row2))

        row1 = {'Адрес доставки': 'Россия', 'Приоритет доставки': 'LOW'}
        row2 = {'Адрес доставки': 'Не Россия', 'Приоритет доставки': 'LOW'}
        self.assertTrue(sort_func(row1) < sort_func(row2))

        row1 = {'Адрес доставки': 'Россия', 'Приоритет доставки': 'LOW'}
        row2 = {'Адрес доставки': 'Не Россия', 'Приоритет доставки': 'MAX'}
        self.assertTrue(sort_func(row1) < sort_func(row2))

        row1 = {'Адрес доставки': 'Российская федерация', 'Приоритет доставки': 'LOW'}
        row2 = {'Адрес доставки': 'Не Россия', 'Приоритет доставки': 'MAX'}
        self.assertTrue(sort_func(row1) < sort_func(row2))

        row1 = {'Адрес доставки': 'Англия', 'Приоритет доставки': 'LOW'}
        row2 = {'Адрес доставки': 'Япония', 'Приоритет доставки': 'MAX'}
        self.assertTrue(sort_func(row1) < sort_func(row2))



if __name__ == "__main__":
    unittest.main()