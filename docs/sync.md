# Git synchronization between computers

This folder is set up for local Git history. A remote will be added later: local commits alone do not synchronize computers. `build/`, temporary scratch contents, Python caches, and local agent/credential folders are ignored. Solutions, shared snippets, scripts, documentation, and editor tasks are tracked.

## Save work locally

From the workspace root:

```bash
git status
git add platforms training practice notes templates snippets script docs README.md .zed .clang-format .gitignore .gitattributes
git diff --cached --stat
git commit -m "Solve problems and update practice notes"
```

Review `git status` before committing. Git preserves file history; ignored build output can be regenerated on each computer.

## Add a remote when ready

Create an empty repository on your Git hosting service, then substitute its URL below:

```bash
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

If `origin` already exists, inspect `git remote -v` before changing it. An existing remote with its own commits needs reconciliation before the first push; do not force-push to overwrite it. No remote or automatic push is configured by this setup.

## Start on another computer

Install Git, Python 3, and GCC/G++ for C/C++ compilation, then:

```bash
git clone YOUR_REPOSITORY_URL competitive-programming
cd competitive-programming
python script/install_snippets.py --editor both
python script/install_snippets.py --editor both --apply
```

Use `python3` where appropriate. Select only your installed editor with `--editor zed` or `--editor vscode`, and use the [directory overrides](../snippets/README.md) for a custom profile. Clone into a normal writable directory. The installer creates machine-local copies; source snippets remain in the repository.

## Each time you switch computers

Before editing, check the working tree and pull the remote's current history:

```bash
git status
git pull --ff-only
```

Commit or otherwise preserve local edits before pulling. If `--ff-only` fails because both computers have new commits, inspect the histories and resolve them before continuing; do not use hard reset or force push to discard work.

After working:

```bash
git add platforms training practice notes templates snippets script docs README.md .zed .clang-format .gitignore .gitattributes
git diff --cached --stat
git commit -m "Describe today's changes"
git push
```

Push before switching computers so the other machine can pull your changes. After pulling snippet changes, rerun `python script/install_snippets.py --editor both --apply`. The installer does not change unrelated editor snippets and keeps backups of changed files.

Git stores normalized text line endings according to `.gitattributes`. New checkouts use LF for source, snippet, and script files on all computers. Existing solution files are not rewritten during repository setup.

[Workspace navigation](../README.md) · [Snippet installation](../snippets/README.md)
