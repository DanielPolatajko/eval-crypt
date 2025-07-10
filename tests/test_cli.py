import os
import pytest
from click.testing import CliRunner
from pathlib import Path

from eval_crypt.cli import main
from eval_crypt.crypto import KEY_FILE

GITATTRIBUTES_PATH = Path('.gitattributes')

@pytest.fixture(autouse=True)
def clean_gitattributes():
    # Remove .gitattributes before and after each test for isolation
    if GITATTRIBUTES_PATH.exists():
        GITATTRIBUTES_PATH.unlink()
    yield
    if GITATTRIBUTES_PATH.exists():
        GITATTRIBUTES_PATH.unlink()

@pytest.fixture
def runner():
    return CliRunner()

def test_init_command(runner):
    with runner.isolated_filesystem():
        assert not GITATTRIBUTES_PATH.exists()
        result = runner.invoke(main, ['init'])
        assert result.exit_code == 0
        assert "Created .gitattributes." in result.output
        assert GITATTRIBUTES_PATH.exists()
        # Should not overwrite if already exists
        result2 = runner.invoke(main, ['init'])
        assert result2.exit_code == 0
        assert ".gitattributes already exists." in result2.output

def test_init_creates_key_and_gitattributes(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(main, ['init'])
        assert result.exit_code == 0
        assert os.path.exists('.gitattributes')
        assert os.path.exists(KEY_FILE)
        assert "Created .gitattributes." in result.output or ".gitattributes already exists." in result.output
        assert f"Created secret key at {KEY_FILE}." in result.output or f"Secret key already exists at {KEY_FILE}." in result.output

def test_init_does_not_overwrite_existing_key(runner):
    with runner.isolated_filesystem():
        # Create a dummy key file
        with open(KEY_FILE, 'wb') as f:
            f.write(b'1234567890abcdef')
        result = runner.invoke(main, ['init'])
        assert result.exit_code == 0
        with open(KEY_FILE, 'rb') as f:
            key_contents = f.read()
        assert key_contents == b'1234567890abcdef'
        assert f"Secret key already exists at {KEY_FILE}." in result.output

def test_init_configures_git_filter(runner):
    with runner.isolated_filesystem():
        import subprocess
        subprocess.run(["git", "init"], check=True)
        result = runner.invoke(main, ["init"])
        assert result.exit_code == 0
        clean = subprocess.run(["git", "config", "--local", "filter.eval-crypt.clean"], capture_output=True, text=True)
        smudge = subprocess.run(["git", "config", "--local", "filter.eval-crypt.smudge"], capture_output=True, text=True)
        required = subprocess.run(["git", "config", "--local", "filter.eval-crypt.required"], capture_output=True, text=True)
        assert clean.stdout.strip() == "eval-crypt clean"
        assert smudge.stdout.strip() == "eval-crypt smudge"
        assert required.stdout.strip() == "true"

def test_add_command_requires_init(runner):
    with runner.isolated_filesystem():
        assert not GITATTRIBUTES_PATH.exists()
        result = runner.invoke(main, ['add', 'test.txt'])
        assert result.exit_code == 0
        assert ".gitattributes not found. Please run 'eval-crypt init' first." in result.output
        assert not GITATTRIBUTES_PATH.exists()

def test_add_command(runner):
    with runner.isolated_filesystem():
        import subprocess
        subprocess.run(["git", "init"], check=True)
        runner.invoke(main, ['init'])
        result = runner.invoke(main, ['add', 'test.txt'])
        assert result.exit_code == 0
        assert "Added test.txt to the managed encryption list." in result.output
        assert GITATTRIBUTES_PATH.exists()
        with GITATTRIBUTES_PATH.open() as f:
            lines = f.readlines()
        expected_entry = 'test.txt filter=eval-crypt diff=eval-crypt merge=eval-crypt\n'
        assert expected_entry in lines

def test_add_idempotent(runner):
    with runner.isolated_filesystem():
        import subprocess
        subprocess.run(["git", "init"], check=True)
        runner.invoke(main, ['init'])
        runner.invoke(main, ['add', 'test.txt'])
        result = runner.invoke(main, ['add', 'test.txt'])
        assert result.exit_code == 0
        assert "already in the managed encryption list" in result.output
        with GITATTRIBUTES_PATH.open() as f:
            lines = f.readlines()
        expected_entry = 'test.txt filter=eval-crypt diff=eval-crypt merge=eval-crypt\n'
        assert lines.count(expected_entry) == 1

def test_remove_command_requires_init(runner):
    with runner.isolated_filesystem():
        assert not GITATTRIBUTES_PATH.exists()
        result = runner.invoke(main, ['remove', 'test.txt'])
        assert result.exit_code == 0
        assert ".gitattributes not found. Please run 'eval-crypt init' first." in result.output

def test_remove_command(runner):
    with runner.isolated_filesystem():
        import subprocess
        subprocess.run(["git", "init"], check=True)
        runner.invoke(main, ['init'])
        runner.invoke(main, ['add', 'test.txt'])
        result = runner.invoke(main, ['remove', 'test.txt'])
        assert result.exit_code == 0
        assert "Removed test.txt from the managed encryption list." in result.output
        with GITATTRIBUTES_PATH.open() as f:
            lines = f.readlines()
        assert 'test.txt filter=eval-crypt\n' not in lines

def test_remove_not_found(runner):
    with runner.isolated_filesystem():
        import subprocess
        subprocess.run(["git", "init"], check=True)
        runner.invoke(main, ['init'])
        result = runner.invoke(main, ['remove', 'notfound.txt'])
        assert result.exit_code == 0
        assert "was not found in the managed encryption list" in result.output

def test_list_command_requires_init(runner):
    with runner.isolated_filesystem():
        assert not GITATTRIBUTES_PATH.exists()
        result = runner.invoke(main, ['list'])
        assert result.exit_code == 0
        assert ".gitattributes not found. Please run 'eval-crypt init' first." in result.output

def test_list_command(runner):
    with runner.isolated_filesystem():
        import subprocess
        subprocess.run(["git", "init"], check=True)
        runner.invoke(main, ['init'])
        runner.invoke(main, ['add', 'file1.txt'])
        runner.invoke(main, ['add', 'file2.txt'])
        result = runner.invoke(main, ['list'])
        assert result.exit_code == 0
        assert "Files managed for encryption:" in result.output
        assert "file1.txt" in result.output
        assert "file2.txt" in result.output

def test_list_empty(runner):
    with runner.isolated_filesystem():
        import subprocess
        subprocess.run(["git", "init"], check=True)
        runner.invoke(main, ['init'])
        result = runner.invoke(main, ['list'])
        assert result.exit_code == 0
        assert "No files are currently managed for encryption." in result.output

def test_clean_and_smudge_roundtrip(runner):
    with runner.isolated_filesystem():
        plaintext = b"Sensitive test data"
        result_clean = runner.invoke(main, ["clean"], input=plaintext, catch_exceptions=False)
        assert result_clean.exit_code == 0
        encrypted = result_clean.stdout_bytes
        assert encrypted != plaintext
        result_smudge = runner.invoke(main, ["smudge"], input=encrypted, catch_exceptions=False)
        assert result_smudge.exit_code == 0
        decrypted = result_smudge.stdout_bytes
        assert decrypted == plaintext

# The following tests are for future implementation:
# def test_encrypt_decrypt_commands(runner, temp_git_repo):
#     ...
# def test_clean_smudge_commands(runner, temp_git_repo):
#     ... 