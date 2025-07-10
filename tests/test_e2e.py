import os
import subprocess
from click.testing import CliRunner
from eval_crypt.cli import main
from eval_crypt.crypto import generate_key, KEY_FILE
from eval_crypt.filters import encrypt_content, decrypt_content

SECRET_CONTENT = b"super secret data"


def test_end_to_end_encryption_decryption(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Simulate a git repo
        subprocess.run(["git", "init"], check=True)

        # 1. Run eval-crypt init
        result = runner.invoke(main, ["init"])
        assert result.exit_code == 0
        assert os.path.exists(".gitattributes")
        assert os.path.exists(KEY_FILE)

        # 2. Create two files
        with open("secret1.txt", "wb") as f:
            f.write(SECRET_CONTENT)
        with open("secret2.txt", "wb") as f:
            f.write(SECRET_CONTENT)

        # 3. Add both files, then remove one
        result = runner.invoke(main, ["add", "secret1.txt"])
        assert result.exit_code == 0
        result = runner.invoke(main, ["add", "secret2.txt"])
        assert result.exit_code == 0
        result = runner.invoke(main, ["remove", "secret2.txt"])
        assert result.exit_code == 0

        # 4. Check .gitattributes only lists secret1.txt
        with open(".gitattributes", "r") as f:
            lines = f.read().splitlines()
        assert any("secret1.txt" in line for line in lines)
        assert not any("secret2.txt" in line for line in lines)

        # 5. Simulate commit: encrypt secret1.txt
        key = generate_key()
        with open("secret1.txt", "rb") as f:
            plaintext = f.read()
        encrypted = encrypt_content(plaintext, key)
        with open("secret1.txt", "wb") as f:
            f.write(encrypted)
        # File should now be encrypted
        with open("secret1.txt", "rb") as f:
            encrypted_on_disk = f.read()
        assert encrypted_on_disk != SECRET_CONTENT
        # Should be decryptable
        decrypted = decrypt_content(encrypted_on_disk, key)
        assert decrypted == SECRET_CONTENT

        # 6. Simulate merge/checkout: decrypt secret1.txt
        with open("secret1.txt", "rb") as f:
            encrypted = f.read()
        decrypted = decrypt_content(encrypted, key)
        with open("secret1.txt", "wb") as f:
            f.write(decrypted)
        # File should now be plaintext again
        with open("secret1.txt", "rb") as f:
            final_content = f.read()
        assert final_content == SECRET_CONTENT 