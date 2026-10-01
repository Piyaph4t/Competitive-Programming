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

## Create a snippet from source

[create_snippet.py](create_snippet.py) creates or updates one named snippet from any UTF-8 source file, including C, C++, and Python. It uses Python 3's standard library.

```bash
python3 script/create_snippet.py templates/example.cpp \
  --output snippets/cpp.json \
  --name "CP: Example" \
  --prefix cp-example \
  --description "My C++ starter"

python3 script/create_snippet.py scratch/example.py \
  --output snippets/python.json \
  --name "Python: Example" \
  --prefix py-example
```

`--output`, `--name`, and `--prefix` are required. `--description` defaults to an empty string. Paths are relative to your current directory. Missing output directories are created. Rerun the same command after editing the source to update that entry; other entries are retained.

By default, source is literal text: dollar signs and backslashes are escaped for snippet expansion. Indentation, blank lines, and the final newline are retained; line endings become LF. Use `--placeholders` when the source already contains snippet syntax such as `${1:// solution}` or `$0`. In that mode, escapes must also follow snippet syntax.

Existing JSON with comments and trailing commas is accepted. Output is formatted strict JSON, compatible with Zed language snippet files and VS Code language snippet files. Pick the destination filename for the editor/language, such as `cpp.json` for VS Code or `c++.json` for Zed. VS Code global `.code-snippets` files may additionally need a `scope` field, which this tool does not add.

Changed existing files receive an exact sibling `.bak` backup before atomic replacement. An unchanged entry creates no backup. Invalid JSON, duplicate JSON keys, output symlinks, and using the same file for source and output are rejected without replacing the destination.

The existing installer distributes only `snippets/c.json` and `snippets/cpp.json`; for other languages, pass your editor's language snippet path to `--output` or copy the resulting JSON there. Use `CP: ...` names for entries in the shared C/C++ files to meet the installer's naming convention.

[Workspace conventions](../README.md)
