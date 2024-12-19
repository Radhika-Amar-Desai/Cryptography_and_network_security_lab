def caesar_cipher_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def caesar_cipher_decrypt(cipher_text, shift):
    return caesar_cipher_encrypt(cipher_text, -shift)

# Example usage:
text = "HELLO WORLD"
shift = 3
encrypted = caesar_cipher_encrypt(text, shift)
decrypted = caesar_cipher_decrypt(encrypted, shift)
print(f"Encrypted: {encrypted}, Decrypted: {decrypted}")
