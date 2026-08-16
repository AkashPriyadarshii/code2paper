# code2paper Usage Guide

Step-by-step tutorial for using `code2paper` to turn any codebase into an academic paper.

## Prerequisites

1. **Python 3.10+** (Required)
2. **Typst Compiler** (Optional, for PDF compilation)
   - Install via Cargo: `cargo install typst-cli`
   - Or download from [typst.app](https://typst.app)
3. **Repomix** (Optional, for token-optimized context extraction)
   - Install globally: `npm install -g repomix`

## Basic Usage

### Option 1: Python CLI
Run `code2paper.py` pointing to any directory:

```bash
# Basic run (writes paper.typ/tex/html/md to the current dir; compiles paper.pdf if typst is installed)
python code2paper.py /path/to/repo

# Write generated sources to a dedicated directory
python code2paper.py /path/to/repo --out-dir build

# Custom output PDF path
python code2paper.py /path/to/repo -o build/my_paper.pdf

# Keep intermediate Typst source file
python code2paper.py /path/to/repo --keep-typst
```

### Option 2: Claude Agent Skill
1. Place the skill directory in `~/.claude/skills/code2paper/`.
2. In Claude Code terminal:
   ```text
   /code2paper
   ```

## Outputs

| File | Format |
| --- | --- |
| `paper.typ` | Typst source (compiles to `paper.pdf`) |
| `paper.tex` | LaTeX source |
| `paper.html` | Interactive WebPaper (print to PDF from browser) |
| `paper.md` | GitHub-Flavored Markdown |

## What gets analyzed

- Python modules: full AST analysis (functions, classes, imports, cyclomatic complexity).
- Other languages: regex heuristics for functions/classes and control-flow complexity.
- Internal dependency graph from Python imports.

## Troubleshooting

- **PDF not compiling**: Verify `typst --version` works in your shell. If not installed, `code2paper` falls back to the HTML WebPaper (browser print-to-PDF) plus `paper.typ`/`paper.tex` sources.
- **Large codebase truncation**: Files over 1MB are skipped automatically; install `repomix` for token-optimized context on huge repositories.
- **Outputs inside the repo**: generated `paper.*` files are always excluded from analysis on subsequent runs.
