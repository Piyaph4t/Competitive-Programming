# Directory migration verification

## Subsequent cleanup update

The user requested a Python cleanup tool in singular `script/` and simpler Zed tasks, while keeping only temporary C/C++ output in `build/`. The old Bash cleanup test and plural `scripts/` folder have been replaced. Its manifest entry is marked `retired`; the source and executable preservation records remain unchanged. Zed tasks now use direct compile-and-run commands with mirrored output paths.

## Original migration result

The approved platform-first directory structure is applied. Solution contents were not edited.

| Check | Observed result |
| --- | --- |
| Original file inventory | 29 C/C++ sources, 5 executables, 1 maintenance test |
| SHA-256 comparison with migration manifest | 35 of 35 original files unchanged |
| Source inventory after migration | 29 files; no duplicate or missing solutions |
| Navigation | All 29 sources indexed; 57 local README links resolve |
| Old directories | `CSES/`, `Codeforces/`, `TOI/`, `ท้ายค่าย 1/`, and `ask_ai/` removed after becoming empty |
| Source-adjacent binaries | None under `platforms/`, `training/`, or `practice/` |
| Zed configuration | Strict JSON parses; four original C/C++ Linux/Windows task labels retained |
| Linux C task | Centered Beautiful Matrix sample outputs `0`; binary appears under mirrored `build/` path |
| Linux C++ task | Sereja and Dima sample `4` with values `4 1 2 10` outputs `12 5`; binary appears under mirrored `build/` path |
| Path handling | Both Linux tasks pass in a temporary workspace whose path contains spaces and Thai characters |
| Failed compilation | Both Linux tasks exit nonzero without executing an existing stale binary |

The Linux commands were tested through both their configured shell command and direct invocation, with Zed-equivalent environment values. Actual interactive Zed execution was not performed. Task variable names and shell configuration were checked against the [official Zed task documentation](https://zed.dev/docs/tasks).

## Preservation record

[directory-migration.json](directory-migration.json) records each original path, destination, and original SHA-256 hash. Existing executables retain their original contents. The two verification builds add new output under `build/` without replacing a migrated executable.

[directory-migration-progress.md](directory-migration-progress.md) records task results and implementation rulings. No Git commits were possible because the exposed `.git` folder contains no repository metadata.

## Independent review

A fresh-context reviewer independently reran preservation, navigation, and Linux build checks and found no Critical, Important, or remaining Minor issues. The reviewer confirmed the [Zed task caller](https://raw.githubusercontent.com/zed-industries/zed/main/crates/terminal_view/src/terminal_panel.rs) uses raw shell argument joining, matching the Linux task quoting. Windows commands were checked statically. Historical pre-mutation collision and inventory checks rely on the executor’s observed results; current hashes were independently verified.

## Limits

- Windows/PowerShell tasks were inspected but cannot be executed in this Linux environment.
- At the original migration, the Bash cleanup test could not pass because its dependency was absent. It has since been replaced by the tested Python cleanup tool.
- This migration does not establish judge acceptance or algorithm correctness. Index status is `unverified`; TOI NSW's currently empty solution function is explicitly noted.

## Recheck preservation

Run from the workspace root:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, json

records = json.loads(Path('docs/directory-migration.json').read_text())
for record in records:
    if record.get('retired'):
        continue
    path = Path(record['new_path'])
    assert path.is_file(), path
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'], path
print('All active migration records preserved')
PY
```

After intentionally editing a solution or rebuilding an original binary, its hash will differ from this historical snapshot.
