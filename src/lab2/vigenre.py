def shift_symb_caesar(symb: str, shift: int = 0) -> str:
    """
    Shifts symbol using a Caesar cipher rules.
    """
    ord_a, ord_z, ord_A, ord_Z = 97, 122, 65, 90
    if not symb:
        return ''
    shift = shift % 26
    if ord_a <= ord(symb) <= ord_z:
        return chr((ord(symb) - ord_a + shift) % 26 + ord_a)
    elif ord_A <= ord(symb) <= ord_Z:
        return chr((ord(symb) - ord_A + shift) % 26 + ord_A)
    else:
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
        return ciphertext
    key_shift = [ord(s.lower()) - ord('a') for s in keyword]
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
    if not keyword or not plaintext:
        return ciphertext
    key_shift = [ord(s.lower()) - ord('a') for s in keyword]
    mod_shift = len(key_shift)
    for i, symb in enumerate(ciphertext):
        shift = key_shift[-i % mod_shift]
        plaintext += shift_symb_caesar(symb, shift)
    return plaintext