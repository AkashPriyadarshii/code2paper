*Fuel the next build:* 

# code2paper

**Support:** fuel the next build — [![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/AkashPriyadarshi)

> **The skill that understands ANY repository — for every developer.** Drop it into any AI agent (Claude Code, OpenCode, Codex, Gemini CLI, Cursor) and get a plain-language guide for beginners AND a formal academic paper for architects — grounded in the real code, never guessed.

## The core idea: skill-first

`code2paper` is a **universal agent skill**, not a CLI. Inside your AI agent it:

1. **Reads the actual source** — entrypoints, dependency hubs, top-LOC modules.
2. **Measures real numbers** — files, LOC, complexity, dependency edges (100+ languages, 2026 ecosystem).
3. **Maps the dependency graph** and builds a foundation-first reading order.
4. **Writes two artifacts from the same ground truth:**
   - `human-guide.md` — plain-language walkthrough for beginners & vibecoders.
   - `paper.*` — formal academic spec (Markdown / Typst / LaTeX / HTML-PDF) for advanced devs & architects.
5. **Never ships guesses.** Anything unverified is labeled "not verified".

## Quick Start

```text
# In any agent
/code2paper /path/to/repo

# Or just ask
"understand this repo: ./my-project"
"make a whitepaper for this codebase"
```

The skill works standalone — no Python package, no install, no CLI. It embeds its own language tables, import-syntax reference for 100+ languages, entrypoint conventions, templates, and a premortem checklist.

## Outputs

| Artifact | Audience | Format |
| --- | --- | --- |
| `human-guide.md` | Beginners & vibecoders | Plain language, reading order, glossary |
| `paper.md` | Advanced devs | GFM academic spec |
| `paper.typ` | Publication | Typst (compiles to PDF) |
| `paper.tex` | Publication | LaTeX |
| `paper.html` | Everyone | WebPaper with MathJax, print-to-PDF |

## Install the skill

Copy `skills/code2paper.md` into your agent's skill directory:

```bash
# Claude Code / OpenCode / most agents
mkdir -p ~/.claude/skills/code2paper
cp skills/code2paper.md ~/.claude/skills/code2paper/SKILL.md
```

## Ecosystem & Related Tools

- **[Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)** — interactive visual knowledge graph for visual learners.
- **[Repomix](https://github.com/yamadashy/repomix)** — high-performance repository packing engine.

## License

MIT
