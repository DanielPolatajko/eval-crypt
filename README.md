# eval-crypt

A Python tool to transparently encrypt sensitive files in Git repositories using git filters and hooks. Designed to help AI safety researchers and others prevent models from memorizing evaluation data during pre-training, while keeping workflows seamless for contributors.

## Why eval-crypt?

AI safety researchers often publish evaluation code and data to GitHub. If these repositories are later crawled for model pre-training, the models could memorize solutions to the evaluations, making them less effective at measuring emergent capabilities. eval-crypt ensures sensitive files are encrypted in the repository, but transparently decrypted for local work.

## Installation

```bash
pip install eval-crypt
```

## Quick Start

1. **Initialize eval-crypt in your repository:**
   ```bash
   eval-crypt init
   ```
   This creates a secret key and sets up git filters and hooks.

2. **Add sensitive files to be encrypted:**
   ```bash
   eval-crypt add secret.txt
   eval-crypt add "*.json"  # Use quotes for patterns with wildcards
   ```
   This updates `.gitattributes` so git knows to filter these files.

3. **Use git as normal:**
   - When you commit, sensitive files are encrypted in the repo.
   - When you checkout or pull, they are transparently decrypted in your working directory.

## How It Works

- **Git filters**: eval-crypt registers a `clean` filter (encrypt on commit) and a `smudge` filter (decrypt on checkout).
- **.gitattributes**: Files you add are listed with `filter=eval-crypt diff=eval-crypt merge=eval-crypt`.
- **Key management**: A secret key is generated and stored locally (not committed).
- **Hooks**: Pre-commit and post-merge hooks ensure files are always in the right state.

## Example Workflow

```bash
eval-crypt init
# Add a file to be encrypted
echo "my secret" > secret.txt
eval-crypt add secret.txt
git add .gitattributes secret.txt
git commit -m "Add encrypted secret.txt"
# secret.txt is now encrypted in the repo, but plaintext locally
```

## Troubleshooting

- **File not decrypted?**
  - Make sure `.gitattributes` lists the file with `filter=eval-crypt`.
  - Check that your `.git/config` has the filter registered (run `eval-crypt init` again if needed).
  - Ensure `eval-crypt` is in your PATH and the key file exists.
- **Manual decryption:**
  ```bash
  cat secret.txt | eval-crypt smudge
  ```
- **Manual encryption:**
  ```bash
  cat secret.txt | eval-crypt clean
  ```

## Security Note
- The secret key is stored locally and should not be committed.
- Anyone with access to the key and the repo can decrypt the files.
- The tool is designed for research and collaboration, not for high-security use cases.

## Contributing
Contributions are welcome! Please open issues or pull requests.

## Credits
This project was developed as part of the MARS programme by Daniel Polatajko, Qi Guo, Matan Shtepel, with mentorship from Justin Olive.
