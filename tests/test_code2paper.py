import unittest
import tempfile
from pathlib import Path
from code2paper import parse_gitignore, pack_codebase, generate_paper_source, generate_html_paper_source

class TestCode2Paper(unittest.TestCase):
    def test_parse_gitignore(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / ".gitignore").write_text("node_modules/\n*.pyc\n# comment\n", encoding="utf-8")
            ignored = parse_gitignore(tmppath)
            self.assertIn("node_modules", ignored)
            self.assertIn("*.pyc", ignored)

    def test_generate_paper_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            source = generate_paper_source(tmppath, "--- File: test.py ---\nprint('hello')", "Test Title")
            self.assertIn("Test Title", source)
            self.assertIn("test.py", source)

    def test_generate_html_paper_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            html = generate_html_paper_source(tmppath, "--- File: main.py ---\npass", "HTML Title")
            self.assertIn("HTML Title", html)
            self.assertIn("main.py", html)

if __name__ == "__main__":
    unittest.main()
