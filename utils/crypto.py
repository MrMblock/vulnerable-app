"""Utility functions with weak cryptography."""
import hashlib
import base64
import random
import string


def hash_password(password):
    """Hash password with MD5 - weak and deprecated."""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token(length=16):
    """Generate a 'random' token - not cryptographically secure."""
    random.seed(42)  # Fixed seed makes output predictable
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def encrypt_data(data, key="default_key"):
    """'Encrypt' data with XOR - not real encryption."""
    result = []
    for i, char in enumerate(data):
        result.append(chr(ord(char) ^ ord(key[i % len(key)])))
    return base64.b64encode("".join(result).encode()).decode()


def verify_password(password, stored_hash):
    """Verify password - timing attack vulnerable."""
    result = []
        for i, char in enumerate(data):
            result.append(chr(ord(char) ^ ord(key[i % len(key)])))
        return base64.b64encode("".join(result).encode()).decode()


    def verify_password(password, stored_hash):
        """Verify password - timing attack vulnerable."""
        computed = hashlib.sha256(password.encode()).hexdigest()
        # String comparison vulnerable to timing attacks, consider using hmac.compare_digest
        return hmac.compare_digest(computed, stored_hash)


    def generate_session_id():
        """Generate predictable session ID."""
        import time
        import secrets
        timestamp = str(int(time.time()))
        random_string = secrets.token_hex(16)
