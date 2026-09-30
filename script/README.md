# Script

[clean_build.py](clean_build.py) previews or deletes compiled binaries in this workspace's `build/` folder. It uses Python 3's standard library and detects ELF, PE, and Mach-O headers instead of operating-system permission bits.

From the workspace root:

```bash
python script/clean_build.py
python script/clean_build.py --delete
```

The first command only lists matching files. The second deletes them. Sources, text files, scripts, symlinks, and hidden metadata are skipped. Empty directories remain. `build/` is reserved for temporary C/C++ output; keep scripts and permanent materials elsewhere.

An optional directory can be supplied: `python script/clean_build.py build/output`. The default is this workspace's `build/`, even when called from another working directory. Use `python3` if that is your Python 3 command.

Run all cleanup, snippet, and installer tests with:

```bash
python -B -m unittest discover -s script -v
```

Zed tasks remain direct compiler commands. They create mirrored output directories under `build/`, compile, and run only after successful compilation.

## Snippet installer

[install_snippets.py](install_snippets.py) reads the shared C/C++ sources in [snippets/](../snippets/README.md), previews changes by default, and installs when `--apply` is supplied:

```bash
python script/install_snippets.py --editor both
python script/install_snippets.py --editor both --apply
```

Select `--editor zed` or `--editor vscode` to target only one editor. `--zed-dir` and `--vscode-dir` override their snippets directories. Changed existing files are backed up before replacement, and unrelated snippet entries are retained. See [complete usage and restoration](../snippets/README.md).

[Workspace conventions](../README.md)
