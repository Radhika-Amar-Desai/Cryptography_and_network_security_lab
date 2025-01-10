import socket

# S-DES functions
def permute(block, table):
    return [block[i - 1] for i in table]

def key_schedule(key):
    p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    p8 = [6, 3, 7, 4, 8, 5, 10, 9]

    key = permute(key, p10)
    left, right = key[:5], key[5:]

    def left_shift(bits, count):
        return bits[count:] + bits[:count]

    left = left_shift(left, 1)
    right = left_shift(right, 1)
    key1 = permute(left + right, p8)

    left = left_shift(left, 2)
    right = left_shift(right, 2)
    key2 = permute(left + right, p8)

    return key1, key2

def fk(subkey, block):
    ep = [4, 1, 2, 3, 2, 3, 4, 1]
    s0 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2],
    ]
    s1 = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3],
    ]
    p4 = [2, 4, 3, 1]

    left, right = block[:4], block[4:]
    right_expanded = permute(right, ep)
    xor_result = [r ^ k for r, k in zip(right_expanded, subkey)]

    def sbox(input_bits, sbox):
        row = int(f"{input_bits[0]}{input_bits[3]}", 2)
        col = int(f"{input_bits[1]}{input_bits[2]}", 2)
        return [int(x) for x in f"{sbox[row][col]:02b}"]

    left_sbox = sbox(xor_result[:4], s0)
    right_sbox = sbox(xor_result[4:], s1)
    sbox_output = permute(left_sbox + right_sbox, p4)

    return [l ^ s for l, s in zip(left, sbox_output)] + right

def encrypt_decrypt(block, keys, encrypt=True):
    ip = [2, 6, 3, 1, 4, 8, 5, 7]
    ip_inv = [4, 1, 3, 5, 7, 2, 8, 6]

    block = permute(block, ip)
    if encrypt:
        block = fk(keys[0], block)
        block = block[4:] + block[:4]
        block = fk(keys[1], block)
    else:
        block = fk(keys[1], block)
        block = block[4:] + block[:4]
        block = fk(keys[0], block)

    return permute(block, ip_inv)

# Networking
def server():
    host = 'localhost'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Server is listening...")
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            data = conn.recv(1024).decode()
            action, plaintext, key = data.split(',')
            plaintext = [int(x) for x in plaintext]
            key = [int(x) for x in key]

            keys = key_schedule(key)
            if action == 'encrypt':
                result = encrypt_decrypt(plaintext, keys, encrypt=True)
            else:
                result = encrypt_decrypt(plaintext, keys, encrypt=False)

            conn.send(','.join(map(str, result)).encode())

if __name__ == "__main__":
    server()
