from DES_constants import IP, EXPANSION_BOX, STRAIGHT_PERM, S_BOX, FINAL_PERM, keyp, shift_table, key_comp 

def hex2bin(s):
    return ''.join(f"{int(c, 16):04b}" for c in s)

def bin2hex(s):
    return ''.join(f"{int(s[i:i+4], 2):X}" for i in range(0, len(s), 4))

def bin2dec(binary):
    return int(str(binary), 2)

def dec2bin(num):
    res = bin(num)[2:]  # Convert to binary and remove '0b' prefix
    return res.zfill((len(res) + 3) // 4 * 4)  # Pad to the nearest multiple of 4

def permute(k, arr, n):
    return ''.join(k[arr[i] - 1] for i in range(n))

def shift_left(k, nth_shifts):
    return k[nth_shifts:] + k[:nth_shifts]

def xor(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))

def encrypt(pt, rkb, rk):
    pt = hex2bin(pt)

    # Initial Permutation
    pt = permute(pt, IP, 64)
    #print("After initial permutation", bin2hex(pt))

    # Splitting
    left, right = pt[:32], pt[32:]

    for i in range(16):
        # Expansion D-box: Expanding 32 bits into 48 bits
        right_expanded = permute(right, EXPANSION_BOX, 48)

        # XOR with RoundKey[i]
        xor_x = xor(right_expanded, rkb[i])

        # S-box substitution
        sbox_str = ''.join(
            dec2bin(S_BOX[j][bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))]
                           [bin2dec(int(xor_x[j * 6 + 1:j * 6 + 5]))])
            for j in range(8)
        )

        sbox_str = permute(sbox_str, STRAIGHT_PERM, 32)

        left = xor(left, sbox_str)

        if i != 15:
            left, right = right, left

        #print(f"Round {i + 1}: {bin2hex(left)} {bin2hex(right)} {rk[i]}")

    cipher_text = permute(left + right, FINAL_PERM, 64)
    return cipher_text

def des_encrypt(pt, key):
    # Convert key to binary
    key = hex2bin(key)

    # Initial key permutation (56-bit)
    key = permute(key, keyp, 56)

    # Splitting key into two halves
    left, right = key[:28], key[28:]

    # Generate 16 round keys
    rkb, rk = [], []
    for i in range(16):
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])

        # Combine left and right halves
        combine_str = left + right

        # Permute to get round key (48-bit)
        round_key = permute(combine_str, key_comp, 48)

        rkb.append(round_key)
        rk.append(bin2hex(round_key))

    # Encrypt the plaintext
    cipher_text = bin2hex(encrypt(pt, rkb, rk))
    
    return cipher_text

def des_decrypt(ciphertext, key):
    key_bin = hex2bin(key)
    key_bin = permute(key_bin, keyp, 56)

    # Splitting key
    left = key_bin[0:28]
    right = key_bin[28:56]

    # Generate round keys in reverse order
    rkb = []
    rk = []
    for i in range(16):
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])
        combine_str = left + right
        round_key = permute(combine_str, key_comp, 48)
        rkb.append(round_key)
        rk.append(bin2hex(round_key))

    # Reverse round keys for decryption
    rkb.reverse()
    rk.reverse()

    plaintext = bin2hex(encrypt(ciphertext, rkb, rk))
    return plaintext
