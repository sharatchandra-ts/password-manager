from cryptography.fernet import Fernet
import os

class Encode:
    def __init__(self):
        self.key_file = "database/secret.key"
        self.f = Fernet(self.load_or_create_key())

    def load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as file:
                file.write(key)
            return key

    def encrypt(self, password):
        return self.f.encrypt(password.encode()).decode()

    def decrypt(self, encoded_password):
        return self.f.decrypt(encoded_password).decode()
