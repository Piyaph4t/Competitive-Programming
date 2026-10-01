"""Exercise the source-to-snippet CLI without touching editor settings."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name('create_snippet.py')


class CreateSnippetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='source snippets ไทย ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'template.cpp'
        self.source.write_text('int main() {}\n', encoding='utf-8')
        self.output = self.root / 'nested' / 'cpp.json'

    def cli(self, *extra):
        return subprocess.run(
            [sys.executable, '-B', str(SCRIPT), str(self.source),
             '--output', str(self.output), '--name', 'CP: Example',
             '--prefix', 'cp-example', '--description', 'Example starter', *extra],
            capture_output=True, text=True, timeout=10)

    def test_create_preserves_literal_source_and_unicode(self):
        self.source.write_text('  print("ไทย $HOME ${1:x} \\n")\n\n', encoding='utf-8')
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = json.loads(self.output.read_text())['CP: Example']
        self.assertEqual(entry['prefix'], 'cp-example')
        self.assertEqual(entry['description'], 'Example starter')
        self.assertEqual(entry['body'], '  print("ไทย \\$HOME \\${1:x} \\\\n")\n\n')

    def test_placeholders_remain_active_when_requested(self):
        source = 'void solve() {\n    ${1:// solution}\n}\n$0\n'
        self.source.write_text(source, encoding='utf-8')
        result = self.cli('--placeholders')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.output.read_text())['CP: Example']['body'], source)

    def test_update_retains_other_entries_and_backs_up_exact_jsonc(self):
        self.output.parent.mkdir()
        original = b'{// personal\n"Other":{"prefix":"other","body":"hello"},\n"CP: Example":{"body":"old"},}\n'
        self.output.write_bytes(original)
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        entries = json.loads(self.output.read_text())
        self.assertEqual(entries['Other'], {'prefix': 'other', 'body': 'hello'})
        self.assertEqual(entries['CP: Example']['body'], 'int main() {}\n')
        backups = list(self.output.parent.glob('*.bak'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original)
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.output.parent.glob('*.bak')), backups)

    def test_invalid_destination_remains_untouched(self):
        self.output.parent.mkdir()
        for original in [b'{bad}', b'{"x":{},"x":{}}', b'[]']:
            with self.subTest(original=original):
                self.output.write_bytes(original)
                self.assertNotEqual(self.cli().returncode, 0)
                self.assertEqual(self.output.read_bytes(), original)
                self.assertEqual(list(self.output.parent.glob('*.bak')), [])

    def test_missing_source_does_not_create_output(self):
        self.source.unlink()
        self.assertNotEqual(self.cli().returncode, 0)
        self.assertFalse(self.output.parent.exists())

    def test_source_cannot_be_overwritten_by_output(self):
        self.output = self.source
        self.assertNotEqual(self.cli().returncode, 0)
        self.assertEqual(self.source.read_text(), 'int main() {}\n')

    def test_symlink_destination_is_rejected(self):
        self.output.parent.mkdir()
        self.output.symlink_to(self.source)
        self.assertNotEqual(self.cli().returncode, 0)
        self.assertTrue(self.output.is_symlink())
        self.assertEqual(self.source.read_text(), 'int main() {}\n')

    def test_empty_name_or_prefix_is_rejected(self):
        for flag in ['--name', '--prefix']:
            with self.subTest(flag=flag):
                self.assertNotEqual(self.cli(flag, ' ').returncode, 0)
                self.assertFalse(self.output.exists())
