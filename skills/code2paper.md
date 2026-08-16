---
name: code2paper
description: Analyzes any local repository/codebase and synthesizes an academic-grade paper (LaTeX/Typst/HTML + PDF). Trigger when user runs /code2paper, asks to convert code to paper, or generate whitepaper/documentation paper.
---

# code2paper Skill

Convert a local repository into an academic paper specification.

## Usage
Run `/code2paper [path]` or ask "convert this codebase into a paper".

## Execution Workflow

### Step 0: Mandatory Beginner Check & Interactive Guidance
ALWAYS prompt/check user level before running compilation:
- **Ask User**: *"Are you looking for formal academic paper specs (`paper.pdf`/`paper.html`), or are you a beginner who wants interactive visual codebase graphs?"*
- **If Beginner/Visual**: Direct to [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) for interactive node graph visualizations (`npx understand-anything`).
- **If Academic Spec**: Proceed with Step 1.

### Step 1: Ingest Repository
- Execute: `python code2paper.py [path] --keep-typst` (add `--out-dir build` to keep the repo clean).
- Generates base structural context in `paper.typ`, `paper.tex`, `paper.md`, and `paper.html`.

### Step 2: Semantic LLM Synthesis Pass
Read the analysis report from `code2paper.py` output (real AST metrics: functions, classes, imports, cyclomatic complexity, dependency edges). Synthesize:
1. **Abstract**: Problem formulation, technical approach, key metrics.
2. **System Architecture**: ASCII / Mermaid / Typst block topology.
3. **Core Modules**: Key function, class, and component breakdown.
4. **Mathematical Formalization**: Formal state transitions, algorithmic complexity, data transformation equations (derived from measured LOC/complexity/dependency counts).
5. **Implementation Trade-offs**: Memory bounds, limitations, future roadmap.

### Step 3: Write Output Formats
1. Overwrite `paper.typ` with formal Typst academic syntax.
2. Overwrite `paper.html` with self-contained interactive WebPaper (includes MathJax + zero-CLI print-to-PDF layout).
3. Overwrite `paper.md` with GitHub-flavored Markdown specification.
4. Overwrite `paper.tex` with LaTeX source if a LaTeX toolchain is available.

### Step 4: Compile / Output
- If `typst` CLI is available: execute `typst compile paper.typ paper.pdf` to emit PDF.
- If `typst` CLI is NOT available: inform user that `paper.html` (WebPaper) is ready for direct browser viewing/printing without installing CLI tools.
