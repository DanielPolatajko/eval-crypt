import click
from eval_crypt.gitattributes import add_to_gitattributes, remove_from_gitattributes, list_gitattributes, GITATTRIBUTES_PATH
from eval_crypt.crypto import generate_key, KEY_FILE
import os
from eval_crypt.git_config import configure_git_filters
from eval_crypt.filters import encrypt_content, decrypt_content

@click.group()
def main():
    """eval-crypt: Manage files to be automatically encrypted/decrypted by git hooks."""
    pass

@main.command()
def init():
    """Initialize eval-crypt by creating .gitattributes and a secret key if they do not exist, and configure git filters."""
    if GITATTRIBUTES_PATH.exists():
        click.echo(".gitattributes already exists.")
    else:
        GITATTRIBUTES_PATH.touch()
        click.echo("Created .gitattributes.")
    if os.path.exists(KEY_FILE):
        click.echo(f"Secret key already exists at {KEY_FILE}.")
    else:
        generate_key()
        click.echo(f"Created secret key at {KEY_FILE}.")
    # Configure git filters
    if configure_git_filters():
        click.echo("Configured git filters for eval-crypt.")
    else:
        click.echo("Failed to configure git filters for eval-crypt.")

@main.command()
@click.argument('file_path', type=click.Path())
def add(file_path):
    """Add a file to the managed encryption list."""
    result = add_to_gitattributes(file_path)
    if result is None:
        return
    if result:
        click.echo(f"Added {file_path} to the managed encryption list.")
    else:
        click.echo(f"{file_path} is already in the managed encryption list.")

@main.command()
@click.argument('file_path', type=click.Path())
def remove(file_path):
    """Remove a file from the managed encryption list."""
    result = remove_from_gitattributes(file_path)
    if result is None:
        return
    if result:
        click.echo(f"Removed {file_path} from the managed encryption list.")
    else:
        click.echo(f"{file_path} was not found in the managed encryption list.")

@main.command()
def list():
    """List all files managed for encryption."""
    managed = list_gitattributes()
    if managed is None:
        return
    if managed:
        click.echo("Files managed for encryption:")
        for f in managed:
            click.echo(f"  {f}")
    else:
        click.echo("No files are currently managed for encryption.")

@main.command()
@click.argument('file', required=False, type=click.Path(exists=False))
def clean(file=None):
    """Git clean filter: encrypt file content from stdin to stdout."""
    import sys
    from eval_crypt.crypto import get_key
    key = get_key()
    data = sys.stdin.buffer.read()
    encrypted = encrypt_content(data, key)
    sys.stdout.buffer.write(encrypted)

@main.command()
@click.argument('file', required=False, type=click.Path(exists=False))
def smudge(file=None):
    """Git smudge filter: decrypt file content from stdin to stdout."""
    import sys
    from eval_crypt.crypto import get_key
    key = get_key()
    data = sys.stdin.buffer.read()
    try:
        decrypted = decrypt_content(data, key)
        sys.stdout.buffer.write(decrypted)
    except Exception:
        # If decryption fails, output the original data
        sys.stdout.buffer.write(data)

if __name__ == "__main__":
    main()
