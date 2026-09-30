"""Preview or install this workspace's shared snippets into Zed and VS Code."""

import argparse
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


def _object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f'Invalid JSON constant: {value}')


def _load_object(text):
    value = json.loads(text, object_pairs_hook=_object_pairs,
                       parse_constant=_reject_constant)
    if not isinstance(value, dict):
        raise ValueError('Snippet file must contain a JSON object')
    return value


def parse_jsonc(text):
    """Remove comments and trailing commas while leaving JSON strings intact."""
    chars = list(text)
    in_string = False
    escaped = False
    index = 0
    while index < len(chars):
        char = chars[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
        elif char == '/' and index + 1 < len(chars):
            following = chars[index + 1]
            if following == '/':
                end = index + 2
                while end < len(chars) and chars[end] not in '\r\n':
                    end += 1
                chars[index:end] = [' '] * (end - index)
                index = end
                continue
            if following == '*':
                end = text.find('*/', index + 2)
                if end < 0:
                    raise ValueError('Unterminated JSON comment')
                end += 2
                for position in range(index, end):
                    if chars[position] not in '\r\n':
                        chars[position] = ' '
                index = end
                continue
        index += 1

    in_string = False
    escaped = False
    for index, char in enumerate(chars):
        if in_string:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == ',':
            end = index + 1
            while end < len(chars) and chars[end].isspace():
                end += 1
            previous = index - 1
            while previous >= 0 and chars[previous].isspace():
                previous -= 1
            # A comma after an opener/colon/comma is invalid, not trailing.
            if (end < len(chars) and chars[end] in '}]' and previous >= 0
                    and chars[previous] not in '{[,:'):
                chars[index] = ' '
    return _load_object(''.join(chars))


def default_snippet_dir(editor, platform, environ, home):
    if editor not in ('zed', 'vscode'):
        raise ValueError(f'Unknown editor: {editor}')
    if platform == 'win32':
        appdata = environ.get('APPDATA')
        if not appdata:
            raise ValueError('APPDATA is missing; supply --zed-dir or --vscode-dir')
        root = Path(appdata)
        return root / ('Zed' if editor == 'zed' else 'Code/User') / 'snippets'
    if platform == 'darwin':
        root = home / '.config' if editor == 'zed' else home / 'Library/Application Support'
    else:
        root = Path(environ.get('XDG_CONFIG_HOME') or home / '.config')
    return root / ('zed' if editor == 'zed' else 'Code/User') / 'snippets'


def _validate_source(snippets, path):
    for name, snippet in snippets.items():
        if not name.startswith('CP: ') or not isinstance(snippet, dict):
            raise ValueError(f'{path}: snippets require CP: names and object values')
        prefix = snippet.get('prefix')
        body = snippet.get('body')
        description = snippet.get('description')
        valid_body = isinstance(body, str) or (
            isinstance(body, list) and all(isinstance(line, str) for line in body))
        if not isinstance(prefix, str) or not prefix.strip() or not valid_body:
            raise ValueError(f'{path}: {name} requires a string prefix and string/list body')
        if not isinstance(description, str):
            raise ValueError(f'{path}: {name} requires a string description')


@dataclass
class InstallPlan:
    path: Path
    original: Optional[bytes]
    merged: dict
    managed_count: int
    changed: bool


def plan_install(source_dir, destinations):
    sources = {}
    for filename in ('c.json', 'cpp.json'):
        path = source_dir / filename
        try:
            sources[filename] = _load_object(path.read_text(encoding='utf-8'))
            _validate_source(sources[filename], path)
        except (OSError, ValueError) as error:
            raise ValueError(f'Cannot load source {path}: {error}') from error

    plans = []
    seen = set()
    for editor, directory in destinations.items():
        if editor not in ('zed', 'vscode'):
            raise ValueError(f'Unknown editor: {editor}')
        for filename, snippets in sources.items():
            target = 'c++.json' if editor == 'zed' and filename == 'cpp.json' else filename
            path = directory / target
            if path.is_symlink():
                raise ValueError(f'Refusing symlink destination: {path}')
            key = path.resolve()
            if key in seen:
                raise ValueError(f'Editors share a destination file: {path}')
            seen.add(key)
            try:
                original = path.read_bytes() if path.exists() else None
                existing = parse_jsonc(original.decode('utf-8-sig')) if original is not None else {}
            except (OSError, ValueError) as error:
                raise ValueError(f'Cannot load destination {path}: {error}') from error
            merged = dict(existing)
            merged.update(snippets)
            plans.append(InstallPlan(path, original, merged, len(snippets),
                                     original is None or merged != existing))
    return plans


def apply_install(plans):
    # Recheck all snapshots before any mutation to avoid replacing intervening edits.
    for plan in plans:
        if plan.path.is_symlink():
            raise ValueError(f'Refusing symlink destination: {plan.path}')
        current = plan.path.read_bytes() if plan.path.exists() else None
        if current != plan.original:
            raise ValueError(f'Destination changed since preview: {plan.path}')

    backups = []
    for plan in plans:
        if not plan.changed:
            continue
        plan.path.parent.mkdir(parents=True, exist_ok=True)
        if plan.original is not None:
            descriptor, name = tempfile.mkstemp(prefix=plan.path.name + '.', suffix='.bak',
                                               dir=plan.path.parent)
            backup = Path(name)
            with os.fdopen(descriptor, 'wb') as stream:
                stream.write(plan.original)
            backups.append(backup)
            print(f'Backup: {backup}')

        descriptor, name = tempfile.mkstemp(prefix='.' + plan.path.name + '.', suffix='.tmp',
                                           dir=plan.path.parent)
        temporary = Path(name)
        try:
            with os.fdopen(descriptor, 'w', encoding='utf-8', newline='\n') as stream:
                json.dump(plan.merged, stream, indent=2, ensure_ascii=False)
                stream.write('\n')
            os.replace(temporary, plan.path)
        finally:
            if temporary.exists():
                temporary.unlink()
        print(f'Installed: {plan.path}')
    return backups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--editor', choices=('zed', 'vscode', 'both'), default='both')
    parser.add_argument('--zed-dir', type=Path, help='override Zed snippets directory')
    parser.add_argument('--vscode-dir', type=Path, help='override VS Code snippets directory')
    parser.add_argument('--apply', action='store_true', help='write changes (default: preview)')
    args = parser.parse_args()
    try:
        destinations = {}
        editors = ('zed', 'vscode') if args.editor == 'both' else (args.editor,)
        for editor in editors:
            override = getattr(args, editor + '_dir')
            destinations[editor] = override.expanduser().absolute() if override is not None else (
                default_snippet_dir(editor, sys.platform, os.environ, Path.home()))
        source_dir = Path(__file__).resolve().parent.parent / 'snippets'
        plans = plan_install(source_dir, destinations)
        for plan in plans:
            status = 'changed' if plan.changed else 'unchanged'
            print(f'{plan.path}: {status}; {plan.managed_count} managed snippets')
        if args.apply:
            apply_install(plans)
        else:
            print('Preview only. Use --apply to install.')
        return 0
    except (OSError, ValueError) as error:
        print(f'Installation failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
