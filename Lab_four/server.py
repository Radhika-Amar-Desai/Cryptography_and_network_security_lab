import socket
import aes

# Set up the server
HOST = '127.0.0.1'  # Local host
PORT = 65432         # Port to bind to
KEY = b'\xa6\xf3\xc3\xba\r%\xa5\xff\r\xeb\xf6\xd0\x8f\x8e\x8a\x01'
IV = b'\x87\x90@\x87\xb2t\xec\xec\xd46iV3y\xfbF'


# Create a socket object and bind it to the address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}...")

# Accept a connection from the client
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Handle the communication
try:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received encrypted message: {data}")
        
        decoded_data = aes.AES(KEY).decrypt_ctr(data, IV)
        print(f"Decrypted message: {decoded_data}")

except KeyboardInterrupt:
    print("Server interrupted")

# Close the connection
conn.close()
server_socket.close()
