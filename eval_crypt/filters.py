from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import json
from typing import Optional

def is_encrypted(content: bytes) -> bool:
    """Check if content is already in our encrypted format."""
    try:
        data = json.loads(content.decode('utf-8'))
        return "nonce" in data and "ciphertext" in data
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False

def encrypt_content(content: bytes, secret_key: bytes) -> bytes:
    """Encrypt content using AES encryption. Idempotent: returns input if already encrypted."""
    if is_encrypted(content):
        return content  # Already encrypted
    cipher = AES.new(secret_key, AES.MODE_CTR)
    encrypted = cipher.encrypt(content)
    nonce = b64encode(cipher.nonce).decode("utf-8")
    ct = b64encode(encrypted).decode("utf-8")
    result = json.dumps({"nonce": nonce, "ciphertext": ct})
    return result.encode('utf-8')

def decrypt_content(content: bytes, secret_key: bytes) -> bytes:
    """Decrypt content that was encrypted using encrypt_content. Returns input if not encrypted."""
    if not is_encrypted(content):
        return content  # Not encrypted or not in our format
    data = json.loads(content.decode('utf-8'))
    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])
    cipher = AES.new(secret_key, AES.MODE_CTR, nonce=nonce)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted 