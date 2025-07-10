from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import json
from base64 import b64encode, b64decode

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


def encrypt_file(input_path: str, key: bytes, output_path: str = None) -> str:
    """Encrypt a file using AES-CTR and write the result to output_path (.enc by default)."""
    if output_path is None:
        output_path = input_path + ".enc"
    with open(input_path, "rb") as f:
        plaintext = f.read()
    cipher = AES.new(key, AES.MODE_CTR)
    ciphertext = cipher.encrypt(plaintext)
    nonce = b64encode(cipher.nonce).decode("utf-8")
    ct = b64encode(ciphertext).decode("utf-8")
    result = json.dumps({"nonce": nonce, "ciphertext": ct})
    with open(output_path, "w") as f:
        f.write(result)
    return output_path


def decrypt_file(enc_path: str, key: bytes, output_path: str = None) -> str:
    """Decrypt a .enc file using AES-CTR and write the result to output_path (original name by default)."""
    if output_path is None and enc_path.endswith(".enc"):
        output_path = enc_path[:-4]
    elif output_path is None:
        output_path = enc_path + ".dec"
    with open(enc_path, "r") as f:
        data = json.load(f)
    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    with open(output_path, "wb") as f:
        f.write(plaintext)
    return output_path 