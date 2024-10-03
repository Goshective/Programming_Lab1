import sys
import os
import unittest

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, '../..', 'src')
    sys.path.insert(0, src_dir)

    from lab2.vigenre import encrypt_vigenere, decrypt_vigenere


class VigenereTestCase(unittest.TestCase):

    def test_basic_encryption(self):
        self.assertEqual(encrypt_vigenere('', ''), "")
        self.assertEqual(encrypt_vigenere('aaaaaaaaa', 'aaabbbaaa'), "aaabbbaaa")
        self.assertEqual(encrypt_vigenere('aaabbbccc', 'abc'), "abcbcdcde")
        self.assertEqual(encrypt_vigenere('aaa', 'bbaabbaa'), "bba")
        self.assertEqual(encrypt_vigenere('abcdefg', 'abcdefg'), "acegikm")
        self.assertEqual(encrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(encrypt_vigenere("python", "a"), "python")
        self.assertEqual(encrypt_vigenere("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")
    
    def test_basic_decryption(self):
        self.assertEqual(decrypt_vigenere(encrypt_vigenere('', ''), ''), "")
        self.assertEqual(decrypt_vigenere(encrypt_vigenere('aaaaaaaaa', 'aaabbbaaa'), 'aaabbbaaa'), 'aaaaaaaaa')
        self.assertEqual(decrypt_vigenere('abcbcdcde', 'abc'), "aaabbbccc")
        self.assertEqual(decrypt_vigenere('bba', 'bbaabbaa'), "aaa")
        self.assertEqual(decrypt_vigenere('acegikm', 'abcdefg'), "abcdefg")
        self.assertEqual(decrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(decrypt_vigenere("python", "a"), "python")
        self.assertEqual(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")

    def test_extended_encryption(self):
        self.assertEqual(encrypt_vigenere('aaarrraaa', 'aaa999bbb'), "aaarrrbbb")
        self.assertEqual(encrypt_vigenere('ab100', ''), "ab100")
        self.assertEqual(encrypt_vigenere('ab_200', 'bb_cde'), "bc_200")
        self.assertEqual(encrypt_vigenere('ab_300', 'yz'), "ya_300")
        self.assertEqual(encrypt_vigenere('aaarrraaa', '100'), "aaarrraaa")

    def test_extended_decryption(self):
        self.assertEqual(decrypt_vigenere('aaarrrbbb', 'aaa999bbb'), "aaarrraaa")
        self.assertEqual(decrypt_vigenere('ab100', ''), "ab100")
        self.assertEqual(decrypt_vigenere('bc_200', 'bb_cde'), "ab_200")
        self.assertEqual(decrypt_vigenere('ya_300', 'yz'), "ab_300")
        self.assertEqual(decrypt_vigenere('aaarrraaa', '100'), "aaarrraaa")

if __name__ == "__main__":
    unittest.main()