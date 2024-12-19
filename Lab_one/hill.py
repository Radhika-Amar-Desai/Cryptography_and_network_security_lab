import numpy as np

def hill_cipher_encrypt(text, key_matrix):
    n = len(key_matrix)
    text_vector = [ord(char) - 65 for char in text.upper()]
    text_vector += [0] * (n - len(text_vector) % n)
    encrypted = ""
    for i in range(0, len(text_vector), n):
        block = np.dot(key_matrix, text_vector[i:i + n]) % 26
        encrypted += "".join(chr(int(num) + 65) for num in block)
    return encrypted

# Example usage:
key_matrix = np.array([[2, 3], [1, 4]])  # Example 2x2 matrix
text = "ACT"
encrypted = hill_cipher_encrypt(text, key_matrix)
print(f"Encrypted: {encrypted}")
