---
name: code2paper
description: >-
  Turn ANY repository or codebase — any language, any size, from a 10-line script
  to a 20-million-line monorepo — into real, code-grounded understanding. Produces
  a plain-language human guide for beginners/vibecoders AND a formal academic
  paper (Typst / LaTeX / Markdown / HTML / PDF) for advanced devs & architects.
  The agent reads the actual source code and writes verified explanations —
  never guesses, never boilerplate. Trigger when the user runs /code2paper, asks
  to "understand this repo", "explain this codebase", "convert code to a paper",
  "make a whitepaper", "onboard me to this project", or "what does this project do".
version: 2.0.0
license: MIT
source: AkashPriyadarshii/code2paper
---

# code2paper — Understand Any Repository, For Any Developer

## What this skill is

One command, three audiences, every language:

| Artifact | Audience | What it is |
| --- | --- | --- |
| `human-guide.md` | Beginners & vibecoders | Plain-language walkthrough: what each file actually does, how to run it, a dependency-aware reading order, and a patterns glossary — all grounded in the real code. |
| `paper.md` | Advanced devs | GitHub-Flavored Markdown academic spec: architecture, module specs, dependency graph, math formalization. |
| `paper.typ` / `paper.tex` | Advanced devs / publication | Typst and LaTeX source, compile-ready. |
| `paper.html` | Everyone | Self-contained WebPaper with an **interactive dependency graph** + MathJax — print to PDF from any browser, zero toolchain. |

**Core promise:** every claim in every output is verifiable from the code you read.
You are the LLM. Guessing is a bug.

## When to use

- User runs `/code2paper [path]`.
- User says: "understand this repo", "explain this codebase", "what does this project do", "onboard me", "make a whitepaper/paper/spec for this code", "is this repo good for beginners".
- User pastes a repo path and wants a walkthrough.

## How to use — the 7-step workflow

### Step 0 — Audience check (always, before anything)

Ask the user ONE question (or infer from context):

> "Who is this for? (a) beginners/vibecoders, (b) advanced devs/architects, (c) both."

- **(a)** → prioritize `human-guide.md`. Make it genuinely beginner-friendly.
- **(b)** → prioritize `paper.*` (formal, heavy on architecture + math).
- **(c)** → produce everything (default).
- If they want an *interactive visual graph* instead, mention
  [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) as an alternative —
  but still deliver the requested artifact.

### Step 1 — Inventory the repository (read the structure, not the files yet)

