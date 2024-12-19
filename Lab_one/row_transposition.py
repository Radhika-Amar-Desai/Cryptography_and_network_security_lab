def row_transposition_encrypt(text, key):
    key_order = sorted(list(key))
    columns = {k: [] for k in key}
    for i, char in enumerate(text):
        columns[key[i % len(key)]].append(char)
    encrypted = ""
    for k in key_order:
        encrypted += "".join(columns[k])
    return encrypted

# Example usage:
text = "HELLOWORLD"
key = "3142"
encrypted = row_transposition_encrypt(text, key)
print(f"Encrypted: {encrypted}")
