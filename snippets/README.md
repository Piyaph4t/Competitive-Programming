# Shared C/C++ snippets

Edit [c.json](c.json) or [cpp.json](cpp.json) here, then rerun the Python installer. These are the shared source files for Zed and VS Code.

| Prefix | Expansion |
| --- | --- |
| `cp-main` | C11 or C++17 program starter; C++ includes fast iostream setup |
| `cp-for` | Counted loop with an editable index and upper bound |
| `cp-template` | C++17 single-case starter with `solve()`, fast I/O, and shorthand helpers |
| `cp-template-tests` | Same C++17 starter, reading a test count and calling `solve()` for each case |

Type the prefix in a C or C++ file and select the snippet from completion suggestions, or use the editor's snippet picker. Tab moves between numbered placeholders; repeated `$1` positions edit together; `$0` marks the final cursor position.

## C++ CP templates

Expand `cp-template` in an empty `.cpp` file for a single-case problem, or `cp-template-tests` when the first input value is the number of test cases. The first placeholder puts you inside `solve()`; Tab moves to the final cursor position after `main()`. Keep per-case variables inside `solve()` so each test case starts fresh.

| Shorthand | Meaning / example |
| --- | --- |
| `ll` | `long long` |
| `pii` | `pair<int, int>` |
| `vi`, `vll` | `vector<int>`, `vector<ll>` |
| `all(v)` | Forward iterator range: `sort(all(v))` |
| `rall(v)` | Reverse iterator range: `sort(rall(v))` for descending order |
| `v.pb(x)` | `v.push_back(x)` |
| `sz(v)` | Container size converted to `int` |
| `chmin(a, b)` | Replace `a` with `b` if smaller; return whether it changed |
| `chmax(a, b)` | Replace `a` with `b` if larger; return whether it changed |

Use matching types for `chmin` and `chmax`, such as `chmin(best, 5LL)` when `best` is `ll`. Pass an existing container to `all`/`rall`; these macros evaluate their argument twice. The templates use standard C++17 headers and `using namespace std;`.

## Install

From the workspace root:

```bash
python script/install_snippets.py --editor both
python script/install_snippets.py --editor both --apply
```

The first command previews destinations without writing anything. The second installs. Use `--editor zed` or `--editor vscode` for only one editor. Python 3 is required; use `python3` if that is your interpreter command.

| Source | Zed destination filename | VS Code destination filename |
| --- | --- | --- |
| `c.json` | `c.json` | `c.json` |
| `cpp.json` | `c++.json` | `cpp.json` |

## Default directories

| OS | Zed | VS Code default profile |
| --- | --- | --- |
| Linux | `~/.config/zed/snippets` | `~/.config/Code/User/snippets` |
| macOS | `~/.config/zed/snippets` | `~/Library/Application Support/Code/User/snippets` |
| Windows | `%APPDATA%/Zed/snippets` | `%APPDATA%/Code/User/snippets` |

On Linux, `XDG_CONFIG_HOME` replaces `~/.config` when set. Supply a snippets directory explicitly for portable editors, nondefault VS Code profiles, or custom configurations:

```bash
python script/install_snippets.py --editor zed --zed-dir "path/to/zed/snippets" --apply
python script/install_snippets.py --editor vscode --vscode-dir "path/to/profile/snippets" --apply
```

## Existing snippets and backups

The installer retains unrelated entries and updates names that match the repository's `CP: ...` snippets. It accepts existing JSON with comments and trailing commas. All selected files are validated before any writes; malformed files, duplicate JSON keys, and destination-file symlinks stop installation.

Each changed existing file gets a unique sibling backup, such as `c.json.<unique-id>.bak`, with its exact original bytes. The installer prints each backup path. Merged output is regular formatted JSON: original comments and formatting remain in the backup. Reinstalling unchanged snippets writes nothing and creates no additional backup. Names removed from source files are not automatically pruned from your editor.

To restore a backup, copy its printed path over the original destination. For example, replace the paths below with the printed values:

```bash
python -c "import shutil; shutil.copyfile('path/to/c.json.unique-id.bak', 'path/to/c.json')"
```

Replacement is atomic per file. If an operating-system write error occurs partway through installation, earlier files may already be installed; use the printed backups to restore those files or rerun after fixing the error.

## Add a snippet

To generate an entry from a raw source file, use [the source-to-snippet CLI](../script/README.md#create-a-snippet-from-source):

```bash
python3 script/create_snippet.py templates/example.cpp --output snippets/cpp.json --name "CP: Example" --prefix cp-example
```

Rerun to update the named entry. Add `--placeholders` if your source already includes snippet tab stops.

Add a named `CP: ...` entry with a single string `prefix`, string or string-list `body`, and string `description`. Keep the repository files strict JSON. Use shared numbered placeholders such as `${1:i}`, `$1`, and `$0`; avoid editor-specific variables and transforms. Ordinary reusable algorithm code belongs in [templates/](../templates/README.md).

After editing, run `python -B -m unittest discover -s script -v`, commit the source changes, and rerun installation after pulling them on another computer.

Format references: [Zed](https://zed.dev/docs/snippets), [VS Code](https://code.visualstudio.com/docs/editing/userdefinedsnippets). See [computer synchronization](../docs/sync.md).
