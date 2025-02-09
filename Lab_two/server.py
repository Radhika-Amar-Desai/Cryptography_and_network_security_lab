# Function to ensure the bit sequence is the correct length
def ensure_length(bits, length):
    return bits + [0] * (length - len(bits))

# Expansion table (E) for DES
E = [
    31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10,
    11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28,
    29, 30, 31, 0
]

# Initial permutation (IP) table for DES
IP = [
    57, 49, 41, 33, 25, 17, 9, 1, 
    58, 50, 42, 34, 26, 18, 10, 2, 
    59, 51, 43, 35, 27, 19, 11, 3, 
    60, 52, 44, 36, 28, 20, 12, 4, 
    61, 53, 45, 37, 29, 21, 13, 5, 
    62, 54, 46, 38, 30, 22, 14, 6, 
    63, 55, 47, 39, 31, 23, 15, 7
]

# Inverse initial permutation (IP^-1) for DES
IP_inv = [
    40, 8, 48, 16, 56, 24, 64, 32, 
    39, 7, 47, 15, 55, 23, 62, 31, 
    38, 6, 46, 14, 54, 22, 61, 30, 
    37, 5, 45, 13, 53, 21, 60, 29, 
    36, 4, 44, 12, 52, 20, 59, 28, 
    35, 3, 43, 11, 51, 19, 58, 27, 
    34, 2, 42, 10, 50, 18, 57, 26
]

# Function to perform the initial permutation (IP)
def initial_permutation(bits):
    return permute(bits, IP)

# Function to perform the inverse initial permutation (IP^-1)
def inverse_initial_permutation(bits):
    return permute(bits, IP_inv)

# Permutation function
def permute(bits, table):
    bits = ensure_length(bits, max(table) + 1)  # Ensure the list is long enough
    return [bits[i] for i in table]

# XOR function
def xor(bits1, bits2):
    return [bit1 ^ bit2 for bit1, bit2 in zip(bits1, bits2)]

# S-boxes for DES (Substitution boxes)
S_BOXES = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 16, 5, 3, 10, 6, 12, 9, 0],
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 8, 3],
        [7, 11, 13, 14, 3, 12, 9, 0, 15, 5, 1, 10, 6, 8, 4, 2]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 7, 15, 10, 1, 13, 9, 0, 5, 11, 14, 2, 8, 12, 4, 6],
        [14, 6, 3, 8, 13, 12, 7, 9, 0, 10, 1, 4, 11, 15, 2, 5],
        [7, 3, 11, 13, 10, 15, 14, 8, 5, 9, 0, 12, 6, 2, 4, 1]
    ],
    # Additional S-boxes can be added as needed
]

# Function to apply the round function
def round_function(right, subkey):
    expanded = permute(right, E)  # Apply expansion
    return xor(expanded, subkey)

# DES encryption function
def des_encrypt(plaintext, key):
    # Ensure both input and key are in the correct length (64 bits each)
    key = [int(bit) for bit in key]
    plaintext = [int(bit) for bit in plaintext]
    
    # Make sure both are 64 bits
    plaintext = ensure_length(plaintext, 64)
    key = ensure_length(key, 64)
    
    # Initial permutation
    bits = initial_permutation(plaintext)
    
    # Split into left and right halves
    left, right = bits[:32], bits[32:]
    
    round_keys = key_schedule(key)  # Function to generate round keys
    
    # Perform 16 rounds of encryption
    for i in range(16):
        new_right = xor(left, round_function(right, round_keys[i]))
        left, right = right, new_right
    
    # Combine the left and right halves and apply inverse initial permutation
    result = inverse_initial_permutation(left + right)
    
    # Return the ciphertext as a string of bits
    return ''.join(str(bit) for bit in result)


# Key schedule function (simplified for this example)
def key_schedule(key):
    # This is a simplified version of key scheduling
    # Normally it generates 16 subkeys based on the key
    return [key] * 16  # Just use the original key for all rounds for simplicity

# Example usage
plaintext = "011011110110111101101110011001110110101101110100"  # Example 64-bit binary plaintext
key = "0001001100110100010101110111100110011011101111001101111111110000"  # Example 64-bit binary key

ciphertext = des_encrypt(plaintext, key)
print("Ciphertext:", ciphertext)

