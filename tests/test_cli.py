import os
import tempfile
import pytest
from click.testing import CliRunner
from pathlib import Path

from eval_crypt.cli import main

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def temp_git_repo(tmp_path):
    cwd = os.getcwd()
    os.chdir(tmp_path)
    os.system('git init')
    yield tmp_path
    os.chdir(cwd)

def test_add_command(runner, temp_git_repo):
    result = runner.invoke(main, ['add', 'test.txt'])
    assert result.exit_code == 0
    assert "Added test.txt to the managed encryption list." in result.output

def test_remove_command(runner, temp_git_repo):
    result = runner.invoke(main, ['remove', 'test.txt'])
    assert result.exit_code == 0
    assert "Removed test.txt from the managed encryption list." in result.output

def test_list_command(runner, temp_git_repo):
    result = runner.invoke(main, ['list'])
    assert result.exit_code == 0
    assert "Listing all managed files..." in result.output

# The following tests are for future implementation:
# def test_encrypt_decrypt_commands(runner, temp_git_repo):
#     ...
# def test_clean_smudge_commands(runner, temp_git_repo):
#     ... 