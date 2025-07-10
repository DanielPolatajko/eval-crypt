import os

GITATTRIBUTES_PATH = os.path.join(os.getcwd(), ".gitattributes")
FILTER_NAME = "eval-crypt"

def add_pattern(pattern: str):
    """Add a file pattern to .gitattributes for eval-crypt filtering."""
    line = f"{pattern} filter={FILTER_NAME}\n"
    if not os.path.exists(GITATTRIBUTES_PATH):
        with open(GITATTRIBUTES_PATH, "w") as f:
            f.write(line)
        return
    with open(GITATTRIBUTES_PATH, "r+") as f:
        lines = f.readlines()
        if line in lines:
            return
        f.write(line)

def remove_pattern(pattern: str):
    """Remove a file pattern from .gitattributes for eval-crypt filtering."""
    line = f"{pattern} filter={FILTER_NAME}\n"
    if not os.path.exists(GITATTRIBUTES_PATH):
        return
    with open(GITATTRIBUTES_PATH, "r") as f:
        lines = f.readlines()
    with open(GITATTRIBUTES_PATH, "w") as f:
        for l in lines:
            if l != line:
                f.write(l)

def list_patterns():
    """List all file patterns managed for eval-crypt filtering in .gitattributes."""
    if not os.path.exists(GITATTRIBUTES_PATH):
        return []
    with open(GITATTRIBUTES_PATH, "r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines if f"filter={FILTER_NAME}" in l] 