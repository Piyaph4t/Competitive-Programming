"""Create or update a Zed/VS Code JSON snippet from a UTF-8 source file."""

import argparse
import sys
from pathlib import Path

from install_snippets import InstallPlan, apply_install, parse_jsonc


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='raw source file (.c, .cpp, .py, etc.)')
    parser.add_argument('--output', required=True, type=Path, help='destination snippet JSON file')
    parser.add_argument('--name', required=True, help='snippet entry name; matching entry is updated')
    parser.add_argument('--prefix', required=True, help='completion trigger')
    parser.add_argument('--description', default='', help='completion description')
    parser.add_argument('--placeholders', action='store_true',
                        help='treat source as snippet syntax, preserving placeholders and escapes')
    args = parser.parse_args(argv)

    try:
        if not args.name.strip() or not args.prefix.strip():
            raise ValueError('--name and --prefix must not be blank')
        source = args.source.expanduser().absolute()
        output = args.output.expanduser().absolute()
        if output.is_symlink():
            raise ValueError(f'Refusing symlink destination: {output}')
        if source.resolve() == output.resolve() or (output.exists() and source.samefile(output)):
            raise ValueError('Source and output must be different files')

        # Normalize line endings while retaining indentation and terminal blank lines.
        body = source.read_text(encoding='utf-8-sig')
        if not args.placeholders:
            body = body.replace('\\', '\\\\').replace('$', '\\$')

        original = output.read_bytes() if output.exists() else None
        existing = parse_jsonc(original.decode('utf-8-sig')) if original is not None else {}
        merged = dict(existing)
        merged[args.name] = {
            'prefix': args.prefix,
            'body': body,
            'description': args.description,
        }
        changed = original is None or merged != existing
        plan = InstallPlan(output, original, merged, 1, changed)
        if changed:
            apply_install([plan])
        else:
            print(f'Unchanged: {output}')
        return 0
    except (OSError, ValueError) as error:
        print(f'Snippet creation failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
