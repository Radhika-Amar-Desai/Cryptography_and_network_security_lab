import socket

# XOR Encryption and Decryption functions
def xor_encrypt_decrypt(message, key):
    return ''.join(chr(ord(c) ^ key) for c in message)

def start_client():
    # XOR key (same key used in the server)
    key = 123

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 12345

    # Connect to the server
    client_socket.connect((host, port))

    # Message to send
    message = "Hello, Server!"
    encrypted_message = xor_encrypt_decrypt(message, key)

    # Send encrypted message to the server
    client_socket.send(encrypted_message.encode())

    # Receive encrypted response from the server
    encrypted_response = client_socket.recv(1024).decode()
    print(f"Received encrypted response: {encrypted_response}")

    # Decrypt the response
    decrypted_response = xor_encrypt_decrypt(encrypted_response, key)
    print(f"Decrypted response: {decrypted_response}")

    # Close the client connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
