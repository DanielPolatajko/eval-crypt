import tempfile
from pathlib import Path
from eval_crypt.crypto import generate_key

def test_generate_key_creates_file_and_returns_key():
    with tempfile.TemporaryDirectory() as tmpdir:
        key_path = Path(tmpdir) / "test.key"
        key = generate_key(str(key_path))
        assert key_path.exists()
        assert isinstance(key, bytes)
        assert len(key) == 16
        # Key file contents should match returned key
        with open(key_path, "rb") as f:
            file_key = f.read()
        assert file_key == key

def test_generate_key_idempotent():
    with tempfile.TemporaryDirectory() as tmpdir:
        key_path = Path(tmpdir) / "test.key"
        key1 = generate_key(str(key_path))
        key2 = generate_key(str(key_path))
        assert key1 == key2
        # File should not be overwritten
        with open(key_path, "rb") as f:
            file_key = f.read()
        assert file_key == key1 