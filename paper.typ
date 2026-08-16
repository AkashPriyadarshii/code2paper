#set page(
  paper: "us-letter",
  margin: (x: 1.8cm, y: 2.2cm),
  header: align(right)[
    #text(size: 9pt, fill: rgb("#666666"))[code2paper -- Academic Codebase Specification]
  ],
  footer: [
    #align(center)[#text(size: 9pt, fill: rgb("#666666"))[Page #counter(page).display()]]
  ]
)
#set text(font: ("Times New Roman", "Liberation Serif", "Arial", "DejaVu Serif"), size: 10pt)

#align(center)[
  #block(width: 100%)[
    #text(18pt, weight: "bold")[ Code2Paper ] \
    #v(4pt)
    #text(11pt, style: "italic")[ An Automated Architectural Analysis and Specification ] \
    #v(8pt)
    #text(10pt)[ *Generated via code2paper* ]
  ]
]

#v(12pt)

#block(
  fill: rgb("#f8f9fa"),
  inset: 12pt,
  radius: 4pt,
  stroke: 0.5pt + rgb("#e9ecef")
)[
  #text(weight: "bold")[Abstract] -- The repository `code2paper` implements a modular system analyzed by code2paper. It contains 15 source files totaling 2107 lines of code with an estimated cyclomatic complexity of 229.

Language breakdown:
- `.py`: 2 files, 911 lines
- `.html`: 1 files, 876 lines
- `.md`: 9 files, 247 lines
- `(none)`: 2 files, 40 lines
- `.txt`: 1 files, 33 lines
]

#v(8pt)

== 1. System Overview
The repository `code2paper` implements a modular system analyzed by code2paper. It contains 15 source files totaling 2107 lines of code with an estimated cyclomatic complexity of 229.

Language breakdown:
- `.py`: 2 files, 911 lines
- `.html`: 1 files, 876 lines
- `.md`: 9 files, 247 lines
- `(none)`: 2 files, 40 lines
- `.txt`: 1 files, 33 lines

== 2. Architecture & Component Structure
```
code2paper/
├── index.html (876 LOC)
├── code2paper.py (675 LOC)
├── tests/test_code2paper.py (236 LOC)
├── docs/USAGE.md (59 LOC)
├── README.md (43 LOC)
├── skills/code2paper.md (41 LOC)
├── llms.txt (33 LOC)
├── docs/ARCHITECTURE.md (31 LOC)
├── LICENSE (21 LOC)
├── docs/DESIGN.md (20 LOC)
├── .gitignore (19 LOC)
├── docs/PRD.md (19 LOC)
```

Dependency graph (top 15):
- `tests/test_code2paper.py` -> `code2paper.py`

== 3. Core Module Specifications
- **`index.html`** — 876 LOC, complexity 22

  - `refreshPaper(...)`
  - `switchTab(...)`
  - `applyPreset(...)`
  - `triggerPDFPrint(...)`
  - `setTimeout(...)`
  - `copySnippet(...)`
- **`code2paper.py`** — 675 LOC, complexity 126

  - `parse_gitignore(repo_path: Path)`
  - `is_ignored(rel, patterns)`
  - `_within(child: Path, parent: Path)`
  - `iter_source_files(repo_path: Path, patterns: set, exclude_basenames=frozenset(), exclude_prefixes=())`
  - `scan_file(path: str, rel: str)`
  - `_norm_ext(rel: str)`
  - `analyze_python(info: dict)`
  - `analyze_generic(info: dict)`
  - `analyze_file(info: dict)`
  - `build_deps(files: list)`
- **`tests/test_code2paper.py`** — 236 LOC, complexity 56
  - `TestGitignore(test_parse_gitignore, test_is_ignored_patterns, test_iter_source_files_excludes_outputs_and_ignored)`
  - `TestScan(test_scan_file_line_count, test_scan_file_binary_sniff, test_iter_source_files_skips_oversized, test_iter_source_files_exclude_prefix)`
  - `TestAnalysis(test_analyze_python, test_analyze_python_syntax_error_falls_back, test_analyze_generic_js, test_analyze_generic_class, test_build_deps)`
  - `TestReport(test_build_report_metrics, test_build_report_excludes_outputs)`
  - `TestPack(test_pack_native_excludes_outputs, test_pack_uses_repomix_when_available)`
  - `TestEscaping(test_typst_escape, test_latex_escape)`
  - `make_repo(files: dict, gitignore: str=None)`
  - `test_parse_gitignore(self)`
  - `test_is_ignored_patterns(self)`
  - `test_iter_source_files_excludes_outputs_and_ignored(self)`
  - `test_scan_file_line_count(self)`
  - `test_scan_file_binary_sniff(self)`
  - `test_iter_source_files_skips_oversized(self)`
  - `test_iter_source_files_exclude_prefix(self)`
  - `test_analyze_python(self)`
  - `test_analyze_python_syntax_error_falls_back(self)`
- **`docs/USAGE.md`** — 59 LOC, complexity 5
- **`README.md`** — 43 LOC, complexity 4
- **`skills/code2paper.md`** — 41 LOC, complexity 4
- **`llms.txt`** — 33 LOC, complexity 4
- **`docs/ARCHITECTURE.md`** — 31 LOC, complexity 1
- **`LICENSE`** — 21 LOC, complexity 0
- **`docs/DESIGN.md`** — 20 LOC, complexity 2
- **`.gitignore`** — 19 LOC, complexity 0
- **`docs/PRD.md`** — 19 LOC, complexity 4

== 4. Mathematical Formalization & Data Flow
$ L_total = sum_(f in F) ell(f) = 2107 $

$ C_total = sum_(f in F) c(f) = 229 $

$ |E| = 1 $

Data flows along internal import edges; for Python modules the graph above lists concrete `from -> to` dependency chains.

== 5. Implementation Trade-offs & Limitations
1. Scalability: memory footprint scales linearly with module count; context packing is capped at per-file limits to bound resource usage.
2. Language Coverage: Python modules get full AST analysis; other languages use regex heuristics (function/class estimates, not bytecode-accurate).
3. Dependency Bound: relies on stdlib and optional external tooling (repomix, typst); absent tools degrade gracefully.
4. Complexity Estimates: 229 is an estimated cyclomatic complexity across all files, dominated by control-flow constructs.
