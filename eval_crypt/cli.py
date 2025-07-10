import click
from eval_crypt.gitattributes import add_to_gitattributes, remove_from_gitattributes, list_gitattributes, GITATTRIBUTES_PATH

@click.group()
def main():
    """eval-crypt: Manage files to be automatically encrypted/decrypted by git hooks."""
    pass

@main.command()
def init():
    """Initialize eval-crypt by creating .gitattributes if it does not exist."""
    if GITATTRIBUTES_PATH.exists():
        click.echo(".gitattributes already exists.")
    else:
        GITATTRIBUTES_PATH.touch()
        click.echo("Created .gitattributes.")

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

if __name__ == "__main__":
    main()
