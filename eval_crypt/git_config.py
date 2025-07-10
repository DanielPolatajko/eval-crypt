import subprocess

FILTER_SECTION = 'filter.eval-crypt'
CLEAN_CMD = 'eval-crypt clean'
SMUDGE_CMD = 'eval-crypt smudge'
REQUIRED = 'true'

def configure_git_filters(clean_cmd=None, smudge_cmd=None):
    """Ensure the eval-crypt filter is registered in .git/config with correct clean/smudge commands.
    Optionally override the clean and smudge commands (for testing)."""
    clean = clean_cmd or CLEAN_CMD
    smudge = smudge_cmd or SMUDGE_CMD
    try:
        # Set clean command
        subprocess.run(['git', 'config', '--local', f'{FILTER_SECTION}.clean', clean], check=True)
        # Set smudge command
        subprocess.run(['git', 'config', '--local', f'{FILTER_SECTION}.smudge', smudge], check=True)
        # Set required
        subprocess.run(['git', 'config', '--local', f'{FILTER_SECTION}.required', REQUIRED], check=True)
        return True
    except Exception:
        return False 