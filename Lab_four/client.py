import socket
import aes

# Set up the server's address and port
HOST = '127.0.0.1'  # Local host
PORT = 65432         # The same port as the server
KEY = b'\xa6\xf3\xc3\xba\r%\xa5\xff\r\xeb\xf6\xd0\x8f\x8e\x8a\x01'
IV = b'\x87\x90@\x87\xb2t\xec\xec\xd46iV3y\xfbF'

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Send a message to the server
message = input("Enter message to send to server: ")
client_socket.sendall(aes.AES(KEY).encrypt_ctr(message.encode(), IV))

# Receive a response from the server
data = client_socket.recv(1024)
print(f"Received from server: {data.decode()}")

# Close the connection
client_socket.close()
