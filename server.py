import socket
from cryptography import caesar_encrypt
from encode import encode_binary, encode_hdb3

def start_server():
    # Create a TCP/IP socket 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to an address and port
    server_socket.bind(('localhost', 65432))

    # Listen for connections 
    server_socket.listen()

    print("Server waiting for connections...")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        try:
            # Send a message to the client
            message = "Hello, client! This is a message from server"

            shift = 4 # Shift value for caesar cipher
            encrypted_message = caesar_encrypt(message, shift)
            binary_message = encode_binary(encrypted_message)
            hdb3_message = encode_hdb3(binary_message)

            client_socket.sendall(hdb3_message.encode('utf-8'))
            
            print(f"Message sent: {message}")
            print(f"Encrypted message sent: {encrypted_message}")
            print(f"Binary message sent: {binary_message}")
            print(f"Encoded HDB3 message sent: {hdb3_message}")

        finally:
            # Close the connection with client
            client_socket.close()

if __name__ == "__main__":
    start_server()
