import os
import pytest
from click.testing import CliRunner
from pathlib import Path

from eval_crypt.cli import main

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

@pytest.fixture
def temp_git_repo(tmp_path):
    cwd = os.getcwd()
    os.chdir(tmp_path)
    os.system('git init')
    yield tmp_path
    os.chdir(cwd)

def test_init_command(runner, temp_git_repo):
    # Should create .gitattributes if missing
    assert not GITATTRIBUTES_PATH.exists()
    result = runner.invoke(main, ['init'])
    assert result.exit_code == 0
    assert "Created .gitattributes." in result.output
    assert GITATTRIBUTES_PATH.exists()
    # Should not overwrite if already exists
    result2 = runner.invoke(main, ['init'])
    assert result2.exit_code == 0
    assert ".gitattributes already exists." in result2.output

def test_add_command_requires_init(runner, temp_git_repo):
    # Should warn if .gitattributes missing
    assert not GITATTRIBUTES_PATH.exists()
    result = runner.invoke(main, ['add', 'test.txt'])
    assert result.exit_code == 0
    assert ".gitattributes not found. Please run 'eval-crypt init' first." in result.output
    assert not GITATTRIBUTES_PATH.exists()

def test_add_command(runner, temp_git_repo):
    runner.invoke(main, ['init'])
    result = runner.invoke(main, ['add', 'test.txt'])
    assert result.exit_code == 0
    assert "Added test.txt to the managed encryption list." in result.output
    # Check .gitattributes content
    assert GITATTRIBUTES_PATH.exists()
    with GITATTRIBUTES_PATH.open() as f:
        lines = f.readlines()
    assert 'test.txt filter=eval-crypt\n' in lines

def test_add_idempotent(runner, temp_git_repo):
    runner.invoke(main, ['init'])
    runner.invoke(main, ['add', 'test.txt'])
    result = runner.invoke(main, ['add', 'test.txt'])
    assert result.exit_code == 0
    assert "already in the managed encryption list" in result.output
    # Only one entry
    with GITATTRIBUTES_PATH.open() as f:
        lines = f.readlines()
    assert lines.count('test.txt filter=eval-crypt\n') == 1

def test_remove_command_requires_init(runner, temp_git_repo):
    assert not GITATTRIBUTES_PATH.exists()
    result = runner.invoke(main, ['remove', 'test.txt'])
    assert result.exit_code == 0
    assert ".gitattributes not found. Please run 'eval-crypt init' first." in result.output

def test_remove_command(runner, temp_git_repo):
    runner.invoke(main, ['init'])
    runner.invoke(main, ['add', 'test.txt'])
    result = runner.invoke(main, ['remove', 'test.txt'])
    assert result.exit_code == 0
    assert "Removed test.txt from the managed encryption list." in result.output
    # Should be removed
    with GITATTRIBUTES_PATH.open() as f:
        lines = f.readlines()
    assert 'test.txt filter=eval-crypt\n' not in lines

def test_remove_not_found(runner, temp_git_repo):
    runner.invoke(main, ['init'])
    result = runner.invoke(main, ['remove', 'notfound.txt'])
    assert result.exit_code == 0
    assert "was not found in the managed encryption list" in result.output

def test_list_command_requires_init(runner, temp_git_repo):
    assert not GITATTRIBUTES_PATH.exists()
    result = runner.invoke(main, ['list'])
    assert result.exit_code == 0
    assert ".gitattributes not found. Please run 'eval-crypt init' first." in result.output

def test_list_command(runner, temp_git_repo):
    runner.invoke(main, ['init'])
    runner.invoke(main, ['add', 'file1.txt'])
    runner.invoke(main, ['add', 'file2.txt'])
    result = runner.invoke(main, ['list'])
    assert result.exit_code == 0
    assert "Files managed for encryption:" in result.output
    assert "file1.txt" in result.output
    assert "file2.txt" in result.output

def test_list_empty(runner, temp_git_repo):
    runner.invoke(main, ['init'])
    result = runner.invoke(main, ['list'])
    assert result.exit_code == 0
    assert "No files are currently managed for encryption." in result.output

# The following tests are for future implementation:
# def test_encrypt_decrypt_commands(runner, temp_git_repo):
#     ...
# def test_clean_smudge_commands(runner, temp_git_repo):
#     ... 