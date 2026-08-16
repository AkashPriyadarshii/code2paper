# Design & Style Specification: code2paper

## Output Formats
- **Primary Engine**: Typst (`paper.typ` → `paper.pdf`).
- **Secondary Engines**: LaTeX (`paper.tex`), HTML WebPaper (`paper.html`), GitHub-Flavored Markdown (`paper.md`).

## Analysis Model
- Python modules: stdlib `ast` parsing for functions, classes, imports, and cyclomatic complexity.
- Other languages: regex heuristics for function/class inventory and control-flow complexity.
- Dependency graph from internal Python imports.

## Paper Layout Specification
- Single-column US Letter layout (Typst default; LaTeX `article` class).
- Sections:
  1. Abstract
  2. System Overview (repo metrics, language breakdown)
  3. Architecture & Component Structure (file tree, dependency graph)
  4. Core Module Specifications (per-module LOC, complexity, functions, classes)
  5. Mathematical Formalization & Data Flow (measured LOC/complexity/dependency equations)
  6. Implementation Trade-offs & Limitations
