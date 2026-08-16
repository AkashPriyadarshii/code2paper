import unittest
import tempfile
from pathlib import Path
from unittest import mock
from code2paper import (
    parse_gitignore, is_ignored, iter_source_files, scan_file,
    analyze_python, analyze_generic, build_report, pack_codebase,
    typst_escape, latex_escape, generate_paper_source,
    generate_latex_source, generate_html_paper_source, generate_markdown_source,
    build_deps, OUTPUT_BASENAMES,
)


def make_repo(files: dict, gitignore: str = None) -> Path:
    tmp = Path(tempfile.mkdtemp())
    for rel, content in files.items():
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    if gitignore is not None:
        (tmp / ".gitignore").write_text(gitignore, encoding="utf-8")
    return tmp


SAMPLE_PY = '''import os
from json import dumps

class Greeter:
    def greet(self, name: str) -> str:
        return f"hi {name}"

def main():
    for i in range(10):
        if i % 2 == 0:
            print(dumps(i))
    return os.getcwd()
'''


class TestGitignore(unittest.TestCase):
    def test_parse_gitignore(self):
        repo = make_repo({}, "node_modules/\n*.pyc\n# comment\n!keep.py\n")
        ignored = parse_gitignore(repo)
        self.assertIn("node_modules", ignored)
        self.assertIn("*.pyc", ignored)
        self.assertNotIn("!keep.py", ignored)

    def test_is_ignored_patterns(self):
        self.assertTrue(is_ignored("dist/app.js", {"dist"}))
        self.assertTrue(is_ignored("src/foo.pyc", {"*.pyc"}))
        self.assertTrue(is_ignored("src/deep/bar.py", {"src/*/bar.py"}))
        self.assertFalse(is_ignored("src/foo.py", {"dist"}))

    def test_iter_source_files_excludes_outputs_and_ignored(self):
        repo = make_repo({
            "main.py": "x = 1\n",
            "paper.typ": "fake output\n",
            "dist/bundle.js": "ignored\n",
            ".env": "SECRET=1\n",
        })
        results = [(str(Path(r)), rel) for r, rel in
                   iter_source_files(repo, parse_gitignore(repo), OUTPUT_BASENAMES)]
        rels = [rel for _, rel in results]
        self.assertIn("main.py", rels)
        self.assertNotIn("paper.typ", rels)
        self.assertNotIn("dist/bundle.js", rels)
        self.assertNotIn(".env", rels)


class TestScan(unittest.TestCase):
    def test_scan_file_line_count(self):
        repo = make_repo({"a.py": "l1\nl2\nl3\n"})
        info = scan_file(str(repo / "a.py"), "a.py")
        self.assertEqual(info["lines"], 3)

    def test_scan_file_binary_sniff(self):
        repo = make_repo({"blob.bin": ""})
        (repo / "blob.bin").write_bytes(b"\x00\x01\x02garbage")
        self.assertIsNone(scan_file(str(repo / "blob.bin"), "blob.bin"))

    def test_iter_source_files_skips_oversized(self):
        repo = make_repo({"big.txt": "x" * 10})
        with mock.patch("code2paper.MAX_FILE_BYTES", 5):
            rels = [rel for _, rel in iter_source_files(repo, set())]
        self.assertEqual(rels, [])

    def test_iter_source_files_exclude_prefix(self):
        repo = make_repo({"src/a.py": "x\n", "gen/b.py": "y\n"})
        rels = [rel for _, rel in iter_source_files(repo, set(), exclude_prefixes=(("gen",),))]
        self.assertNotIn("gen/b.py", rels)
        self.assertIn("src/a.py", rels)


class TestAnalysis(unittest.TestCase):
    def test_analyze_python(self):
        info = analyze_python({"rel": "mod.py", "text": SAMPLE_PY, "lines": 12})
        self.assertIn("Greeter(greet)", info["classes"])
        self.assertTrue(any(f == "main" or f.startswith("main(") for f in info["funcs"]))
        self.assertIn("os", info["imports"])
        self.assertGreater(info["complexity"], 0)

    def test_analyze_python_syntax_error_falls_back(self):
        info = analyze_python({"rel": "bad.py", "text": "def broken(:\n", "lines": 1})
        self.assertEqual(info["ext"], ".py")
        self.assertIsInstance(info["complexity"], int)

    def test_analyze_generic_js(self):
        info = analyze_generic({"rel": "app.js", "text": "function render() {\n  if (x) { return 1; }\n}\n", "lines": 3})
        self.assertIn("render(...)", info["funcs"])
        self.assertGreater(info["complexity"], 0)

    def test_analyze_generic_class(self):
        info = analyze_generic({"rel": "app.ts", "text": "export class Service {\n  handle() {}\n}\n", "lines": 3})
        self.assertIn("Service", info["classes"])

    def test_build_deps(self):
        files = [
            {"ext": ".py", "rel": "app.py", "imports": ["helpers"]},
            {"ext": ".py", "rel": "helpers.py", "imports": []},
            {"ext": ".py", "rel": "app.py", "imports": ["os"]},
        ]
        deps = build_deps(files)
        self.assertIn(("app.py", "helpers.py"), deps)
        self.assertNotIn(("app.py", "os"), deps)


