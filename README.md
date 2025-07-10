# eval-crypt

A tool to encrypt sensitive AI safety evaluation files in Git repositories.

## Installation

```bash
pip install eval-crypt
```

For development:
```bash
git clone https://github.com/DanielPolatajko/eval-crypt.git
cd eval-crypt
pip install -e .
```

## Usage

```bash
# Encrypt a file
eval-crypt encrypt path/to/sensitive/file.txt

# Decrypt a file
eval-crypt decrypt path/to/encrypted/file.txt.enc
```

## Features

- Secure AES encryption for sensitive files
- Simple CLI interface
- Git integration via pre-commit hooks

## License

TBD
