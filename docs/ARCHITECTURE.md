# System Architecture: code2paper

```
┌──────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  Local Repo  │ → │ Scan & Analyze   │ → │  Renderers       │ → │ Typst / LaTeX /  │
│ (Source Code)│   │ (gitignore-aware │   │ (Typst, LaTeX,   │   │ HTML / Markdown  │
│              │   │  walker + AST/   │   │  HTML, Markdown) │   │ / PDF outputs    │
└──────────────┘   │  regex metrics)  │   └──────────────────┘   └──────────────────┘
                   └──────────────────┘
```

## Core Components

All logic lives in a single stdlib-only module, `code2paper.py`:

1. **Scanner (`iter_source_files`, `scan_file`)**: `.gitignore`-aware repository walker with binary sniffing, per-file size caps (1MB), and exclusion of generated `paper.*` outputs.
2. **Analyzer (`analyze_python`, `analyze_generic`, `build_report`)**: Python modules are parsed via `ast` for functions, classes, imports, and cyclomatic complexity; other languages use regex heuristics. `build_deps` derives an internal import dependency graph.
3. **Renderers (`generate_paper_source`, `generate_latex_source`, `generate_html_paper_source`, `generate_markdown_source`)**: emit Typst, LaTeX, HTML WebPaper, and GitHub-Flavored Markdown from a shared report.
4. **Optional packer (`pack_codebase`)**: uses `repomix --stdout` when installed (resolved binary, timeout guarded); falls back to the native walker.
5. **Compiler (in `main`)**: calls `typst compile` when the Typst CLI is present; otherwise HTML WebPaper serves as the PDF fallback.

## Outputs

- `paper.typ` → `paper.pdf` (requires Typst CLI)
- `paper.tex` — LaTeX source
- `paper.html` — self-contained interactive WebPaper (MathJax, print-to-PDF)
- `paper.md` — GitHub-Flavored Markdown

## Skill Package

`skills/code2paper.md` defines the Claude/LLM agent skill that orchestrates the CLI and a semantic LLM synthesis pass.
