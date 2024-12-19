def vigenere_cipher_encrypt(text, key):
    key = key.upper()
    key_repeated = (key * ((len(text) // len(key)) + 1))[:len(text)]
    encrypted = ""
    for t, k in zip(text, key_repeated):
        if t.isalpha():
            shift = ord(k) - 65
            shift_base = 65 if t.isupper() else 97
            encrypted += chr((ord(t) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted += t
    return encrypted

# Example usage:
text = "HELLO WORLD"
key = "KEY"
encrypted = vigenere_cipher_encrypt(text, key)
print(f"Encrypted: {encrypted}")
