import re
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64


class Password:
    @staticmethod
    def is_valid_password(password):
        # Minimum length requirement
        if len(password) < 10:
            return False

        # Regular expressions to check for various criteria
        has_upper = re.search(r"[A-Z]", password)
        has_lower = re.search(r"[a-z]", password)
        has_digit = re.search(r"\d", password)
        has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

        # Checking if all criteria are met
        if has_upper and has_lower and has_digit and has_special:
            return True
        else:
            return False

    @staticmethod
    def generate_hash(password):
        # Convert password and salt to bytes
        password = password.encode('utf-8')
        salt = os.environ.get('PASSWORD_SALT').encode('utf-8')

        # Derive a 256-bit AES key using PBKDF2HMAC
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,  # You can adjust the number of iterations as needed
            backend=default_backend()
        )

        # Generate the hash
        key = kdf.derive(password)
        output = base64.encodebytes(key).decode('ascii')
        return output

    @staticmethod
    def check_password(input_password, stored_hash):
        input_hash = Password.generate_hash(input_password)
        # Compare the generated hash with the stored hash
        return input_hash == stored_hash

    @staticmethod
    def two_factor_authentication():
        # to be implemented in future
        pass
