"""Compile and run representative shared snippet expansions."""

import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parent.parent / 'snippets'


def expand(body, values=None):
    """Expand the numbered subset used by this collection, for compilation."""
    values = dict(values or {})
    text = '\n'.join(body) if isinstance(body, list) else body

    def default(match):
        index = int(match[1])
        values.setdefault(index, match[2])
        return values[index]

    text = re.sub(r'\$\{(\d+):([^}]*)\}', default, text)
    return re.sub(r'\$(\d+)', lambda m: values.get(int(m[1]), ''), text)


class SnippetCompilationTests(unittest.TestCase):
    def snippets(self, language):
        path = SOURCE / (language + '.json')
        self.assertTrue(path.is_file(), 'Shared snippet source is not implemented')
        return json.loads(path.read_text(encoding='utf-8'))

    def compile_and_run(self, source, language, input_text=''):
        compiler, standard = ('gcc', 'c11') if language == 'c' else ('g++', 'c++17')
        if not shutil.which(compiler):
            self.skipTest(f'{compiler} unavailable')
        with tempfile.TemporaryDirectory(prefix='snippet ไทย ') as directory:
            root = Path(directory)
            path = root / ('program.' + language)
            binary = root / 'program'
            path.write_text(source, encoding='utf-8')
            build = subprocess.run([compiler, '-std=' + standard, str(path), '-o', str(binary)],
                                   capture_output=True, text=True, timeout=30)
            self.assertEqual(build.returncode, 0, build.stderr)
            run = subprocess.run([str(binary)], input=input_text, capture_output=True, text=True, timeout=5)
            self.assertEqual(run.returncode, 0, run.stderr)
            return run.stdout

    def test_c_main_compiles_and_exits_successfully(self):
        code = expand(self.snippets('c')['CP: Main']['body'])
        self.assertEqual(self.compile_and_run(code, 'c'), '')

    def test_cpp_main_compiles_and_exits_successfully(self):
        code = expand(self.snippets('cpp')['CP: Main']['body'])
        self.assertEqual(self.compile_and_run(code, 'cpp'), '')

    def test_cpp_template_shorthands_work_in_solution(self):
        snippets = self.snippets('cpp')
        self.assertIn('CP: Template', snippets)
        solution = '''vi a = {3, 1, 2};
    a.pb(4);
    sort(all(a));
    cout << a.front() << ' ';
    sort(rall(a));
    ll best = 10;
    cout << chmin(best, 5LL) << ' ' << chmin(best, 7LL) << ' ';
    cout << chmax(best, 8LL) << ' ' << chmax(best, 6LL) << ' ';
    pii p = {a.front(), sz(a)};
    vll big = {3000000000LL};
    cout << p.first << ' ' << p.second << ' ' << best << ' ' << big[0] << '\\n';'''
        code = expand(snippets['CP: Template']['body'], {1: solution})
        self.assertEqual(self.compile_and_run(code, 'cpp'), '1 1 0 1 0 4 4 8 3000000000\n')

    def test_cpp_template_test_cases_read_count_and_process_each_case(self):
        snippets = self.snippets('cpp')
        self.assertIn('CP: Template Test Cases', snippets)
        code = expand(snippets['CP: Template Test Cases']['body'],
                      {1: "ll x; cin >> x; cout << x * 2 << '\\n';"})
        self.assertEqual(self.compile_and_run(code, 'cpp', '3\n2\n5\n9\n'), '4\n10\n18\n')

    def test_c_loop_links_index_and_runs_three_iterations(self):
        loop = expand(self.snippets('c')['CP: For Loop']['body'], {0: 'total += 1;'})
        code = '#include <stdio.h>\nint main(void) { int n=3, total=0;\n' + loop
        code += '\nprintf("%d\\n", total); return 0; }\n'
        self.assertEqual(self.compile_and_run(code, 'c'), '3\n')

    def test_cpp_loop_links_index_and_runs_three_iterations(self):
        loop = expand(self.snippets('cpp')['CP: For Loop']['body'], {0: 'total += 1;'})
        code = '#include <iostream>\nint main() { int n=3, total=0;\n' + loop
        code += '\nstd::cout << total << "\\n"; return 0; }\n'
        self.assertEqual(self.compile_and_run(code, 'cpp'), '3\n')


if __name__ == '__main__':
    unittest.main()
