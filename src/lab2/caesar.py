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
    # list(map(chr, range(ord('a'), ord('z')+1)))
    alph = "abcdefghijklmnopqrstuvwxyz"
    alph_idx = {s: i for i, s in enumerate(alph)}
    ciphertext = ""
    if not plaintext:
        return ciphertext
    shift = shift % 26
    for symb in plaintext:
        if symb.lower() in alph_idx:
            new_symb = alph[(alph_idx[symb.lower()] + shift) % 26]
            ciphertext += new_symb if symb.islower() else new_symb.upper()
        else:
            ciphertext += symb
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
    alph = "abcdefghijklmnopqrstuvwxyz"
    alph_idx = {s: i for i, s in enumerate(alph)}
    plaintext = ""
    if not ciphertext:
        return plaintext
    shift = shift % 26
    for symb in ciphertext:
        if symb.lower() in alph_idx:
            new_symb = alph[(alph_idx[symb.lower()] - shift) % 26]
            plaintext += new_symb if symb.islower() else new_symb.upper()
        else:
            plaintext += symb
    return plaintext