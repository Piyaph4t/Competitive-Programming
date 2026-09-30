"""Installer tests use temporary directories, never real editor settings."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name('install_snippets.py').resolve()
SOURCES = SCRIPT.parent.parent / 'snippets'


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'Python snippet installer is not implemented')
        spec = importlib.util.spec_from_file_location('snippet_installer', SCRIPT)
        self.installer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.installer)
        self.temp = tempfile.TemporaryDirectory(prefix='snippets ไทย ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.zed = self.root / 'zed snippets'
        self.vscode = self.root / 'vscode profile snippets'

    def cli(self, *args, cwd=None):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), '--editor', 'both',
                               '--zed-dir', str(self.zed), '--vscode-dir', str(self.vscode),
                               *args], cwd=cwd, capture_output=True, text=True, timeout=10)

    def test_default_paths_for_all_platforms(self):
        cases = [
            ('zed', 'linux', {}, Path('/home/test/.config/zed/snippets')),
            ('vscode', 'linux', {}, Path('/home/test/.config/Code/User/snippets')),
            ('zed', 'linux', {'XDG_CONFIG_HOME': '/custom'}, Path('/custom/zed/snippets')),
            ('vscode', 'linux', {'XDG_CONFIG_HOME': '/custom'}, Path('/custom/Code/User/snippets')),
            ('zed', 'darwin', {}, Path('/home/test/.config/zed/snippets')),
            ('vscode', 'darwin', {}, Path('/home/test/Library/Application Support/Code/User/snippets')),
            ('zed', 'win32', {'APPDATA': 'C:/Roaming'}, Path('C:/Roaming/Zed/snippets')),
            ('vscode', 'win32', {'APPDATA': 'C:/Roaming'}, Path('C:/Roaming/Code/User/snippets')),
        ]
        for editor, platform, env, want in cases:
            with self.subTest(editor=editor, platform=platform, env=env):
                self.assertEqual(self.installer.default_snippet_dir(editor, platform, env, Path('/home/test')), want)

    def test_missing_windows_appdata_is_an_error(self):
        with self.assertRaisesRegex(ValueError, 'APPDATA'):
            self.installer.default_snippet_dir('zed', 'win32', {}, self.root)

    def test_jsonc_preserves_comment_like_strings_and_escaped_quotes(self):
        text = r'''{
          // actual comment
          "Personal": {"body": ["https://example.com/a//b", "/* literal */", "say \"hello\""],},
          /* another comment */
        }'''
        self.assertEqual(self.installer.parse_jsonc(text), {
            'Personal': {'body': ['https://example.com/a//b', '/* literal */', 'say "hello"']}})

    def test_duplicate_keys_and_malformed_jsonc_are_rejected(self):
        for text in ['{"x": {}, "x": {}}', '{"x": {"body": 1, "body": 2}}',
                     '{not json}', '{"x": 1 /* unterminated', '[1,2]', '{"x": NaN}']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.installer.parse_jsonc(text)

    def test_comma_without_a_previous_value_is_not_a_trailing_comma(self):
        for text in ['{,}', '{/* comment */,}', '{,/* comment */}',
                     '{"Personal":{"body":[,]}}',
                     '{"Personal":{"body":[/* comment */, /* comment */]}}']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.installer.parse_jsonc(text)

    def test_preview_creates_no_directories(self):
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('c++.json', result.stdout)
        self.assertIn('cpp.json', result.stdout)
        self.assertFalse(self.zed.exists())
        self.assertFalse(self.vscode.exists())

    def test_install_maps_language_files_and_preserves_placeholders(self):
        result = self.cli('--apply', cwd=self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        for directory, cpp_name in [(self.zed, 'c++.json'), (self.vscode, 'cpp.json')]:
            cpp = json.loads((directory / cpp_name).read_text())
            self.assertIn('cp-main', [value['prefix'] for value in cpp.values()])
            loop = cpp['CP: For Loop']['body'][0]
            self.assertIn('${1:i}', loop)
            self.assertIn('$1', loop)
            self.assertTrue((directory / 'c.json').is_file())
        self.assertFalse((self.zed / 'cpp.json').exists())
        self.assertFalse((self.vscode / 'c++.json').exists())

    def test_merge_preserves_personal_entries_and_exact_backup(self):
        self.zed.mkdir()
        path = self.zed / 'c.json'
        original = b'{\r\n// personal comment\r\n"Personal": {"prefix":"mine","body":"hello // world"},\r\n}\r\n'
        path.write_bytes(original)
        result = self.cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        content = json.loads(path.read_text())
        self.assertEqual(content['Personal'], {'prefix': 'mine', 'body': 'hello // world'})
        backups = list(self.zed.glob('c.json.*.bak'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original)
        self.assertIn(str(backups[0]), result.stdout)

    def test_repeat_install_is_a_noop_with_no_new_backup(self):
        self.assertEqual(self.cli('--apply').returncode, 0)
        paths = [self.zed / 'c.json', self.zed / 'c++.json',
                 self.vscode / 'c.json', self.vscode / 'cpp.json']
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths}
        result = self.cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('unchanged', result.stdout)
        for p in paths:
            self.assertEqual((p.read_bytes(), p.stat().st_mtime_ns), before[p])
        self.assertFalse(list(self.root.rglob('*.bak')))

    def test_update_replaces_managed_entry_but_retains_other_names(self):
        source = self.root / 'sources'
        source.mkdir()
        for language in ('c', 'cpp'):
            (source / (language + '.json')).write_bytes((SOURCES / (language + '.json')).read_bytes())
        self.zed.mkdir()
        path = self.zed / 'c.json'
        path.write_text('{"CP: Main":{"prefix":"old","body":"old"},"CP: Removed":{"body":"keep"}}')
        plans = self.installer.plan_install(source, {'zed': self.zed})
        self.installer.apply_install(plans)
        merged = json.loads(path.read_text())
        self.assertEqual(merged['CP: Main']['prefix'], 'cp-main')
        self.assertEqual(merged['CP: Removed'], {'body': 'keep'})

    def test_invalid_last_destination_prevents_all_writes_and_backups(self):
        self.zed.mkdir()
        original = b'{"Personal": {"body": "unchanged"}}'
        (self.zed / 'c.json').write_bytes(original)
        self.vscode.mkdir()
        (self.vscode / 'cpp.json').write_text('invalid')
        result = self.cli('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.zed / 'c.json').read_bytes(), original)
        self.assertFalse((self.zed / 'c++.json').exists())
        self.assertFalse((self.vscode / 'c.json').exists())
        self.assertFalse(list(self.root.rglob('*.bak')))

    def test_malformed_empty_last_destination_prevents_earlier_installation(self):
        self.zed.mkdir()
        self.vscode.mkdir()
        original = b'{"Personal": {"body": "unchanged"}}'
        (self.zed / 'c.json').write_bytes(original)
        for malformed in ['{,}', '{/* comment */,}', '{"Personal":{"body":[,]}}']:
            (self.vscode / 'cpp.json').write_text(malformed)
            with self.subTest(malformed=malformed):
                result = self.cli('--apply')
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual((self.zed / 'c.json').read_bytes(), original)
                self.assertFalse((self.zed / 'c++.json').exists())
                self.assertFalse((self.vscode / 'c.json').exists())
                self.assertFalse(list(self.root.rglob('*.bak')))

    def test_invalid_source_schema_is_rejected(self):
        source = self.root / 'sources'
        source.mkdir()
        (source / 'cpp.json').write_bytes((SOURCES / 'cpp.json').read_bytes())
        for raw in ['{"Not namespaced": {"prefix":"x","body":"x","description":"x"}}',
                    '{"CP: Bad": {"prefix":["x","y"],"body":"x","description":"x"}}',
                    '{"CP: Bad": {"prefix":"x","body":[1],"description":"x"}}',
                    '{"CP: Bad": {"prefix":"x","body":"x","description":false}}',
                    '// comment\n{}']:
            (source / 'c.json').write_text(raw)
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.installer.plan_install(source, {'zed': self.zed})
        self.assertFalse(self.zed.exists())

    def test_symlink_destination_is_rejected(self):
        self.zed.mkdir()
        external = self.root / 'external.json'
        external.write_text('{}')
        try:
            (self.zed / 'c.json').symlink_to(external)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        result = self.cli('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('symlink', result.stderr.lower())
        self.assertEqual(external.read_text(), '{}')
        self.assertFalse(self.vscode.exists())

    def test_preview_preserves_existing_jsonc_bytes(self):
        self.zed.mkdir()
        path = self.zed / 'c.json'
        original = b'{/*comment*/"Personal":{"body":"// text"},}'
        path.write_bytes(original)
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse(list(self.root.rglob('*.bak')))


if __name__ == '__main__':
    unittest.main()
