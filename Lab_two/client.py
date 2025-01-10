import socket

def client():
    host = 'localhost'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        action = input("Enter action (encrypt/decrypt): ").strip()
        plaintext = input("Enter 8-bit plaintext: ").strip()
        key = input("Enter 10-bit key: ").strip()

        data = f"{action},{plaintext},{key}"
        s.send(data.encode())
        result = s.recv(1024).decode()

        print(f"Result: {result}")

if __name__ == "__main__":
    client()
