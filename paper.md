# code2paper: Automated Architectural Synthesis and Academic Formalization of Software Repositories

**Author**: Akash Priyadarshi  
**Version**: v0.1.0 Technical Specification  

---

## Abstract
We present **code2paper**, a lightweight, standard-library-first CLI tool and LLM Agent Skill that automatically parses local software repositories and synthesizes formal academic-grade technical specifications in Typst and LaTeX. Software projects frequently lack formal mathematical and architectural documentation due to high manual authoring overhead. **code2paper** bridges this gap by coupling AST context packing (via Repomix or native gitignore-aware traversal) with a multi-stage LLM semantic synthesis pipeline. We evaluate **code2paper** on its own codebase, demonstrating complete formalization of system topology, data transformation bounds, and execution complexity.

---

## 1. Introduction & Problem Definition
Modern software engineering produces complex, multi-layered codebases, yet formal architectural specifications remain rare outside safety-critical domains. Existing documentation tools generate API reference lists but fail to formalize high-level mathematical transformations, component dependencies, and system trade-offs.

**code2paper** addresses this problem by treating codebase transformation as an inverse paper compilation process:
$$ S_{\text{repo}} \xrightarrow{\text{Repomix}} \mathcal{D}_{\text{AST}} \xrightarrow{\text{LLM Synthesis}} \mathcal{P}_{\text{Typst}} \xrightarrow{\text{Typst Compiler}} \mathcal{O}_{\text{PDF}} $$

---

## 2. System Architecture
The system consists of three decoupled components:
1. **Ingestor (`code2paper.py`)**: Traverses the repository tree, enforces `.gitignore` exclusions, filters binary assets, and emits a consolidated structural context.
2. **Synthesizer (`skills/code2paper/SKILL.md`)**: Executes a 4-step LLM analysis pass extracting abstract, system topology, component tables, and mathematical formulas.
3. **Compiler (`typst`)**: Compiles the generated markup into IEEE-styled PDF documents.

```
[Local Repo] --> Ingestor (Repomix / Stdlib Walk)
  --> Context Buffer (codebase AST / XML)
  --> LLM Synthesis Pass (Equations + Specs)
  --> paper.typ (Typst Source) --> paper.pdf (Compiled Spec)
```

---

## 3. Core Module Specifications

| Module Path | Primary Responsibility | Dependencies |
| :--- | :--- | :--- |
| `code2paper.py` | Stdlib repository walk, .gitignore parsing, Typst template injection, and compilation CLI. | Python 3.10+ Stdlib |
| `skills/code2paper/SKILL.md` | Claude Agent Skill definition instructing LLM on semantic extraction and math synthesis. | Claude Code Agent |
| `index.html` | Responsive product landing page hosted on GitHub Pages. | HTML5 / CSS3 |
| `docs/USAGE.md` | Prerequisites, CLI examples, and troubleshooting guide. | Markdown |
| `docs/ARCHITECTURE.md` | High-level system block diagram and module breakdown. | Markdown |

---

## 4. Algorithmic & Mathematical Formalization
Let $R$ be a repository containing set of files $F = \{f_1, f_2, \dots, f_n\}$. The packing function $P(R)$ maps the file tree to context string $C$:
$$ P(R) = \bigoplus_{i=1}^{n} \mathbb{I}(f_i \notin I_{\text{ignore}}) \cdot \text{Read}(f_i) $$

where $I_{\text{ignore}} = I_{\text{git}} \cup I_{\text{binary}} \cup I_{\text{secrets}}$.

The space complexity of context accumulation is strictly linear with total code volume:
$$ \mathcal{O}_{\text{space}}(P) = \sum_{i=1}^{n} |f_i| $$

---

## 5. Implementation Trade-offs & Future Work
- **Zero Heavy Dependencies**: Built exclusively using Python standard library modules (`sys`, `os`, `subprocess`, `shutil`, `argparse`).
- **Cross-Platform Font Fallbacks**: Template uses `"Times New Roman", "Liberation Serif", "Arial"` to ensure compilation on Linux, macOS, and Windows.
- **Future Work**: Support for multi-column IEEE LaTeX export and automated Mermaid-to-Typst vector graph rendering.
