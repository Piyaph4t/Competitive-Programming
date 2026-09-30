"""Preview or remove compiled binaries from build/, using only Python's stdlib."""

import argparse
import os
import sys
from pathlib import Path


def is_binary(path):
    """Recognize ELF, PE, and Mach-O headers without Unix permission checks."""
    with path.open('rb') as stream:
        header = stream.read(64)
        if header[:4] in {
            b'\x7fELF', b'\xfe\xed\xfa\xce', b'\xce\xfa\xed\xfe',
            b'\xfe\xed\xfa\xcf', b'\xcf\xfa\xed\xfe',
            b'\xca\xfe\xba\xbe', b'\xbe\xba\xfe\xca',
            b'\xca\xfe\xba\xbf', b'\xbf\xba\xfe\xca',
        }:
            return True
        if header[:2] == b'MZ' and len(header) == 64:
            stream.seek(int.from_bytes(header[60:64], 'little'))
            return stream.read(4) == b'PE\0\0'
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', type=Path,
                        default=Path(__file__).resolve().parent.parent / 'build',
                        help='directory to scan (default: this workspace\'s build/)')
    parser.add_argument('--delete', action='store_true',
                        help='delete matching binaries; otherwise only preview')
    args = parser.parse_args()
    directory = args.directory.absolute()
    if directory.is_symlink():
        parser.error('the scan directory must not be a symlink')
    if not directory.exists():
        print('No compiled binaries found.')
        return 0
    if not directory.is_dir():
        parser.error('the scan path must be a directory')

    count = 0
    try:
        def scan_error(error):
            raise error

        for root, dirs, files in os.walk(directory, followlinks=False,
                                         onerror=scan_error):
            dirs[:] = sorted(d for d in dirs if not d.startswith('.')
                             and not (Path(root) / d).is_symlink())
            for name in sorted(files):
                path = Path(root) / name
                if name.startswith('.') or path.is_symlink() or not path.is_file():
                    continue
                if not is_binary(path):
                    continue
                if args.delete:
                    path.unlink()
                print(f'{"Deleted" if args.delete else "Would delete"}: {path}')
                count += 1
    except OSError as error:
        print(f'Cleanup failed: {error}', file=sys.stderr)
        return 1
    if count == 0:
        print('No compiled binaries found.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
