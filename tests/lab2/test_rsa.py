import sys
import os
import unittest


class RSATestCase(unittest.TestCase):

    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(97))
        self.assertTrue(is_prime(15331))
        self.assertTrue(is_prime(309121))

        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(2021))
        self.assertFalse(is_prime(309121**2))
    
    def test_gcd(self):
        self.assertEqual(gcd(1, 1), 1)
        self.assertEqual(gcd(2, 1), 1)
        self.assertEqual(gcd(1, 2), 1)
        self.assertEqual(gcd(15, 3), 3)
        self.assertEqual(gcd(81, 90), 9)
        self.assertEqual(gcd(15331*2, 309121**2), 1)

    def test_multiplicative_inverse(self):
        self.assertEqual(multiplicative_inverse(7, 40), 23)
        self.assertEqual(multiplicative_inverse(3, 11), 4)
        self.assertEqual(multiplicative_inverse(2, 157), 79)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, '../..', 'src')
    sys.path.insert(0, src_dir)

    from lab2.rsa import is_prime, gcd, multiplicative_inverse
    unittest.main()