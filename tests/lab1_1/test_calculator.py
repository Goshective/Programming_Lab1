import unittest
from src.lab1_1.calculator import parse_to_polish, calculate_polish
# import sys

# def parse_to_polish(s):
#     return True, ['+']
# def calculate_polish(l):
#     return True, ['+']

class CalculatorTestCase(unittest.TestCase):

    def test_incorrect_symbols(self):
        self.assertFalse(parse_to_polish('abcdefg')[0])
        self.assertFalse(parse_to_polish('=_[]{}<>?')[0])
    
    def test_incorrect_math_expression_1(self):
        self.assertFalse(parse_to_polish('10 + 30 20')[0])
        self.assertFalse(parse_to_polish('0.1 + 0.0.1')[0])
        self.assertFalse(parse_to_polish('0.1 + .01')[0])
        self.assertFalse(parse_to_polish('17.6 * 3^(12/3 - 0) + ((1 - 2) + 66/6))')[0])

        self.assertTrue(parse_to_polish('-1 + (-2)')[0])
        self.assertTrue(parse_to_polish('10 + 3020')[0])
        self.assertTrue(parse_to_polish('0.1 + (-0.1)')[0])

    def test_incorrect_math_expression_2(self):
        self.assertFalse(calculate_polish(parse_to_polish('1++2++3++4')[1])[0])
        self.assertFalse(calculate_polish(parse_to_polish('13*-6+')[1])[0])
        self.assertFalse(calculate_polish(parse_to_polish('(3 + 5) * 10 - 17*2+-+-+-((()())()()())')[1])[0])

        self.assertEqual(calculate_polish(parse_to_polish('(3 + 5) * 10 - 17*2')[1])[1], 46)
        self.assertEqual(calculate_polish(parse_to_polish('1+5-6+9')[1])[1], 9)
        self.assertEqual(round(calculate_polish(parse_to_polish('17.6 * 3^(12/3 - 0) + ((1 - 2) + 66/6)')[1])[1], 1), 1435.6)
        self.assertEqual(calculate_polish(parse_to_polish('10-1-2-3-4-(0-1-2-3-4)+(0-1-2-3-4)')[1])[1], 0)
        self.assertEqual(calculate_polish(parse_to_polish('0-1-2-3-4')[1])[1], -10)
        self.assertEqual(calculate_polish(parse_to_polish('-1 - 2-3 -4')[1])[1], -10)

if __name__ == "__main__":
    unittest.main()