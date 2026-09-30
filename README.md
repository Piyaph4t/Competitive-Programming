# Competitive Programming

Browse by [platform](platforms/README.md), [camp](training/README.md), or [practice topic](practice/README.md). Each solution has one home; indexes list additional topics.

```text
.
├── platforms/
│   ├── cses/                  # Official problem-set categories
│   ├── codeforces/            # Primary algorithm topic
│   └── toi/toi05/             # Competition edition
├── training/camp-1/problems/  # Camp assignments
├── practice/basics/           # Independent exercises
├── notes/                    # Learning notes
├── templates/                # Reusable algorithms
├── snippets/                 # Shared Zed and VS Code expansions
├── scratch/                  # Temporary experiments
├── script/                   # Cleanup and snippet installation
├── docs/                     # Structure and migration records
├── build/                    # Generated output (ignored)
├── .zed/                     # Editor tasks
└── .clang-format
```

| Area | Navigation |
| --- | --- |
| CSES | [Problems and topics](platforms/cses/README.md) |
| Codeforces | [Problems and topics](platforms/codeforces/README.md) |
| TOI | [Problems by edition](platforms/toi/README.md) |
| Training | [Camp assignments](training/README.md) |
| Practice | [Independent exercises](practice/README.md) |
| Shared material | [Notes](notes/README.md), [templates](templates/README.md) |
| Editor snippets | [Shared C/C++ snippets](snippets/README.md) |
| Computer synchronization | [Git workflow](docs/sync.md) |
| Working area | [Scratch](scratch/README.md), [script](script/README.md) |
| Migration | [Original-to-new paths](docs/directory-migration.json) |

## Naming and organization

- Use lowercase kebab-case: `sorting-and-searching`, `gray-code.cpp`.
- Preserve official problem identifiers. Codeforces: `<id>-<title>.<ext>`; TOI: `toi<edition>-<name>.<ext>`; camp work: retain the camp identifier.
- CSES follows official categories; Codeforces follows one primary topic; TOI follows edition. Camp work stays together and uses topic tags in its index.
- Use consistent tags: `implementation`, `math`, `strings`, `sorting`, `binary-search`, `two-pointers`, `sliding-window`, `greedy`, `dynamic-programming`, `graphs`, `trees`, `range-queries`. Add a specific tag such as `simulation` when useful.
- Store a solution once and list secondary topics in its index. Keep a single source file unless samples, notes, or multiple implementations justify a problem directory.
- `unverified` means judge acceptance has not been checked; update it only with evidence of acceptance.

## Add a problem

1. Choose its platform and category, primary topic, or edition. Use `training/` for camp assignments and `practice/` for independent exercises.
2. Add the source using the naming rules above.
3. Add a relative solution link, topic tags, and status to that area's README.
4. Put explanation notes or sample files beside the solution only when needed.

## Build and run

Open this root folder in Zed. Select the C or C++ Compile & Run task matching your operating system. GCC/G++ must be available on PATH. Tasks retain C11/C++17, `-DDEBUG`, and `-O2` and create binaries under `build/` with the source's relative path.

For example, `platforms/codeforces/binary-search/706b-interesting-drink.cpp` builds to `build/platforms/codeforces/binary-search/706b-interesting-drink` on Linux, or the same path with `.exe` on Windows. Do not place binaries beside source files.

## Clean temporary builds

The `build/` folder contains only disposable C/C++ build output. The portable cleanup tool lives in `script/`, outside that folder.

```bash
python script/clean_build.py           # Preview
python script/clean_build.py --delete  # Delete compiled binaries
```

Use `python3` if that is your Python 3 command. See [cleanup usage](script/README.md).

## Snippets and computer synchronization

Snippet sources live in `snippets/`; install them into either editor using Python:

```bash
python script/install_snippets.py --editor both          # Preview
python script/install_snippets.py --editor both --apply  # Install
```

Expand `cp-main` for a program starter or `cp-for` for a counted loop. See [snippet usage](snippets/README.md), including editor paths, backups, and profile overrides.

Use the [Git synchronization guide](docs/sync.md) to add a remote and work across computers. Local commits preserve history; synchronization requires pushing to and pulling from your remote.
