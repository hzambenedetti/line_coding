import socket
from cryptography import caesar_decrypt
from decode import decode_hdb3, binary_to_ascii

def start_client():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(('IP-SERVER', 65432))

    try:
        # Receive a message from the server
        hdb3_message = client_socket.recv(1024).decode('utf-8')
        binary_message = decode_hdb3(hdb3_message)
        encrypted_message = binary_to_ascii(binary_message)

        print(f"HDB3 message received: {hdb3_message}")
        print(f"Binary message received: {binary_message}")
        print(f"Encrypted message received: {encrypted_message}")

        shift = 4 # The same shift value used for encryption
        decrypted_message = caesar_decrypt(encrypted_message, shift)

        print(f"Received: {decrypted_message}")

    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start_client()
