from Crypto.Random import get_random_bytes
import os

KEY_FILE = "eval-crypt.key"


def generate_key(key_file: str = KEY_FILE) -> bytes:
    """Generate a new 16-byte AES key and save it to key_file if it doesn't exist."""
    if not os.path.exists(key_file):
        key = get_random_bytes(16)
        with open(key_file, "wb") as f:
            f.write(key)
    else:
        with open(key_file, "rb") as f:
            key = f.read()
    return key 