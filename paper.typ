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
  #text(weight: "bold")[Abstract] -- This document presents the system architecture, component breakdown, and algorithmic specification of Code2Paper. The codebase comprises 1257 lines of structural representation across 15 key source modules auto-analyzed by code2paper.
]

#v(8pt)

== 1. System Overview
The repository `code2paper` implements a modular system. Primary source files analyzed:

- `AGENTS.md ---`
- `CLAUDE.md ---`
- `code2paper.py ---`
- `CONTRIBUTING.md ---`
- `index.html ---`
- `LICENSE ---`
- `paper.html ---`
- `paper.md ---`
- `paper.typ ---`
- `README.md ---`
- `docs\ARCHITECTURE.md ---`
- `docs\DESIGN.md ---`
- `docs\PRD.md ---`
- `docs\USAGE.md ---`
- `skills\code2paper.md ---`

== 2. Architecture & Component Structure
```
├── AGENTS.md ---
├── CLAUDE.md ---
├── code2paper.py ---
├── CONTRIBUTING.md ---
├── index.html ---
├── LICENSE ---
├── paper.html ---
├── paper.md ---
├── paper.typ ---
├── README.md ---
├── docs\ARCHITECTURE.md ---
├── docs\DESIGN.md ---
├── docs\PRD.md ---
├── docs\USAGE.md ---
├── skills\code2paper.md ---
```

== 3. Core Module Specifications
Core components handle data processing, logic orchestration, and runtime execution.

== 4. Mathematical Formalization & Data Flow
$ f(x) = \text{Transform}(x) \quad \text{where } x \in \mathcal{D}_{\text{codebase}} $

== 5. Implementation Trade-offs & Limitations
1. Scalability: Memory footprint scales linearly with module count.
2. Dependency Bound: Dependent on stdlib and external parser availability.
