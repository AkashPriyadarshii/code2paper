# System Architecture: code2paper

code2paper is a **universal agent skill** — a single self-contained skill file that runs
inside any AI agent. There is no CLI and no runtime dependency.

```
┌──────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────────┐
│  Repo path   │ → │ Agent reads code │ → │ Agent measures    │ → │ Agent writes         │
│ (any language│   │ (entrypoints,    │   │ (files, LOC,      │   │ human-guide.md +     │
│  , any size) │   │  hubs, top-LOC)  │   │  complexity, deps)│   │ paper.{md,typ,tex,   │
└──────────────┘   └──────────────────┘   └──────────────────┘   │ html}                │
                                                                 └──────────────────────┘
```

## Core Components

All logic lives in a single file, `skills/code2paper.md`:

1. **Step 0 — Audience check**: beginner/vibecoder, advanced, or both; routes output priority.
2. **Step 1 — Inventory**: agent lists the repo, identifies stack, framework, entrypoints.
3. **Step 2 — Metrics**: agent measures real numbers (files, LOC, complexity) using its own tools.
4. **Step 3 — Read**: agent reads actual source (entrypoints + hubs + top-LOC + per-directory samples).
5. **Step 4 — Dependency map**: language-specific import syntax tables (100+ languages) build the
   dependency graph and a foundation-first reading order.
6. **Step 5-6 — Render**: `human-guide.md` (plain language) + `paper.*` (formal spec).
7. **Step 7 — Compile & deliver**: optional `typst compile`; HTML WebPaper as zero-CLI PDF route.

## Embedded reference data (inside the skill)

- Language tables: 100+ languages with import syntax for dependency mapping.
- Entrypoint conventions per stack (Python, Node, Flutter, JVM, Go, Rust, C/C++, C#, PHP, Ruby, ...).
- Function/class detection hints per language family.
- Templates for both artifacts, a verification checklist, and a premortem failure table.

## Outputs

- `human-guide.md` — plain-language guide (beginners & vibecoders)
- `paper.md` / `paper.typ` / `paper.tex` — formal academic spec (advanced)
- `paper.html` — WebPaper with MathJax (print-to-PDF, everyone)

## Skill File

`skills/code2paper.md` defines the workflow, embedded language reference, templates,
and QA gates. Copy it into any agent's skill directory to install.
