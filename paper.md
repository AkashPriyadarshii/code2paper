# Code2Paper

> Automated architectural analysis and specification generated via code2paper.

## Abstract

The repository `code2paper` implements a modular system analyzed by code2paper. It contains 15 source files totaling 2107 lines of code with an estimated cyclomatic complexity of 229.

Language breakdown:
- `.py`: 2 files, 911 lines
- `.html`: 1 files, 876 lines
- `.md`: 9 files, 247 lines
- `(none)`: 2 files, 40 lines
- `.txt`: 1 files, 33 lines

## 1. System Overview

Repository: **code2paper** -- 15 files, 2107 LOC,
estimated cyclomatic complexity 229.

### Language Breakdown

- `.py`: 2 files, 911 lines
- `.html`: 1 files, 876 lines
- `.md`: 9 files, 247 lines
- `(none)`: 2 files, 40 lines
- `.txt`: 1 files, 33 lines

## 2. Architecture & Component Structure

| Module | LOC | Complexity | Functions/Classes |
| --- | ---: | ---: | --- |
| `index.html` | 876 | 22 | refreshPaper(...), switchTab(...), applyPreset(...), triggerPDFPrint(...) |
| `code2paper.py` | 675 | 126 | parse_gitignore(repo_path: Path), is_ignored(rel, patterns), _within(child: Path, parent: Path), iter_source_files(repo_path: Path, patterns: set, exclude_basenames=frozenset(), exclude_prefixes=()) |
| `tests/test_code2paper.py` | 236 | 56 | make_repo(files: dict, gitignore: str=None), test_parse_gitignore(self), test_is_ignored_patterns(self), test_iter_source_files_excludes_outputs_and_ignored(self) |
| `docs/USAGE.md` | 59 | 5 |  |
| `README.md` | 43 | 4 |  |
| `skills/code2paper.md` | 41 | 4 |  |
| `llms.txt` | 33 | 4 |  |
| `docs/ARCHITECTURE.md` | 31 | 1 |  |
| `LICENSE` | 21 | 0 |  |
| `docs/DESIGN.md` | 20 | 2 |  |
| `.gitignore` | 19 | 0 |  |
| `docs/PRD.md` | 19 | 4 |  |
| `CONTRIBUTING.md` | 17 | 1 |  |
| `CLAUDE.md` | 12 | 0 |  |
| `AGENTS.md` | 5 | 0 |  |


## 3. Dependency Graph

- `tests/test_code2paper.py` -> `code2paper.py`

## 4. Mathematical Formalization & Data Flow

- Total lines of code: $L_{total} = \sum_{f \in F} \ell(f) = 2107$
- Estimated cyclomatic complexity: $C_{total} = \sum_{f \in F} c(f) = 229$
- Internal dependency edges: $|E| = 1$

## 5. Implementation Trade-offs & Limitations

1. Scalability: memory footprint scales linearly with module count; context packing is capped at per-file limits to bound resource usage.
2. Language Coverage: Python modules get full AST analysis; other languages use regex heuristics (function/class estimates, not bytecode-accurate).
3. Dependency Bound: relies on stdlib and optional external tooling (repomix, typst); absent tools degrade gracefully.
4. Complexity Estimates: 229 is an estimated cyclomatic complexity across all files, dominated by control-flow constructs.
