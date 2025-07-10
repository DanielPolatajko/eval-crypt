import os
import subprocess
from click.testing import CliRunner
from eval_crypt.cli import main
from eval_crypt.crypto import KEY_FILE
from eval_crypt.git_config import configure_git_filters

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

        # Re-register the filter for the test environment
        configure_git_filters(
            clean_cmd="python -m eval_crypt.cli clean",
            smudge_cmd="python -m eval_crypt.cli smudge"
        )

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

        # 5. Add and commit secret1.txt (should trigger git clean filter)
        subprocess.run(["git", "add", "secret1.txt"], check=True)
        subprocess.run(["git", "commit", "-m", "Add encrypted secret1.txt"], check=True)

        # 6. The file in the repo should be encrypted (compare blob to plaintext)
        # Get the blob hash for secret1.txt
        blob_hash = subprocess.check_output(["git", "ls-files", "-s", "secret1.txt"]).decode().split()[1]
        # Extract the blob content
        blob_content = subprocess.check_output(["git", "cat-file", "-p", blob_hash])
        assert blob_content != SECRET_CONTENT

        # 7. Remove the file and restore it from git (should trigger smudge filter)
        os.remove("secret1.txt")
        subprocess.run(["git", "checkout", "--", "secret1.txt"], check=True)
        # File should now be plaintext again
        with open("secret1.txt", "rb") as f:
            final_content = f.read()
        assert final_content == SECRET_CONTENT 