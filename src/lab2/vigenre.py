def shift_symb_caesar(symb: str, shift: int = 0) -> str:
    """
    Shifts symbol using a Caesar cipher rules.
    """
    ord_a, ord_z, ordA, ordZ = 97, 122, 65, 90
    if not symb:
        return ''
    shift = shift % 26
    if ord_a <= ord(symb) <= ord_z:
        return chr((ord(symb) - ord_a + shift) % 26 + ord_a)
    if ordA <= ord(symb) <= ordZ:
        return chr((ord(symb) - ordA + shift) % 26 + ordA)
    return symb


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    if not keyword or not plaintext:
        return plaintext
    key_shift = [ord(s.lower()) - ord('a') if ord('a') <= ord(s.lower()) <= ord('z') else 0 for s in keyword]
    mod_shift = len(key_shift)
    for i, symb in enumerate(plaintext):
        shift = key_shift[i % mod_shift]
        ciphertext += shift_symb_caesar(symb, shift)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    if not keyword or not ciphertext:
        return ciphertext
    key_shift = [ord(s.lower()) - ord('a') if ord('a') <= ord(s.lower()) <= ord('z') else 0 for s in keyword]
    mod_shift = len(key_shift)
    for i, symb in enumerate(ciphertext):
        shift = key_shift[i % mod_shift]
        plaintext += shift_symb_caesar(symb, -shift)
    return plaintext
