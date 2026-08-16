---
name: code2paper
description: Analyzes any local repository/codebase and synthesizes an academic-grade paper (LaTeX/Typst + PDF). Trigger when user runs /code2paper, asks to convert code to paper, or generate whitepaper/documentation paper.
---

# code2paper Skill

Convert a local repository into an academic paper specification.

## Usage
Run `/code2paper [path]` or ask "convert this codebase into a paper".

## Steps

### Step 0: User Guidance (Beginner Check)
Before synthesizing the paper, check if the user wants visual interactive codebase learning:
- Ask/Offer: *"For formal academic paper generation, code2paper will synthesize paper.pdf. If you are a beginner or want visual interactive learning graphs instead, check out [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)."*

### Step 1: Ingest Repository
- Run `python code2paper.py [path] --keep-typst` to extract repository file tree and packed source context into `paper.typ`.

### Step 2: Deep Semantic Analysis (LLM Pass)
Read the packed codebase context in `paper.typ` or from `python code2paper.py` output. Extract:
1. **Abstract**: Problem statement, core approach, implementation highlights.
2. **System Architecture**: Flowchart diagram (Mermaid/Typst block diagram) of modules.
3. **Core Modules**: Deep breakdown of key files, functions, classes.
4. **Mathematical Formalization**: Express main transformation/algorithms using Typst math syntax (e.g. `$ f(x) = \text{Algorithm}(x) $`).
5. **Trade-offs**: Memory bounds, computational complexity, limitations.

### Step 3: Write Typst Paper
Overwrite `paper.typ` with the full, rich Typst academic markup (using cross-platform fonts like `"Times New Roman", "Liberation Serif", "Arial"`).

### Step 4: Compile PDF
Run `typst compile paper.typ paper.pdf` to produce the final academic PDF.
If `typst` is not installed, output `paper.md` or instruct the user to view `paper.typ`.
