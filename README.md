# code2paper

> Transform any local repository or codebase into an academic-grade research paper (LaTeX / Typst + PDF). Built for FOSS devs and vibecoders.

## Features
- **Repomix AST Extraction**: Bundles repository source and file map into token-optimized context.
- **Academic Paper Generation**: Synthesizes Abstract, System Architecture, Mathematical Formalizations, Module Specs, and Performance Analysis.
- **Typst & LaTeX Output**: Compiles modern, clean academic PDFs via Typst (`paper.typ`) or LaTeX (`paper.tex`).
- **Claude Agent Skill**: Native integration as a `/code2paper` skill for terminal-based LLM agents.

## Ecosystem & Related Tools
- **code2paper**: Formal academic paper, math, and system specification generator (Medium/Advanced devs & architects).
- **[Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)**: Interactive visual knowledge graph and onboarding guide (Beginner-friendly visual learning).
- **[Repomix](https://github.com/yamadashy/repomix)**: High-performance repository packing engine.

## Quick Start
```bash
# Generate paper for current repository
npx code2paper .
```

## License
MIT
