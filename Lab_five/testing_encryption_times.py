import os
import time
import binascii
from DES import des_encrypt

def generate_random_data(size_in_bytes):
    return os.urandom(size_in_bytes)

def measure_encryption_time(des_encrypt, key):
    file_sizes = {"512 bits": 64, "1 KB": 1024, "10 KB": 10240}
    encryption_times = {}

    for label, size in file_sizes.items():
        # Generate random binary data and convert it to hexadecimal
        data = generate_random_data(size)
        hex_data = binascii.hexlify(data).decode().upper()  # Convert to hex

        # Ensure plaintext is exactly 16 hex chars (64 bits) for DES blocks
        if len(hex_data) % 16 != 0:
            hex_data = hex_data.ljust((len(hex_data) // 16 + 1) * 16, '0')

        start_time = time.time()  # Start timing
        encrypted_data = des_encrypt(hex_data, key)  # Encrypt data
        end_time = time.time()  # End timing

        encryption_times[label] = end_time - start_time  # Compute duration

    return encryption_times


# 64-bit DES key
hex_key = "AABB09182736CCDD"

# Measure encryption time
encryption_results = measure_encryption_time(des_encrypt, hex_key)

# Display the results
for size, duration in encryption_results.items():
    print(f"Encryption time for {size}: {duration:.6f} seconds")
