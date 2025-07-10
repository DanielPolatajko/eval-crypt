import pytest
from eval_crypt.gitattributes import add_to_gitattributes, remove_from_gitattributes, list_gitattributes, GITATTRIBUTES_PATH

@pytest.fixture(autouse=True)
def clean_gitattributes():
    if GITATTRIBUTES_PATH.exists():
        GITATTRIBUTES_PATH.unlink()
    yield
    if GITATTRIBUTES_PATH.exists():
        GITATTRIBUTES_PATH.unlink()

def test_add_and_list_gitattributes():
    GITATTRIBUTES_PATH.touch()
    assert add_to_gitattributes('file1.txt') is True
    assert add_to_gitattributes('file2.txt') is True
    assert add_to_gitattributes('file1.txt') is False  # duplicate
    managed = list_gitattributes()
    assert managed is not None
    assert 'file1.txt' in managed
    assert 'file2.txt' in managed
    assert len(managed) == 2

def test_remove_gitattributes():
    GITATTRIBUTES_PATH.touch()
    add_to_gitattributes('file1.txt')
    add_to_gitattributes('file2.txt')
    assert remove_from_gitattributes('file1.txt') is True
    assert remove_from_gitattributes('file1.txt') is False  # already removed
    managed = list_gitattributes()
    assert managed is not None
    assert 'file1.txt' not in managed
    assert 'file2.txt' in managed
    assert remove_from_gitattributes('file2.txt') is True
    managed = list_gitattributes()
    assert managed is not None
    assert managed == []

def test_list_gitattributes_empty():
    GITATTRIBUTES_PATH.touch()
    managed = list_gitattributes()
    assert managed is not None
    assert managed == []

def test_add_remove_without_gitattributes():
    if GITATTRIBUTES_PATH.exists():
        GITATTRIBUTES_PATH.unlink()
    assert add_to_gitattributes('file.txt') is None
    assert remove_from_gitattributes('file.txt') is None
    assert list_gitattributes() is None 