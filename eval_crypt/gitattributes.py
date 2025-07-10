from pathlib import Path
import click

GITATTRIBUTES_PATH = Path('.gitattributes')
FILTER_ATTR = 'filter=eval-crypt diff=eval-crypt merge=eval-crypt'

def add_to_gitattributes(file_path):
    if not GITATTRIBUTES_PATH.exists():
        click.echo(".gitattributes not found. Please run 'eval-crypt init' first.")
        return None
    entry = f"{file_path} {FILTER_ATTR}\n"
    with GITATTRIBUTES_PATH.open('r+', encoding='utf-8') as f:
        lines = f.readlines()
        if entry in lines:
            return False  # Already present
        f.write(entry)
    return True

def remove_from_gitattributes(file_path):
    if not GITATTRIBUTES_PATH.exists():
        click.echo(".gitattributes not found. Please run 'eval-crypt init' first.")
        return None
    entry = f"{file_path} {FILTER_ATTR}\n"
    with GITATTRIBUTES_PATH.open('r', encoding='utf-8') as f:
        lines = f.readlines()
    if entry not in lines:
        return False
    lines = [line for line in lines if line != entry]
    with GITATTRIBUTES_PATH.open('w', encoding='utf-8') as f:
        f.writelines(lines)
    return True

def list_gitattributes():
    if not GITATTRIBUTES_PATH.exists():
        click.echo(".gitattributes not found. Please run 'eval-crypt init' first.")
        return None
    with GITATTRIBUTES_PATH.open('r', encoding='utf-8') as f:
        lines = f.readlines()
    managed = [line.split()[0] for line in lines if 'filter=eval-crypt' in line]
    return managed 