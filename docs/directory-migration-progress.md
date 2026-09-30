# SDD ledger — plan: docs/superpowers/plans/2026-10-01-directory-structure.md

Pre-flight: Task 1 manifest produces old_path/new_path/sha256 consumed by Task 2 indexes and Task 3 preservation checks; compatible. Task 3 consumes existing Zed task configuration; available.

Ruling: Git-backed workspaces, task helpers, commits, and final cleanup are unavailable because .git contains no repository metadata — execute in the user-authorized folder, use /tmp/cp-directory-migration for temporary tooling, and retain this ledger in docs — cost if wrong: no Git rollback; the hash manifest provides an explicit inverse move map.
Ruling: Inventory contains five executables rather than six — preserve the actual five and check all inventoried files — cost if wrong: an unlisted file could be missed; coverage checks compare against the complete old directories.
Ruling: This is a filesystem/documentation migration with no solution code changes — use hash and link verification rather than adding permanent tests mirroring the layout; use a failing behavioral build check before editing tasks — cost if wrong: future rearrangements require rerunning the documented checks.

Task 1: complete — 35/35 hashes match, 29 source files preserved, obsolete directories removed only after becoming empty.

Task 2: complete — 29/29 solutions indexed, all README links resolve, .gitignore isolates build output. TOI NSW is explicitly unclassified because its solve function is empty.

Task 3: Ruling: Use the explicit PowerShell task shell to execute the Windows command directly, rather than nesting powershell -Command — avoids a second native-argument quoting layer while preserving platform behavior — cost if wrong: Windows task invocation requires checking on Windows; not executable in this environment.
Task 3: RED observed — existing Linux C task produced correct sample output but failed the mirrored-build-location assertion.

Task 3: complete — task JSON parses; Linux C/C++ tasks passed sample outputs 0 and 12 5 in this root and a temporary root with spaces and Thai characters; all 35 original file hashes and 57 links remain valid. Windows task execution unavailable; missing cleanup dependency documented.

Final verification: Linux failed-compilation checks pass for C/C++, with no stale binary execution. Verification report saved to docs/directory-migration-verification.md.

Final review: independent fresh-context reviewer — no Critical, Important, or remaining Minor findings. Reviewer reran hash/layout checks and Linux sample builds, and confirmed Zed task caller uses build_no_quote.
Final: Ruling: Algorithm correctness and judge acceptance remain outside migration scope — keep all source bytes unchanged and statuses unverified — cost if wrong: existing solution bugs remain.
Final: Ruling: Windows and interactive Zed execution cannot be verified here — accept static Windows inspection and equivalent-shell Linux execution — cost if wrong: an editor or Windows integration issue may need a follow-up.
Final: Ruling: Reviewer cannot reconstruct historical collision preflight or completeness from the final tree — accept executor-observed pre-mutation inventory and collision checks, independently matched current hashes — cost if wrong: historical omissions cannot be detected solely by the manifest.
Finish: using finishing-a-development-branch; no Git branch exists, so merge/push menus and workspace deletion do not apply. Updated folder and permanent migration evidence are retained.

Follow-up: user requested portable Python cleanup under singular script/ and simple Zed commands, with build/ containing only temporary C/C++ output. Added script/clean_build.py and five Python behavioral tests; replaced obsolete Bash test; retired its historical manifest entry. Direct tasks retain four platform/language labels and mirrored build paths.
Follow-up verification: 5/5 Python tests pass after initial missing-implementation failures; preview from another working directory targets this workspace build/; Linux C/C++ samples and failed-compilation stale-output checks pass; 34 active original hashes match; 58 README links resolve. Existing binaries were previewed only, not deleted. Windows tasks statically checked only.
