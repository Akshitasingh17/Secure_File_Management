from cryptography.fernet import Fernet
import os

# Generate or load a key
def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return key

# Encrypt a file
def encrypt_file(file_data, key):
    f = Fernet(key)
    encrypted = f.encrypt(file_data)
    return encrypted

# Decrypt a file
def decrypt_file(encrypted_data, key):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_data)
    return decrypted
