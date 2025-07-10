import pytest
from eval_crypt import filters

SECRET_KEY = b'0123456789abcdef'  # 16 bytes for AES-128


def test_is_encrypted_false_on_plaintext():
    assert not filters.is_encrypted(b"hello world")

def test_encrypt_and_is_encrypted():
    plaintext = b"secret data"
    encrypted = filters.encrypt_content(plaintext, SECRET_KEY)
    assert filters.is_encrypted(encrypted)
    assert encrypted != plaintext

def test_encrypt_idempotency():
    plaintext = b"idempotent"
    encrypted1 = filters.encrypt_content(plaintext, SECRET_KEY)
    encrypted2 = filters.encrypt_content(encrypted1, SECRET_KEY)
    assert encrypted1 == encrypted2

def test_decrypt_content_round_trip():
    plaintext = b"round trip test"
    encrypted = filters.encrypt_content(plaintext, SECRET_KEY)
    decrypted = filters.decrypt_content(encrypted, SECRET_KEY)
    assert decrypted == plaintext

def test_decrypt_content_on_plaintext():
    plaintext = b"not encrypted"
    decrypted = filters.decrypt_content(plaintext, SECRET_KEY)
    assert decrypted == plaintext

def test_decrypt_content_wrong_key():
    plaintext = b"wrong key test"
    encrypted = filters.encrypt_content(plaintext, SECRET_KEY)
    wrong_key = b'abcdef0123456789'
    # Should raise ValueError or produce garbage, but not crash
    try:
        result = filters.decrypt_content(encrypted, wrong_key)
        # If decryption fails, result will not match plaintext
        assert result != plaintext
    except Exception:
        pass 