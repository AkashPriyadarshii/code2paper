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

DEFAULT_TYPST_TEMPLATE = r"""#set page(
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
    #text(18pt, weight: "bold")[ {title} ] \
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

def parse_gitignore(repo_path: Path) -> set:
    """Parse .gitignore rules if present."""
    ignored = set()
    gitignore_path = repo_path / ".gitignore"
    if gitignore_path.exists():
        try:
            for line in gitignore_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    ignored.add(line.rstrip("/"))
        except Exception:
            pass
    return ignored

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

    # Native fallback: scan text files with gitignore awareness
    custom_ignored = parse_gitignore(repo_path)
    ignore_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".idea", ".vscode"}.union(custom_ignored)
    ignore_exts = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".exe", ".dll", ".so", ".pyc", ".tar", ".gz", ".env", ".secrets"}

    packed = [f"=== Repository Context: {repo_path.name} ===\n"]
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith(".")]
        for file in files:
            if file.startswith(".env") or file in ignore_dirs:
                continue
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
    lines = packed_code.splitlines()
    files_found = [line.replace("--- File: ", "").strip() for line in lines if line.startswith("--- File: ")]

    abstract = f"This document presents the system architecture, component breakdown, and algorithmic specification of {title}. The codebase comprises {len(lines)} lines of structural representation across {len(files_found)} key source modules auto-analyzed by code2paper."
    overview = f"The repository `{repo_path.name}` implements a modular system. Primary source files analyzed:\n\n" + "\n".join([f"- `{f}`" for f in files_found[:15]])
    architecture = "```\n" + "\n".join([f"├── {f}" for f in files_found[:20]]) + "\n```"
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

def generate_html_paper_source(repo_path: Path, packed_code: str, title: str) -> str:
    """Generate standalone interactive HTML WebPaper (WebPDF fallback when typst is missing)."""
    lines = packed_code.splitlines()
    files_found = [line.replace("--- File: ", "").strip() for line in lines if line.startswith("--- File: ")]

    file_list_html = "".join([f"<li><code>{f}</code></li>" for f in files_found[:15]])
    tree_html = "\n".join([f"├── {f}" for f in files_found[:20]])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} -- Academic Specification (WebPaper)</title>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
  <style>
    :root {{
      --bg: #f4f5f7;
      --paper: #ffffff;
      --text: #1e293b;
      --muted: #64748b;
      --border: #e2e8f0;
      --accent: #2563eb;
    }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Times New Roman', Times, serif, sans-serif;
      line-height: 1.6;
      margin: 0;
      padding: 40px 20px;
    }}
    .paper {{
      max-width: 850px;
      margin: 0 auto;
      background: var(--paper);
      padding: 60px 80px;
      border-radius: 4px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.05);
      border: 1px solid var(--border);
    }}
    h1 {{
      font-size: 22pt;
      text-align: center;
      margin-bottom: 4px;
    }}
    .subtitle {{
      text-align: center;
      font-style: italic;
      color: var(--muted);
      font-size: 11pt;
      margin-bottom: 24px;
    }}
    .abstract {{
      background: #f8fafc;
      border-left: 4px solid var(--accent);
      padding: 16px;
      margin: 24px 0;
      font-size: 10pt;
    }}
    h2 {{
      font-size: 14pt;
      border-bottom: 1px solid var(--border);
      padding-bottom: 4px;
      margin-top: 32px;
      color: #0f172a;
    }}
    pre {{
      background: #0f172a;
      color: #38bdf8;
      padding: 16px;
      border-radius: 6px;
      font-family: monospace;
      font-size: 9.5pt;
      overflow-x: auto;
    }}
    .math-block {{
      background: #f8fafc;
      padding: 12px;
      text-align: center;
      font-size: 12pt;
      border-radius: 4px;
      margin: 16px 0;
    }}
    @media print {{
      body {{ background: #fff; padding: 0; }}
      .paper {{ box-shadow: none; border: none; padding: 0; max-width: 100%; }}
    }}
  </style>
</head>
<body>
  <div class="paper">
    <h1>{title}</h1>
    <div class="subtitle">An Automated Architectural Analysis & Specification (WebPaper)</div>
    <div class="abstract">
      <strong>Abstract</strong> -- This document presents the architectural topology, module dependencies, and algorithmic formalization of <code>{repo_path.name}</code>. Generated automatically via code2paper WebPaper engine.
    </div>

    <h2>1. System Overview</h2>
    <p>Repository comprises {len(lines)} lines across {len(files_found)} key source modules:</p>
    <ul>{file_list_html}</ul>

    <h2>2. Architecture Tree</h2>
    <pre>{tree_html}</pre>

    <h2>3. Core Modules & Formalization</h2>
    <div class="math-block">
      \\[ f(x) = \\text{{Transform}}(x) \\quad \\text{{where }} x \\in \\mathcal{{D}}_{{\\text{{codebase}}}} \\]
    </div>

    <h2>4. Implementation Trade-offs</h2>
    <ol>
      <li>Zero-CLI WebPaper rendering via browser print (Ctrl+P).</li>
      <li>AST packaging bound by stdlib memory capacity.</li>
    </ol>
  </div>
</body>
</html>"""

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

    # Always generate interactive HTML WebPaper fallback
    html_code = generate_html_paper_source(repo_path, packed, title)
    html_path = repo_path / "paper.html"
    html_path.write_text(html_code, encoding="utf-8")
    print(f"[code2paper] Generated Interactive WebPaper: {html_path}")

    typst_bin = shutil.which("typst")
    if typst_bin:
        out_pdf = Path(args.output).resolve()
        res = subprocess.run(["typst", "compile", str(typst_path), str(out_pdf)], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[code2paper] Successfully compiled PDF: {out_pdf}")
        else:
            print(f"[code2paper] Typst compilation failed:\n{res.stderr}", file=sys.stderr)
    else:
        print("[code2paper] 'typst' CLI not found. Generated 'paper.typ'. Install Typst to auto-compile PDF (https://typst.app).")

    if not args.keep_typst and typst_bin and (repo_path / "paper.typ").exists():
        os.remove(typst_path)

if __name__ == "__main__":
    main()
