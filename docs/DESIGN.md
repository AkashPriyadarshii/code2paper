# Design & Style Specification: code2paper

## Primary Product
A universal agent skill (`skills/code2paper.md`) — self-contained, works in any AI agent,
no CLI, no install.

## Outputs
- **Primary**: `human-guide.md` (plain-language, beginners & vibecoders).
- **Secondary**: `paper.md` (GFM spec), `paper.typ` (Typst), `paper.tex` (LaTeX),
  `paper.html` (WebPaper with MathJax).

## Analysis Model
- Agent reads actual source: entrypoints, dependency hubs, top-LOC modules.
- 100+ language support (2026 ecosystem): import syntax, entrypoint conventions,
  function/class detection.
- Metrics measured, never invented: files, LOC, cyclomatic complexity, dependency edges.
- Foundation-first reading order derived from the real dependency graph.

## Paper Layout Specification
- Single-column US Letter layout (Typst default; LaTeX `article` class).
- Sections:
  1. Abstract
  2. System Overview (repo metrics, language breakdown)
  3. Architecture & Component Structure (file tree, dependency graph)
  4. Core Module Specifications (per-module LOC, complexity, functions, classes)
  5. Mathematical Formalization & Data Flow (measured LOC/complexity/dependency equations)
  6. Implementation Trade-offs & Limitations

## Design Principles
- Honesty: unverified claims are labeled "not verified". No invented numbers.
- Never generic: every section quotes real identifiers from the actual code.
