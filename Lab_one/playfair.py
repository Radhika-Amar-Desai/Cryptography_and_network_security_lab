def generate_key_square(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = "".join(dict.fromkeys(key.upper().replace("J", "I")))  # Remove duplicates
    key_square = key + "".join([ch for ch in alphabet if ch not in key])
    return [key_square[i:i + 5] for i in range(0, 25, 5)]

def find_position(key_square, char):
    for i, row in enumerate(key_square):
        if char in row:
            return i, row.index(char)

def playfair_cipher_encrypt(text, key):
    key_square = generate_key_square(key)
    text = text.upper().replace("J", "I")
    text = "".join([char for char in text if char.isalpha()])
    pairs = [text[i:i + 2] if i + 1 < len(text) else text[i] + "X"
             for i in range(0, len(text), 2)]

    encrypted_text = ""
    for a, b in pairs:
        row1, col1 = find_position(key_square, a)
        row2, col2 = find_position(key_square, b)
        if row1 == row2:
            encrypted_text += key_square[row1][(col1 + 1) % 5] + key_square[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += key_square[(row1 + 1) % 5][col1] + key_square[(row2 + 1) % 5][col2]
        else:
            encrypted_text += key_square[row1][col2] + key_square[row2][col1]
    return encrypted_text

# Example usage:
key = "KEYWORD"
text = "HELLO"
encrypted = playfair_cipher_encrypt(text, key)
print(f"Encrypted: {encrypted}")
