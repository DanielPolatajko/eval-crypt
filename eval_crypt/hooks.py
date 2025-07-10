from eval_crypt.filters import encrypt_content, decrypt_content

# These functions are for use by git filters/hooks only, not CLI

def clean_filter(input_bytes: bytes, secret_key: bytes) -> bytes:
    """Git clean filter: encrypts file content before staging."""
    return encrypt_content(input_bytes, secret_key)

def smudge_filter(input_bytes: bytes, secret_key: bytes) -> bytes:
    """Git smudge filter: decrypts file content after checkout."""
    return decrypt_content(input_bytes, secret_key)

# Future: add functions to install/uninstall git hooks, register filters, etc. 