import os
import time
import binascii
from DES import des_decrypt, des_encrypt

def measure_decryption_time(key):
    file_sizes = {"512 bits": 64, "1 KB": 1024, "10 KB": 10240}
    decryption_times = {}

    for label, size in file_sizes.items():
        # Generate random binary data and convert it to hexadecimal
        data = os.urandom(size)
        hex_data = binascii.hexlify(data).decode().upper()

        # Ensure data is a multiple of 16 hex chars (64-bit blocks)
        if len(hex_data) % 16 != 0:
            hex_data = hex_data.ljust((len(hex_data) // 16 + 1) * 16, '0')

        # Encrypt the data
        encrypted_data = des_encrypt(hex_data, key)

        # Measure decryption time
        start_time = time.time()
        decrypted_data = des_decrypt(encrypted_data, key)
        end_time = time.time()

        decryption_times[label] = end_time - start_time

    return decryption_times

# 64-bit DES key
hex_key = "AABB09182736CCDD"

# Measure decryption time
decryption_results = measure_decryption_time(hex_key)

# Display the results
for size, duration in decryption_results.items():
    print(f"Decryption time for {size}: {duration:.6f} seconds")

