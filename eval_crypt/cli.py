import click

@click.group()
def main():
    """eval-crypt: Manage files to be automatically encrypted/decrypted by git hooks."""
    pass

@main.command()
@click.argument('file_path', type=click.Path())
def add(file_path):
    """Add a file to the managed encryption list."""
    click.echo(f"Added {file_path} to the managed encryption list.")
    # TODO: Implement logic to add file to config/list

@main.command()
@click.argument('file_path', type=click.Path())
def remove(file_path):
    """Remove a file from the managed encryption list."""
    click.echo(f"Removed {file_path} from the managed encryption list.")
    # TODO: Implement logic to remove file from config/list

@main.command()
def list():
    """List all files managed for encryption."""
    click.echo("Listing all managed files...")
    # TODO: Implement logic to list files from config/list

if __name__ == "__main__":
    main()
