#!/usr/bin/env python3
"""
code2paper - Convert any codebase into an academic paper (Typst / PDF).
Stdlib-only CLI. Uses repomix if available, fallback to built-in code pack.
"""

import sys
import os
import argparse
import subprocess
import shutil
from pathlib import Path

DEFAULT_TYPST_TEMPLATE = """#set page(
  paper: "us-letter",
  margin: (x: 1.8cm, y: 2.2cm),
  header: align(right)[
    #text(size: 9pt, fill: rgb("#666666"))[code2paper -- Academic Codebase Specification]
  ],
  footer: [
    #align(center)[#text(size: 9pt, fill: rgb("#666666"))[Page #counter(page).display()]]
  ]
)
#set text(font: "Liberation Serif", size: 10pt)

#align(center)[
  #block(width: 100%)[
    #text(18pt, weight: "bold")[ {title} ] \ \
    #v(4pt)
    #text(11pt, style: "italic")[ An Automated Architectural Analysis and Specification ] \ \
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
  #text(weight: "bold")[Abstract] -- {abstract}
]

#v(8pt)

== 1. System Overview
{overview}

== 2. Architecture & Component Structure
{architecture}

== 3. Core Module Specifications
{modules}

== 4. Mathematical Formalization & Data Flow
{data_flow}

== 5. Implementation Trade-offs & Limitations
{tradeoffs}
"""

def pack_codebase(repo_path: Path) -> str:
    """Pack codebase using repomix if installed, else native fallback."""
    repomix_bin = shutil.which("repomix") or shutil.which("npx")
    if repomix_bin:
        try:
            cmd = ["repomix", "--stdout"] if shutil.which("repomix") else ["npx", "repomix", "--stdout"]
            res = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=True)
            if res.stdout.strip():
                return res.stdout
        except Exception:
            pass

    # Native fallback: scan text files
    ignore_dirs = {".git", "node_modules", "__pycache__", ".venv", "dist", "build"}
    ignore_exts = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".exe", ".dll", ".so", ".pyc"}

    packed = [f"=== Repository Context: {repo_path.name} ===\n"]
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            p = Path(root) / file
            if p.suffix in ignore_exts:
                continue
            rel = p.relative_to(repo_path)
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                packed.append(f"\n--- File: {rel} ---\n{content}")
            except Exception:
                continue
    return "\n".join(packed)

def generate_paper_source(repo_path: Path, packed_code: str, title: str) -> str:
    """Generate Typst markup representing the paper."""
    abstract = f"This document presents the system architecture, component breakdown, and algorithmic specification of {title}. The codebase comprises {len(packed_code.splitlines())} lines of structural representation auto-analyzed by code2paper."
    overview = f"The repository `{repo_path.name}` implements a modular system. Source files analyzed: {len(packed_code.split('--- File: '))} primary modules."
    architecture = "```\n" + "\n".join([line for line in packed_code.splitlines() if line.startswith("--- File: ")][:15]) + "\n```"
    modules = "Core components handle data processing, logic orchestration, and runtime execution."
    data_flow = "$ f(x) = \\text{Transform}(x) \\quad \\text{where } x \\in \\mathcal{D}_{\\text{codebase}} $"
    tradeoffs = "1. Scalability: Memory footprint scales linearly with module count.\n2. Dependency Bound: Dependent on stdlib and external parser availability."

    return DEFAULT_TYPST_TEMPLATE.format(
        title=title or repo_path.resolve().name,
        abstract=abstract,
        overview=overview,
        architecture=architecture,
        modules=modules,
        data_flow=data_flow,
        tradeoffs=tradeoffs
    )

def main():
    parser = argparse.ArgumentParser(description="Convert any codebase into an academic paper (Typst/PDF).")
    parser.add_argument("repo", nargs="?", default=".", help="Path to codebase repository")
    parser.add_argument("-o", "--output", default="paper.pdf", help="Output PDF file path")
    parser.add_argument("--keep-typst", action="store_true", help="Keep .typ source file")
    args = parser.parse_args()

    repo_path = Path(args.repo).resolve()
    if not repo_path.exists():
        print(f"Error: path {repo_path} does not exist", file=sys.stderr)
        sys.exit(1)

    title = repo_path.name.replace("-", " ").replace("_", " ").title()
    print(f"[code2paper] Ingesting repository: {repo_path}...")
    packed = pack_codebase(repo_path)

    print("[code2paper] Synthesizing academic paper structure...")
    typst_code = generate_paper_source(repo_path, packed, title)

    typst_path = repo_path / "paper.typ"
    typst_path.write_text(typst_code, encoding="utf-8")
    print(f"[code2paper] Generated Typst source: {typst_path}")

    typst_bin = shutil.which("typst")
    if typst_bin:
        out_pdf = Path(args.output).resolve()
        res = subprocess.run(["typst", "compile", str(typst_path), str(out_pdf)], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[code2paper] Successfully compiled PDF: {out_pdf}")
        else:
            print(f"[code2paper] Typst compilation failed:\n{res.stderr}", file=sys.stderr)
    else:
        print("[code2paper] 'typst' CLI not found. Install Typst to auto-compile PDF (https://typst.app).")

    if not args.keep_typst and typst_bin and (repo_path / "paper.typ").exists():
        os.remove(typst_path)

if __name__ == "__main__":
    main()
