# PRD: code2paper

## Problem
Developers of all levels — beginners, vibecoders, and architects — struggle to understand
repositories they didn't write. Existing tools either pack code for LLMs (repomix),
index it for agents (repowise), or visualize it (Understand-Anything, graphify) — but
none produce a code-grounded *document* that explains a repo to a human.

## Target Audience
- FOSS Maintainers needing architectural whitepapers.
- Beginners & Vibecoders wanting a plain-language walkthrough of any repo.
- Advanced devs & architects wanting a formal academic spec.

## Positioning
**Skill-first.** The primary product is `skills/code2paper.md` — a universal agent skill
that works in any AI agent (Claude Code, OpenCode, Codex, Gemini CLI, Cursor) with zero
installation. The agent reads real code and writes verified explanations.

## Scope
1. Universal agent skill: inventory → measure → read → map deps → write `human-guide.md`
   + `paper.{md,typ,tex,html}`.
2. 100+ language support (2026 ecosystem) with import syntax, entrypoint conventions,
   function/class detection.
3. Landing page (GitHub Pages) + SEO.

## Non-Goals
- Shipping a CLI or any runtime dependency (the skill is self-contained).
- Reimplementing tree-sitter, embeddings, or MCP servers.
- Becoming a knowledge-graph viewer (Understand-Anything covers that).
- Interacting with code beyond static reading (no runtime analysis).
