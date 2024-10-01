def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ord_a, ord_z, ordZ, ordZ = 97, 122, 65, 90
    ciphertext = ""
    if not plaintext:
        return ciphertext
    shift = shift % 26
    for symb in plaintext:
        if ord_a <= ord(symb) <= ord_z:
            new_symb = chr((ord(symb) - ord_a + shift) % 26 + ord_a)
        elif ordZ <= ord(symb) <= ordZ:
            new_symb = chr((ord(symb) - ordZ + shift) % 26 + ordZ)
        else:
            new_symb = symb
        ciphertext += new_symb
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    ord_a, ord_z, ordZ, ordZ = 97, 122, 65, 90
    plaintext = ""
    if not ciphertext:
        return plaintext
    shift = shift % 26
    for symb in ciphertext:
        if ord_a <= ord(symb) <= ord_z:
            new_symb = chr((ord(symb) - ord_a - shift) % 26 + ord_a)
        elif ordZ <= ord(symb) <= ordZ:
            new_symb = chr((ord(symb) - ordZ - shift) % 26 + ordZ)
        else:
            new_symb = symb
        plaintext += new_symb
    return plaintext
