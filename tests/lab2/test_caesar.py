import sys
import os
import unittest


class CaesarTestCase(unittest.TestCase):

    def test_basic_encryption(self):
        self.assertEqual(encrypt_caesar(''), "")
        self.assertEqual(encrypt_caesar('abcdefg'), "defghij")
        self.assertEqual(encrypt_caesar('yz', 0), "yz")
        self.assertEqual(encrypt_caesar('yz', 1), "za")
        self.assertEqual(encrypt_caesar('ab', -2), "yz")
    
    def test_basic_decryption(self):
        self.assertEqual(decrypt_caesar(''), "")
        self.assertEqual(decrypt_caesar('defghij'), "abcdefg")
        self.assertEqual(decrypt_caesar('yz', 0), "yz")
        self.assertEqual(decrypt_caesar('za', 1), "yz")
        self.assertEqual(decrypt_caesar('yz', -2), "ab")

    def test_extended_encryption(self):
        self.assertEqual(encrypt_caesar('1_+=()*&^%'), "1_+=()*&^%")
        self.assertEqual(encrypt_caesar('ab100', 0), "ab100")
        self.assertEqual(encrypt_caesar('ab_200', 1), "bc_200")
        self.assertEqual(encrypt_caesar('ab_300', -2), "yz_300")

    def test_extended_decryption(self):
        self.assertEqual(decrypt_caesar('1_+=()*&^%'), "1_+=()*&^%")
        self.assertEqual(decrypt_caesar('ab100', 0), "ab100")
        self.assertEqual(decrypt_caesar('bc_200', 1), "ab_200")
        self.assertEqual(decrypt_caesar('yz_300', -2), "ab_300")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, '../..', 'src')
    sys.path.insert(0, src_dir)

    from lab2.caesar import encrypt_caesar, decrypt_caesar
    unittest.main()