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
    ciphertext = ""
    ord_A = ord("A")
    ord_a = ord("a")
    alph_len = 26
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                shifted_char = chr((ord(char) - ord_A + shift) % alph_len + ord_A)
            else:
                shifted_char = chr((ord(char) - ord_a + shift) % alph_len + ord_a)
            ciphertext += shifted_char
        else:
            ciphertext += char
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
    plaintext = ""
    ord_A = ord("A")
    ord_a = ord("a")
    alph_len = 26
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                shifted_char = chr((ord(char) - ord_A - shift) % alph_len + ord_A)
            else:
                shifted_char = chr((ord(char) - ord_a - shift) % alph_len + ord_a)
            plaintext += shifted_char
        else:
            plaintext += char
    return plaintext