1. List the repo root (`ls` / `dir` / file tree). Identify the stack:
   - Language(s) by extension (see the language table below).
   - Framework signals: `package.json` (Node), `pyproject.toml`/`requirements.txt` (Python),
     `pubspec.yaml` (Flutter/Dart), `composer.json` (PHP), `Cargo.toml` (Rust),
     `go.mod` (Go), `pom.xml`/`build.gradle` (JVM), `*.csproj` (C#), `Gemfile` (Ruby),
     `mix.exs` (Elixir), `stack.yaml`/`cabal` (Haskell).
   - Build/run entrypoints: `main.*`, `index.*`, `app.*`, `__main__.py`, `artisan`/`bin/` scripts,
     Dockerfile, Makefile.
2. Read `README` (if present) — it is the project's own authoritative description. Quote it where honest.
3. Note the directory layout: `src/`, `lib/`, `app/`, `tests/`, `docs/`, config files, and any
   generated/vendor dirs to ignore (`node_modules`, `vendor/`, `build/`, `dist/`, `__pycache__`,
   `.dart_tool/`, `target/`, `*.g.dart`, `*.pb.go`, lockfiles, minified bundles).

### Step 2 — Get the numbers (deterministic metrics)

Compute REAL numbers by reading/measuring — do not invent them. Use your native tools
(recursive file listing, `wc -l`, count by extension).

Metrics you need:

- Total file count, total lines of code (per language family).
- Per-file: line count, functions (with signatures), classes (with methods).
- Estimated cyclomatic complexity per file (count control-flow: `if`, `for`, `while`,
  `switch`, `case`, `catch`, `&&`, `||`, ternaries).
- Internal dependency edges (what imports what — read the import statements).

> These numbers are ground truth. Reuse them verbatim in every artifact. If you cannot
> measure something exactly, say "estimated" — never fabricate a precise-looking figure.

### Step 3 — Read the real code (the non-negotiable core)

Read actual source files. Minimum set:

1. **Every entrypoint** you found in Step 1.
2. **The top 10 files by line count** (or the 10 most-cited files).
3. **The dependency hubs** — files that many others import.
4. **One representative file per module/directory** so you can describe each area.

While reading, extract for each key file:

- **Actual purpose** — what it does, its side effects, I/O, the data it owns.
- **Key functions/classes** — real names and signatures, not guesses.
- **Patterns** — decorators, interfaces, generics, async, state management, dependency injection,
  event loops, error handling, caching.
- **Entrypoints & flows** — how the app starts, the main call path.

For huge repos (>200 files): don't try to read everything. Read entrypoints + hubs + a sample
per directory, and mark areas you did NOT fully read as "overviewed, not deep-read".

**The golden rule:** If you didn't read a file, don't claim to know what it does. Write
"not verified" or "overviewed only" instead of inventing.

### Step 4 — Map the dependency graph

For each key file, list what it imports (see language table for syntax). Build a mental or
literal edge list: `file → file_it_imports`. Keep only internal edges (skip stdlib/third-party).

Use the graph to determine **reading order**: leaf modules first (fewest internal deps),
hubs next, entrypoints last. This ordering is your "read this first" list.

### Step 5 — Write the plain-language guide (`human-guide.md`)

Plain, concrete, slightly informal. Show real function names and real examples. Structure:

```markdown
# {Repo} — A Plain-Language Guide

> What this is in one paragraph. No jargon.

## What is this?
3–5 sentences, grounded in what you read. What problem does the repo solve?

## Numbers at a glance
- Files: N · Lines of code: N · Estimated complexity: N
- Languages: list with file+line counts
- Stack: framework signals you found

## How to run it
Exact commands (verified from README, package.json, Makefile, etc.).
1. Install / setup (from README)
2. Run (entrypoint command)
3. Test (test command)

## The big picture
ASCII/Mermaid flow: how the pieces fit. Built from the real call graph.
Example: `[main.dart] → [app] → [pages/] → [services/] → [database/]`

## What each file actually does
### `path/to/file.ext` (N LOC)
- **What it does:** one honest sentence, from reading it.
- **Key pieces:** `functionName(args)`, `ClassName`, ...
- **Patterns:** e.g. decorator routing, async, state management

(Repeat for entrypoints, hubs, and every directory's representative file. For repos
with many files, cover all of them briefly or group small ones per directory.)

## Suggested reading order (start here)
1. leaf util → 2. model → ... → entrypoint
Why each file matters, one line each.

## Concepts & patterns glossary
Real patterns you found, with real file references.
- "Decorators for HTTP routing in `app/routes.py`"
- "Dependency injection in `services/container.go`"

## Honest limitations
- What you overviewed but didn't deep-read.
- Anything you could not verify.
```

### Step 6 — Write the formal specs (`paper.*`)

Same facts, formal register. Sections:

1. **Abstract** — problem, approach, measured metrics.
2. **System Overview** — repo stats, language breakdown (with real numbers), architecture.
3. **Architecture & Component Structure** — topology + real dependency graph.
4. **Core Module Specifications** — per module: real functions/classes + what they do.
5. **Mathematical Formalization & Data Flow** — real equations from measured data
   ($L_{total}$, $C_{total}$, $|E|$) + data-flow description from the real call graph.
6. **Implementation Trade-offs & Limitations** — observed realities, not boilerplate.

Format rules:
- `paper.md`: GitHub-Flavored Markdown, tables for module metrics, mermaid allowed.
- `paper.typ`: valid Typst. Wrap math in `$ ... $`. Verify by eye; do not emit broken syntax.
- `paper.tex`: valid LaTeX `\documentclass{article}`, `amsmath`, escape `# % & _ { }`.
- `paper.html`: self-contained WebPaper. **Must include an interactive dependency-graph
  visualization** (force-directed node graph on `<canvas>`/SVG, vanilla JS, zero libraries)
  showing files as nodes and import/reference edges as links — the same graph you mapped in
  Step 4, draggable and hover-highlighted like Understand-Anything. Keep the MathJax CDN and
  print-to-PDF CSS. Real content in every section.

### Step 7 — Compile & deliver

- If `typst` CLI available: `typst compile paper.typ paper.pdf`. Else: `paper.html` is the
  zero-CLI PDF route (browser print).
- Present `human-guide.md` first for beginners; `paper.pdf`/`paper.html` for advanced.

## Language reference (100+ languages)

### Import syntax for dependency mapping

| Family | Extensions | Import syntax to look for |
| --- | --- | --- |
| Python | `.py` | `import x`, `from x import y`, `from . import`, `from ..pkg import` |
| JS/TS | `.js .jsx .ts .tsx .mjs .cjs` | `import x from '...'`, `import('...')`, `require('...')` |
| Dart | `.dart` | `import 'package:...'`, `import 'relative.dart'` |
| Java/Kotlin | `.java .kt .kts` | `import a.b.c;` |
| Swift | `.swift` | `import Module` |
| C/C++ | `.c .h .cpp .hpp .cc .cxx` | `#include <...>`, `#include "..."` |
| C# | `.cs` | `using A.B.C;` |
| Go | `.go` | `import "path"`, `import "module/pkg"` |
| Rust | `.rs` | `use crate::a::b;`, `use std::...` |
| PHP | `.php` | `use A\B\C;`, `require '...'` |
| Ruby | `.rb` | `require '...'`, `require_relative '...'` |
| Scala | `.scala` | `import a.b.c` |
| Perl | `.pl .pm` | `use Module;` |
| R | `.r .R` | `library(pkg)`, `require(pkg)` |
| Lua | `.lua` | `require("x")` |
| Haskell | `.hs` | `import Module`, `import qualified M` |
| Elixir | `.ex .exs` | `alias A.B`, `use A.B` |
| Erlang | `.erl` | `-include("x.hrl").` |
| Clojure | `.clj .cljs` | `(require '[x :as y])`, `(use 'x)` |
| Julia | `.jl` | `using Pkg`, `import Pkg` |
| Shell | `.sh .bash .zsh` | `source x.sh`, `. ./x.sh` |
| Elm | `.elm` | `import Html exposing (..)` |
| F# | `.fs .fsx` | `open A.B` |
| Groovy | `.groovy` | `import a.b.c` |
| Solidity | `.sol` | `import "x.sol";` |

### Entrypoint conventions by stack

| Stack | Entrypoint signals |
| --- | --- |
| Python | `if __name__ == "__main__"`, `main.py`, `app.py`, `cli.py` |
| Node | `package.json` `"scripts"` / `"main"`, `index.js/ts`, `bin/` |
| Flutter/Dart | `main.dart`, `runApp(` |
| JVM (Java/Kotlin) | `main()` method, Spring `@SpringBootApplication`, `Application.java` |
| Go | `func main()`, `main.go`, `cmd/` |
| Rust | `fn main()`, `src/main.rs`, `#[tokio::main]` |
| C/C++ | `int main(...)` |
| C# | `Main`, `Program.cs`, ASP.NET `app.MapGet` / `Startup` |
| PHP/Laravel | `artisan`, `public/index.php`, `routes/web.php` |
| Ruby/Rails | `bin/rails`, `config/routes.rb` |
| Swift | `@main`, `App.swift` |
| Elixir/Phoenix | `mix.exs`, `lib/*/application.ex` |
| Frontend (React/Vue/Svelte) | `src/main.jsx/tsx`, `index.html`, `vite.config`, `src/App.*` |

### Function/class detection hints

- Python: `def name(args)`, `class Name:`, decorators `@...` above functions.
- JS/TS: `function name(args)`, `const name = (args) =>`, `class Name`, `export function`.
- C-family: `type name(args) {`, `class Name {`.
- Go: `func name(args)`, `type Name struct`.
- Rust: `fn name(args)`, `struct Name`, `enum Name`, `impl Name`.
- Java/Kotlin: `public/private type name(args)`, `class Name`.
- PHP: `function name(args)`, `class Name`.
- Ruby: `def name(args)`, `class Name`.
- Dart: `Type name(args)`, `class Name extends Widget`, `final name = ...`.

## Templates & prompts

### One-liner summary prompt (for you to self-check)

> "Summarize what this repo does in one sentence, naming the stack and the main flow.
> Every word must be backed by something I read."

### Beginner-guide voice

Write like a senior dev explaining to a smart junior: concrete, honest, real examples,
no fluff, no fake enthusiasm, no "seamlessly/elevate/unleash".

### Formal-paper voice

IEEE-ish, third person, precise, citations to file paths instead of literature.

## Verification checklist (before finishing)

- [ ] I read every module I described (all entrypoints + top-LOC + hubs).
- [ ] Every number (files, LOC, complexity, deps) is measured, not invented.
- [ ] Every "What it does" is grounded in source I actually read.
- [ ] Unverified items are labeled "not verified" — nothing fabricated.
- [ ] Reading order respects the real dependency graph.
- [ ] Language breakdown uses real language names + counts.
- [ ] `paper.typ` and `paper.tex` are syntactically valid.
- [ ] `paper.html` renders with MathJax + print-to-PDF.
- [ ] `paper.html` contains an interactive dependency graph (nodes = files, edges = imports/references).
- [ ] Repo stack (framework/entrypoints) identified correctly.

## Premortem — why this skill fails, and how to avoid it

| Failure | Cause | Prevention |
| --- | --- | --- |
| Looks generic/AI-written | Not reading the code, pattern-matching on filenames | Step 3 is mandatory; quote real identifiers |
| Wrong numbers | Estimating instead of measuring | Step 2 — count, don't guess |
| Useless for the audience | Ignored Step 0 | Always set audience first |
| Vague "what it does" | Describing directories, not code | Read the file; say what it *actually* does |
| Broken output formats | Sloppy Typst/LaTeX | Check syntax, keep sections valid |
| Overwhelmed by huge repos | Trying to read everything | Entrypoints + hubs + sample; label the rest "overviewed" |
| Burying the lede | Leading with config files | Reading order: leaves → hubs → entrypoint; filter config/dotfiles |
| Making claims about generated/vendor code | Scanning lockfiles, bundles, `.g.dart` | Skip generated/vendor/minified; they add noise not understanding |

## Limitations (be honest with the user)

- Heuristic complexity is an **estimate**, not a guarantee.
- The skill reads code; it cannot run it. Runtime behavior, race conditions, or
  performance characteristics that aren't visible statically are "not verified".
- Very large monorepos get overview + deep-dive on key areas, not exhaustive coverage.
- This skill produces documents, not interactive graphs. For visual exploration,
  suggest [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything).
