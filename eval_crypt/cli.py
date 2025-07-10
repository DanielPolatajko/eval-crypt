import click

@click.group()
def main():
    """eval-crypt: A tool to encrypt sensitive AI safety evaluation files."""
    pass

@main.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file path')
def encrypt(file_path, output):
    """Encrypt a sensitive file."""
    click.echo(f"Encrypting {file_path}")
    # Encryption logic will be implemented later

@main.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file path')
def decrypt(file_path, output):
    """Decrypt an encrypted file."""
    click.echo(f"Decrypting {file_path}")
    # Decryption logic will be implemented later

if __name__ == "__main__":
    main()
