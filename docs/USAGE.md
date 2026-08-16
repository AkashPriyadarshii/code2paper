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
# Basic run (generates paper.typ and compiles paper.pdf if typst is installed)
python code2paper.py /path/to/repo

# Custom output path
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

## Troubleshooting

- **PDF not compiling**: Verify `typst --version` works in your shell. If not installed, `code2paper` falls back to outputting `paper.typ` source.
- **Large codebase truncation**: Ensure `repomix` is installed to enable smart AST pruning on huge repositories.
