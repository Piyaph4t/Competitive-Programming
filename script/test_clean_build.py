"""Run with: python -m unittest discover -s script -v."""
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('clean_build.py')


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cp build ไทย ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.elf = self.root / 'nested' / 'program with spaces'
        self.elf.parent.mkdir()
        self.elf.write_bytes(b'\x7fELF' + bytes(60))
        self.pe = self.root / 'program.exe'
        header = bytearray(64)
        header[:2] = b'MZ'
        struct.pack_into('<I', header, 60, 64)
        self.pe.write_bytes(header + b'PE\0\0')
        self.macho = self.root / 'mac-program'
        self.macho.write_bytes(b'\xcf\xfa\xed\xfe' + bytes(60))
        self.source = self.root / 'source.cpp'
        self.source.write_text('int main() { return 0; }\n')
        self.shell = self.root / 'helper.sh'
        self.shell.write_text('#!/bin/sh\necho hello\n')
        self.shell.chmod(0o755)
        self.fake_exe = self.root / 'notes.exe'
        self.fake_exe.write_text('Not a binary\n')

    def run_script(self, *args):
        self.assertTrue(SCRIPT.is_file(), 'Python cleanup script is not implemented')
        return subprocess.run([sys.executable, str(SCRIPT), str(self.root), *args],
                              capture_output=True, text=True, timeout=10)

    def test_preview_lists_formats_without_deleting_anything(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        for binary in (self.elf, self.pe, self.macho):
            self.assertIn(str(binary), result.stdout)
            self.assertTrue(binary.exists())
        for other in (self.source, self.shell, self.fake_exe):
            self.assertNotIn(str(other), result.stdout)
            self.assertTrue(other.exists())

    def test_delete_removes_binaries_and_preserves_sources_and_scripts(self):
        result = self.run_script('--delete')
        self.assertEqual(result.returncode, 0, result.stderr)
        for binary in (self.elf, self.pe, self.macho):
            self.assertFalse(binary.exists())
        for other in (self.source, self.shell, self.fake_exe):
            self.assertTrue(other.exists())

    def test_symlink_files_and_directories_are_not_followed(self):
        with tempfile.TemporaryDirectory() as d:
            external = Path(d) / 'external-program'
            external.write_bytes(b'\x7fELF' + bytes(60))
            try:
                (self.root / 'linked-program').symlink_to(external)
                (self.root / 'linked-directory').symlink_to(d, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest('Symlink creation unavailable')
            result = self.run_script('--delete')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(external.exists())
            self.assertTrue((self.root / 'linked-program').is_symlink())

    def test_hidden_metadata_is_preserved(self):
        hidden = self.root / '.metadata'
        hidden.mkdir()
        binary = hidden / 'program'
        binary.write_bytes(b'\x7fELF' + bytes(60))
        result = self.run_script('--delete')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(binary.exists())

    def test_nonexistent_directory_is_a_noop(self):
        self.assertTrue(SCRIPT.is_file(), 'Python cleanup script is not implemented')
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.root / 'absent')],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
