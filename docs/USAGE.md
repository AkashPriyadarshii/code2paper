# code2paper Usage Guide

How to use `code2paper` to understand any repository — no install, no CLI.

## Option 1: In your AI agent (recommended)

1. Copy the skill into your agent's skill directory:
   ```bash
   mkdir -p ~/.claude/skills/code2paper
   cp skills/code2paper.md ~/.claude/skills/code2paper/SKILL.md
   ```
   (OpenCode, Codex, Gemini CLI, and Cursor accept the same `SKILL.md` format.)

2. Run it:
   ```text
   /code2paper /path/to/repo
   ```

3. Or just ask in natural language:
   ```text
   "understand this repo: ./my-project"
   "make a whitepaper for this codebase"
   "is this repo beginner-friendly?"
   ```

The agent then reads the real code, measures real metrics, maps the dependency graph,
and writes `human-guide.md` + `paper.{md,typ,tex,html}`.

## Outputs

| Artifact | Format | Audience |
| --- | --- | --- |
| `human-guide.md` | Plain-language guide | Beginners & vibecoders |
| `paper.md` | GitHub-Flavored Markdown spec | Advanced |
| `paper.typ` | Typst source (compiles to `paper.pdf`) | Publication |
| `paper.tex` | LaTeX source | Publication |
| `paper.html` | WebPaper with MathJax (print-to-PDF) | Everyone |

## Optional: compile a PDF

If you have the Typst CLI installed:

```bash
typst compile paper.typ paper.pdf
```

If not, open `paper.html` in a browser and print to PDF — zero toolchain.

## Troubleshooting

- **Agent produced guesses?** The skill mandates reading real code. If a section looks
  invented, the agent skipped Step 3 — re-run and insist every claim be code-grounded.
- **Huge repo?** The skill reads entrypoints + hubs + top-LOC + a sample per directory,
  and labels the rest "overviewed". That is by design.
- **Non-Python repo?** Language tables cover 100+ languages (2026 ecosystem), including
  import syntax and entrypoint conventions.