class TestReport(unittest.TestCase):
    def test_build_report_metrics(self):
        repo = make_repo({"a.py": "print('hi')\n" * 5, "b.js": "function x(){}\n" * 3})
        report = build_report(repo, "Test", OUTPUT_BASENAMES)
        self.assertEqual(report["total_files"], 2)
        self.assertEqual(report["total_lines"], 8)
        self.assertEqual(len(report["by_ext"]), 2)
        self.assertIn(".py", dict(report["by_ext"]))

    def test_build_report_excludes_outputs(self):
        repo = make_repo({"a.py": "x=1\n", "paper.md": "old\n"})
        report = build_report(repo, "Test", OUTPUT_BASENAMES)
        rels = [f["rel"] for f in report["files"]]
        self.assertIn("a.py", rels)
        self.assertNotIn("paper.md", rels)


class TestPack(unittest.TestCase):
    def test_pack_native_excludes_outputs(self):
        repo = make_repo({"main.py": "print(1)\n", "paper.typ": "junk\n"})
        with mock.patch("code2paper.shutil.which", return_value=None):
            packed = pack_codebase(repo, parse_gitignore(repo), OUTPUT_BASENAMES)
        self.assertIn("--- File: main.py ---", packed)
        self.assertNotIn("--- File: paper.typ ---", packed)

    def test_pack_uses_repomix_when_available(self):
        repo = make_repo({"main.py": "x=1\n"})
        with mock.patch("code2paper.shutil.which", return_value="/fake/repomix"):
            with mock.patch("code2paper.subprocess.run") as run:
                run.return_value = mock.Mock(stdout="packed by repomix", returncode=0)
                packed = pack_codebase(repo, parse_gitignore(repo), OUTPUT_BASENAMES)
                self.assertEqual(packed, "packed by repomix")
                cmd = run.call_args.args[0]
                self.assertEqual(cmd[0], "/fake/repomix")
                self.assertIn("--ignore", cmd)


class TestEscaping(unittest.TestCase):
    def test_typst_escape(self):
        self.assertEqual(typst_escape("# $ { } @"), r"\# \$ \{ \} \@")

    def test_latex_escape(self):
        self.assertEqual(latex_escape("a_%#b"), r"a\_\%\#b")


class TestRenderers(unittest.TestCase):
    def setUp(self):
        self.repo = make_repo({"core.py": SAMPLE_PY, "util.js": "function helper(){\n}\n"})
        self.report = build_report(self.repo, "Demo", OUTPUT_BASENAMES)

    def test_paper_source(self):
        src = generate_paper_source(self.report, "Demo")
        self.assertIn("Demo", src)
        self.assertIn("== 1. System Overview", src)
        self.assertIn("core.py", src)
        self.assertIn("Greeter(greet)", src)

    def test_latex_source(self):
        src = generate_latex_source(self.report, "Demo")
        self.assertIn(r"\documentclass", src)
        self.assertIn(r"\begin{abstract}", src)
        self.assertIn("core.py", src)

    def test_html_source_escapes(self):
        report = {"repo": "r", "title": "T", "files": [
            {"rel": "<script>alert(1)</script>.py", "lines": 3, "complexity": 1,
             "funcs": [], "classes": []}
        ], "total_files": 1, "total_lines": 3, "total_complexity": 1,
            "by_ext": [(".py", [1, 3])], "deps": []}
        src = generate_html_paper_source(report, "T")
        body = src.split("<body>")[-1].split("</body>")[0]
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", body)
        self.assertNotIn("<script>alert", body)

    def test_markdown_source(self):
        src = generate_markdown_source(self.report, "Demo")
        self.assertIn("| Module |", src)
        self.assertIn("core.py", src)


class TestE2E(unittest.TestCase):
    def test_main_writes_all_formats(self):
        repo = make_repo({"a.py": "def f():\n    return 1\n"})
        out = Path(tempfile.mkdtemp())
        with mock.patch("code2paper.shutil.which", side_effect=lambda name: None):
            with mock.patch("sys.argv", ["code2paper", str(repo), "--out-dir", str(out)]):
                from code2paper import main
                main()
        for name in ("paper.typ", "paper.html", "paper.md", "paper.tex"):
            self.assertTrue((out / name).exists(), f"missing {name}")

    def test_main_outdir_equals_repo_still_analyzes(self):
        repo = make_repo({"a.py": "def f():\n    return 1\n"})
        with mock.patch("code2paper.shutil.which", side_effect=lambda name: None):
            with mock.patch("sys.argv", ["code2paper", str(repo), "--out-dir", str(repo)]):
                from code2paper import main
                main()
        md = (repo / "paper.md").read_text(encoding="utf-8")
        self.assertIn("a.py", md)
        self.assertNotIn("paper.typ", md)

    def test_main_rejects_missing_path(self):
        with mock.patch("sys.argv", ["code2paper", "C:/nonexistent/xyz"]):
            from code2paper import main
            with self.assertRaises(SystemExit):
                main()


if __name__ == "__main__":
    unittest.main()
