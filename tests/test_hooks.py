from eval_crypt.hooks import clean_filter, smudge_filter
from eval_crypt.filters import encrypt_content, decrypt_content

SECRET_KEY = b'0123456789abcdef'


def test_clean_filter_encrypts():
    plaintext = b"hook test data"
    encrypted = clean_filter(plaintext, SECRET_KEY)
    # Should be encrypted and decryptable
    assert encrypted != plaintext
    decrypted = decrypt_content(encrypted, SECRET_KEY)
    assert decrypted == plaintext

def test_smudge_filter_decrypts():
    plaintext = b"hook test data"
    encrypted = encrypt_content(plaintext, SECRET_KEY)
    decrypted = smudge_filter(encrypted, SECRET_KEY)
    assert decrypted == plaintext


def test_clean_filter_idempotent():
    plaintext = b"already encrypted"
    encrypted = encrypt_content(plaintext, SECRET_KEY)
    encrypted2 = clean_filter(encrypted, SECRET_KEY)
    assert encrypted2 == encrypted

def test_smudge_filter_on_plaintext():
    plaintext = b"not encrypted"
    decrypted = smudge_filter(plaintext, SECRET_KEY)
    assert decrypted == plaintext 