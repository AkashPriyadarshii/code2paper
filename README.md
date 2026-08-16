# code2paper

> Transform any local repository or codebase into an academic-grade research paper (Typst / LaTeX / HTML / Markdown + PDF). Built for FOSS devs and vibecoders.

## Features
- **Real Code Analysis**: Python modules parsed via stdlib `ast` (functions, classes, imports, cyclomatic complexity); other languages analyzed via regex heuristics.
- **Dependency Graph**: Internal Python import edges extracted automatically.
- **Four Output Formats**: Typst (`paper.typ` → `paper.pdf`), LaTeX (`paper.tex`), interactive HTML WebPaper (`paper.html`), and GitHub-Flavored Markdown (`paper.md`).
- **Safe Ingestion**: `.gitignore`-aware scanning, binary sniffing, per-file size caps, and automatic exclusion of generated outputs.
- **Claude Agent Skill**: Native integration as a `/code2paper` skill for terminal-based LLM agents.

## Ecosystem & Related Tools
- **code2paper**: Formal academic paper, math, and system specification generator (Medium/Advanced devs & architects).
- **[Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)**: Interactive visual knowledge graph and onboarding guide (Beginner-friendly visual learning).
- **[Repomix](https://github.com/yamadashy/repomix)**: High-performance repository packing engine (optional, auto-detected).

## Quick Start
```bash
# Basic run (generates paper.typ/tex/html/md in the current directory, compiles paper.pdf if typst is installed)
python code2paper.py .

# Write outputs into a separate directory
python code2paper.py /path/to/repo --out-dir ./build

# Keep the Typst source file after compiling
python code2paper.py . --keep-typst

# Or run via Claude Code Agent Skill
/code2paper
```

## Prerequisites
- Python 3.10+ (stdlib only)
- Optional: [Typst](https://typst.app) CLI for PDF compilation
- Optional: [Repomix](https://github.com/yamadashy/repomix) for token-optimized packing (falls back to built-in walker)

## Testing
```bash
python -m unittest discover tests
```

## License
MIT
