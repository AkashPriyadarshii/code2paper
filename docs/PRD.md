# PRD: code2paper

## Problem
Vibecoders and FOSS developers build significant software repositories but lack formal academic write-ups (papers/whitepapers) for portfolios, documentation, or publication.

## Target Audience
- FOSS Maintainers needing architectural whitepapers.
- AI Engineers & Vibecoders wanting academic-style documentation for side projects.

## Scope
1. CLI tool (`code2paper.py`) taking a local repository path.
2. Ingests code with a stdlib `ast`/regex analyzer; optionally uses `repomix` for token-optimized context.
3. Emits Typst, LaTeX, HTML WebPaper, and Markdown outputs.
4. Compiles PDF using local `typst` compiler if installed.
5. Serves as a Claude Code Agent Skill (`skills/code2paper.md`).

## Non-Goals
- Full static-analysis linting or language servers (heuristic coverage only).
- Cloud/remote repository ingestion (local paths only).
