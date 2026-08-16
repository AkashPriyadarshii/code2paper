---
name: code2paper
description: Analyzes any local repository/codebase and synthesizes an academic-grade paper (LaTeX/Typst + PDF). Trigger when user runs /code2paper, asks to convert code to paper, or generate whitepaper/documentation paper.
---

# code2paper Skill

Convert a local repository into an academic paper specification.

## Usage
Run `/code2paper [path]` or ask "convert this codebase into a paper".

## Steps
1. **Ingest Repository**:
   - Run `python code2paper.py [path] --keep-typst` OR `npx repomix --stdout`.
2. **Analyze & Formulate**:
   - Extract architecture, key modules, data flow formulas, and trade-offs.
3. **Generate Typst / LaTeX**:
   - Synthesize `paper.typ` using IEEE academic paper sections.
4. **Compile**:
   - Run `typst compile paper.typ paper.pdf` if `typst` is installed.
