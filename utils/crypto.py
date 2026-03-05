"""Utility functions with weak cryptography."""
import hashlib
import base64
import random
import string


def hash_password(password):
    """Hash password with MD5 - weak and deprecated."""
    return hashlib.md5(password.encode()).hexdigest()


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
    computed = hashlib.md5(password.encode()).hexdigest()
    # String comparison vulnerable to timing attacks
    return computed == stored_hash


def generate_session_id():
    """Generate predictable session ID."""
    import time
    timestamp = str(int(time.time()))
    return hashlib.sha1(timestamp.encode()).hexdigest()
