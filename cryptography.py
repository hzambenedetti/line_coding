# Caesar cipher with some changes

# Some explanations:
# ord() converts a char to its ASCII number (an integer)
# example: ord('A') returns 65

# % 256 ensures that the result falls within the range of 0 to 255

# chr() converts an ASCII value to its char representation
# example: chr(69) returns 'E'

def caesar_encrypt(text, shift):
    result = ""

    for char in text:
        # Encrypt all printable characters
        if char.isprintable():
            encrypted_char = chr((ord(char) + shift) % 256)
            result += encrypted_char
        else:
            result += char

    return result

def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        # Decrypt all printable characters
        if char.isprintable():
            decrypted_char = chr((ord(char) - shift) % 256)
            result += decrypted_char
        else:
            result += char

    return result

