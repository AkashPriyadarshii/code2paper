# PRD: code2paper

## Problem
Vibecoders and FOSS developers build significant software repositories but lack formal academic write-ups (papers/whitepapers) for portfolios, documentation, or publication.

## Target Audience
- FOSS Maintainers needing architectural whitepapers.
- AI Engineers & Vibecoders wanting academic-style documentation for side projects.

## Scope
1. CLI tool (`code2paper`) taking a local repository path.
2. Ingests code using `repomix`.
3. Synthesizes a structured Typst/LaTeX document.
4. Compiles PDF using local `typst` compiler if installed.
5. Serves as a Claude Code Agent Skill (`skills/code2paper/SKILL.md`).
