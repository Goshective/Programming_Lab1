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


if __name__ == "__main__":
    unittest.main()