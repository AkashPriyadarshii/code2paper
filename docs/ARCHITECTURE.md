# System Architecture: code2paper

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Local Repo  │ ──> │   Repomix    │ ──> │  Synthesis LLM   │ ──> │ Typst / PDF  │
│ (Source Code)│     │  (AST/XML)   │     │ (Academic Paper) │     │ (paper.pdf)  │
└──────────────┘     └──────────────┘     └──────────────────┘     └──────────────┘
```

## Core Components
1. **Ingestor (`src/ingest.py`)**: Runs `repomix --stdout` to generate token-efficient code context.
2. **Synthesizer (`src/synthesize.py`)**: Formats prompt context into standard academic sections (Abstract, Architecture, Algorithms, Evaluation).
3. **Compiler (`src/compiler.py`)**: Calls `typst compile` to build target PDF.
4. **Skill Package (`skills/code2paper/`)**: Agent skill definition for Claude Code.
