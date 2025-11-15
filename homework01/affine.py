def encrypt_affine(plaintext, a, b):
    ciphertext = ""
    m = 33
    for char in plaintext:
        if char.isalpha():
            changed_char = chr((a * ord(char) + b) % m)
            ciphertext += changed_char
        else:
            ciphertext += char
    return ciphertext
