import os

gitattributes_path = os.path.join(os.getcwd(), ".gitattributes")
filter_name = "eval-crypt"

def add_pattern(pattern: str):
    """Add a file pattern to .gitattributes for eval-crypt filtering."""
    line = f"{pattern} filter={filter_name}\n"
    if not os.path.exists(gitattributes_path):
        with open(gitattributes_path, "w") as f:
            f.write(line)
        return
    with open(gitattributes_path, "r+") as f:
        lines = f.readlines()
        if line in lines:
            return  # Already present
        f.write(line)

def remove_pattern(pattern: str):
    """Remove a file pattern from .gitattributes for eval-crypt filtering."""
    line = f"{pattern} filter={filter_name}\n"
    if not os.path.exists(gitattributes_path):
        return
    with open(gitattributes_path, "r") as f:
        lines = f.readlines()
    with open(gitattributes_path, "w") as f:
        for l in lines:
            if l != line:
                f.write(l)

def list_patterns():
    """List all file patterns managed for eval-crypt filtering in .gitattributes."""
    if not os.path.exists(gitattributes_path):
        return []
    with open(gitattributes_path, "r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines if f"filter={filter_name}" in l] 