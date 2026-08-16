#!/usr/bin/env python3
"""
code2paper - Convert any codebase into an academic paper
(Typst / LaTeX / HTML / Markdown / PDF). Stdlib-only CLI.
Uses repomix if available, fallback to built-in code pack.
"""

import sys
import os
import re
import ast
import html
import argparse
import subprocess
import shutil
import fnmatch
from pathlib import Path

MAX_FILE_BYTES = 1_000_000
IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
               ".idea", ".vscode", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache"}
IGNORE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".exe", ".dll", ".so",
               ".pyc", ".tar", ".gz", ".bin", ".woff", ".woff2", ".ttf", ".otf", ".ico",
               ".webp", ".mp4", ".mp3", ".wav", ".o", ".a", ".lock", ".min.js", ".svgz"}
OUTPUT_BASENAMES = {"paper.typ", "paper.html", "paper.md", "paper.tex", "paper.pdf"}


def parse_gitignore(repo_path: Path) -> set:
    """Parse .gitignore rules (positive patterns; negation unsupported)."""
    ignored = set()
    gitignore_path = repo_path / ".gitignore"
    if gitignore_path.exists():
        try:
            for line in gitignore_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("!"):
                    ignored.add(line.rstrip("/"))
        except Exception:
            pass
    return ignored


def is_ignored(rel, patterns) -> bool:
    """Match a relative path (with / separators) against gitignore patterns."""
    rel = rel.replace("\\", "/")
    parts = rel.split("/")
    for pat in patterns:
        pat = pat.replace("\\", "/").rstrip("/")
        if not pat:
            continue
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(parts[-1], pat):
            return True
        if "/" in pat:
            for i in range(1, len(parts)):
                if fnmatch.fnmatch("/".join(parts[:i]), pat):
                    return True
        else:
            if pat in parts:
                return True
    return False


def _within(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def iter_source_files(repo_path: Path, patterns: set,
                      exclude_basenames=frozenset(), exclude_prefixes=()) -> list:
    """Walk repo and return [(abs_path, rel_path)] honoring gitignore, size, exclusions."""
    results = []
    repo_str = str(repo_path)
    for root, dirs, files in os.walk(repo_path):
        root_path = Path(root)
        pruned = []
        for d in dirs:
            rel_d = root_path.relative_to(repo_path) / d
            if any(rel_d.parts[:len(p)] == p for p in exclude_prefixes):
                continue
            if d in IGNORE_DIRS or d.startswith("."):
                continue
            if is_ignored(str(rel_d), patterns):
                continue
            pruned.append(d)
        dirs[:] = pruned
        for name in files:
            rel = root_path.relative_to(repo_path) / name
            if name in exclude_basenames or rel.name in exclude_basenames:
                continue
            if any(rel.parts[:len(p)] == p for p in exclude_prefixes):
                continue
            if name.startswith(".env") or name == ".secrets":
                continue
            ext = Path(name).suffix.lower()
            if ext in IGNORE_EXTS:
                continue
            if is_ignored(str(rel), patterns):
                continue
            p = root_path / name
            try:
                if p.stat().st_size > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            results.append((str(p), str(rel).replace("\\", "/")))
    return results


def scan_file(path: str, rel: str) -> dict:
    """Read a file with binary sniffing; return text, real line count, size."""
    try:
        raw = Path(path).read_bytes()
    except OSError:
        return None
    if b"\x00" in raw[:8192]:
        return None
    text = raw.decode("utf-8", errors="replace")
    lines = raw.count(b"\n") + (0 if raw.endswith(b"\n") else 1)
    return {"rel": rel, "text": text, "lines": lines, "size": len(raw)}


def _norm_ext(rel: str) -> str:
    if rel.endswith((".py", ".pyi")):
        return ".py"
    return Path(rel).suffix.lower()


def analyze_python(info: dict) -> dict:
    """AST-based inventory: functions, classes, imports, cyclomatic complexity."""
    try:
        tree = ast.parse(info["text"])
    except SyntaxError:
        return analyze_generic(info)
    funcs, classes, imports, complexity = [], [], [], 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = ast.unparse(node.args) if hasattr(ast, "unparse") else "..."
            funcs.append(f"{node.name}({args})")
            complexity += 1
        elif isinstance(node, ast.ClassDef):
            methods = [m.name for m in node.body
                       if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
            classes.append(f"{node.name}({', '.join(methods)})")
            complexity += 1
        elif isinstance(node, ast.Import):
            imports.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
        elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With,
                               ast.BoolOp, ast.ListComp, ast.DictComp, ast.SetComp,
                               ast.GeneratorExp)):
            complexity += 1
    return {**info, "ext": ".py", "funcs": funcs[:20], "classes": classes[:10],
            "imports": imports[:10], "complexity": complexity}


def analyze_generic(info: dict) -> dict:
    """Regex heuristic inventory for non-Python languages (honest estimate)."""
    text = info["text"]
    funcs, classes = [], []
    complexity = 0
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith(("//", "#", "/*", "*", "--", "<!--")):
            continue
        complexity += sum(s.count(k) for k in ("if ", "for ", "while ", "&&", "||", "? "))
        fm = re.match(r"^(?:export\s+|default\s+|async\s+)*(?:function\s+)?"
                      r"([A-Za-z_]\w*)\s*\([^)]*\)\s*(?:\{|=>|\()", s)
        if fm:
            name = fm.group(1)
            if name not in ("if", "for", "while", "switch", "return", "print", "puts"):
                funcs.append(f"{name}(...)")
        cm = re.match(r"^(?:export\s+|abstract\s+|final\s+)*(?:class|struct|interface)\s+"
                      r"([A-Za-z_]\w*)", s)
        if cm:
            classes.append(cm.group(1))
    return {**info, "ext": _norm_ext(info["rel"]), "funcs": list(dict.fromkeys(funcs))[:20],
            "classes": list(dict.fromkeys(classes))[:10], "imports": [], "complexity": complexity}


def analyze_file(info: dict) -> dict:
    if info["rel"].endswith((".py", ".pyi")):
        return analyze_python(info)
    return analyze_generic(info)


def build_deps(files: list) -> list:
    """Internal Python import dependency edges (local files only)."""
    stems = {}
    for f in files:
        if f["ext"] == ".py":
            stems[Path(f["rel"]).stem] = f["rel"]
    deps = []
    for f in files:
        if f["ext"] != ".py":
            continue
        for imp in f["imports"]:
            root = imp.split(".")[0]
            if root in stems and stems[root] != f["rel"]:
                deps.append((f["rel"], stems[root]))
    return sorted(set(deps))


def build_report(repo_path: Path, title: str, exclude_basenames=frozenset(),
                 exclude_prefixes=()) -> dict:
    patterns = parse_gitignore(repo_path)
    files = []
    for path, rel in iter_source_files(repo_path, patterns, exclude_basenames, exclude_prefixes):
        info = scan_file(path, rel)
        if info is not None:
            files.append(analyze_file(info))
    by_ext = {}
    for f in files:
        ext = f["ext"] or "(none)"
        by_ext.setdefault(ext, [0, 0])
        by_ext[ext][0] += 1
        by_ext[ext][1] += f["lines"]
    return {
        "repo": repo_path.resolve().name,
        "title": title,
        "files": files,
        "total_files": len(files),
        "total_lines": sum(f["lines"] for f in files),
        "total_complexity": sum(f["complexity"] for f in files),
        "by_ext": sorted(by_ext.items(), key=lambda kv: -kv[1][1]),
        "deps": build_deps(files),
    }


def pack_codebase(repo_path: Path, patterns: set, exclude_basenames=frozenset(),
                  exclude_prefixes=()) -> str:
    """Pack codebase using repomix if installed, else native fallback."""
    repomix_bin = shutil.which("repomix")
    if repomix_bin:
        try:
            cmd = [repomix_bin, "--stdout"]
            if exclude_basenames:
                cmd += ["--ignore", ",".join(sorted(exclude_basenames))]
            res = subprocess.run(cmd, cwd=str(repo_path), capture_output=True,
                                 text=True, check=True, timeout=120)
            if res.stdout.strip():
                return res.stdout
        except Exception:
            pass

    packed = [f"=== Repository Context: {repo_path.name} ===\n"]
    for path, rel in iter_source_files(repo_path, patterns, exclude_basenames, exclude_prefixes):
        info = scan_file(path, rel)
        if info is None:
            continue
        packed.append(f"\n--- File: {rel} ---\n{info['text']}")
    return "\n".join(packed)


# --- escaping ---------------------------------------------------------------

def typst_escape(s: str) -> str:
    return (s.replace("\\", "\\\\").replace("#", "\\#").replace("$", "\\$")
            .replace("@", "\\@").replace("{", "\\{").replace("}", "\\}"))


def latex_escape(s: str) -> str:
    return (s.replace("\\", r"\textbackslash{}").replace("{", r"\{").replace("}", r"\}")
            .replace("#", r"\#").replace("$", r"\$").replace("%", r"\%")
            .replace("&", r"\&").replace("_", r"\_").replace("^", r"\^{}")
            .replace("~", r"\textasciitilde{}"))


def render_template(template: str, **kwargs) -> str:
    for key, val in kwargs.items():
        template = template.replace("{{" + key + "}}", val)
    return template


# --- report sections --------------------------------------------------------

def _sections(report: dict, title: str) -> dict:
    repo = report["repo"]
    top = sorted(report["files"], key=lambda f: -f["lines"])[:12]
    lang_rows = "\n".join(
        f"- `{ext}`: {n} files, {lines} lines"
        for ext, (n, lines) in report["by_ext"])
    lang_plain = "\n".join(
        f"- {ext}: {n} files, {lines} lines"
        for ext, (n, lines) in report["by_ext"])

    overview = (f"The repository `{repo}` implements a modular system analyzed by "
                f"code2paper. It contains {report['total_files']} source files totaling "
                f"{report['total_lines']} lines of code with an estimated cyclomatic "
                f"complexity of {report['total_complexity']}.\n\nLanguage breakdown:\n{lang_rows}")
    overview_plain = (f"The repository {repo} implements a modular system analyzed by "
                      f"code2paper. It contains {report['total_files']} source files totaling "
                      f"{report['total_lines']} lines of code with an estimated cyclomatic "
                      f"complexity of {report['total_complexity']}.\n\n"
                      f"Language breakdown:\n{lang_plain}")

    tree_lines = "\n".join(f"├── {f['rel']} ({f['lines']} LOC)" for f in top)
    deps_txt = "\n".join(f"- `{a}` -> `{b}`" for a, b in report["deps"][:15])
    if not deps_txt:
        deps_txt = "- No internal dependency edges detected."
    architecture = f"```\n{repo}/\n{tree_lines}\n```\n\nDependency graph (top 15):\n{deps_txt}"

    module_blocks = []
    for f in top:
        sigs = "\n".join(f"  - `{typst_escape(s)}`" for s in f["funcs"][:10])
        classes = "\n".join(f"  - `{typst_escape(c)}`" for c in f["classes"][:6])
        module_blocks.append(
            f"- **`{typst_escape(f['rel'])}`** — {f['lines']} LOC, complexity {f['complexity']}\n"
            f"{classes}\n{sigs}".rstrip())
    modules = "\n".join(module_blocks) if module_blocks else "No analyzable modules detected."

    tl, tc, deps_n = report["total_lines"], report["total_complexity"], len(report["deps"])
    df_math = [
        f"$ L_total = sum_(f in F) ell(f) = {tl} $",
        f"$ C_total = sum_(f in F) c(f) = {tc} $",
        f"$ |E| = {deps_n} $",
    ]
    df_prose = ("Data flows along internal import edges; for Python modules the graph "
                "above lists concrete `from -> to` dependency chains.")
    data_flow = (df_math, df_prose)

    tradeoffs = ("1. Scalability: memory footprint scales linearly with module count; "
                 "context packing is capped at per-file limits to bound resource usage.\n"
                 "2. Language Coverage: Python modules get full AST analysis; other languages "
                 "use regex heuristics (function/class estimates, not bytecode-accurate).\n"
                 "3. Dependency Bound: relies on stdlib and optional external tooling "
                 "(repomix, typst); absent tools degrade gracefully.\n"
                 f"4. Complexity Estimates: {tc} is an estimated cyclomatic complexity "
                 "across all files, dominated by control-flow constructs.")
    return {"title": title, "repo": repo, "overview": overview,
            "overview_plain": overview_plain, "architecture": architecture,
            "modules": modules, "data_flow": data_flow, "tradeoffs": tradeoffs}


# --- renderers ---------------------------------------------------------------

TYPST_TEMPLATE = r"""#set page(
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
    #text(18pt, weight: "bold")[ {{title}} ] \
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
  #text(weight: "bold")[Abstract] -- {{overview}}
]

#v(8pt)

== 1. System Overview
{{overview}}

== 2. Architecture & Component Structure
{{architecture}}

== 3. Core Module Specifications
{{modules}}

== 4. Mathematical Formalization & Data Flow
{{data_flow}}

== 5. Implementation Trade-offs & Limitations
{{tradeoffs}}
"""


def generate_paper_source(report: dict, title: str) -> str:
    s = _sections(report, title)
    df_math, df_prose = s["data_flow"]
    data_flow = "\n\n".join(df_math) + "\n\n" + typst_escape(df_prose)
    return render_template(TYPST_TEMPLATE,
                           title=typst_escape(s["title"]),
                           overview=typst_escape(s["overview"]),
                           architecture=s["architecture"],
                           modules=s["modules"],
                           data_flow=data_flow,
                           tradeoffs=typst_escape(s["tradeoffs"]))


def generate_latex_source(report: dict, title: str) -> str:
    s = _sections(report, title)
    top = sorted(report["files"], key=lambda f: -f["lines"])[:12]
    mods = []
    for f in top:
        sigs = "".join(f"\\item \\texttt{{{latex_escape(x)}}}\n" for x in f["funcs"][:10])
        cls = "".join(f"\\item \\texttt{{{latex_escape(c)}}}\n" for c in f["classes"][:6])
        mods.append(
            f"\\subsubsection*{{{latex_escape(f['rel'])}}}\n"
            f"{f['lines']} LOC, complexity {f['complexity']}\n"
            f"\\begin{{itemize}}\n{cls}{sigs}\\end{{itemize}}")
    deps = "".join(f"\\item \\texttt{{{latex_escape(a)}}} $\\rightarrow$ \\texttt{{{latex_escape(b)}}}\n"
                   for a, b in report["deps"][:15])
    lang = "".join(f"\\item \\texttt{{{ext}}}: {n} files, {lines} lines\n"
                   for ext, (n, lines) in report["by_ext"])
    tree = "\n".join(f"\\texttt{{{latex_escape(f['rel'])} ({f['lines']} LOC)}}" for f in top)
    return f"""\\documentclass[11pt]{{article}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{amsmath,amssymb}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}
\\title{{{latex_escape(s['title'])}}}
\\author{{code2paper -- Automated Architectural Analysis}}
\\date{{}}

\\begin{{document}}
\\maketitle

\\begin{{abstract}}
{latex_escape(s['overview_plain'])}
\\end{{abstract}}

\\section{{System Overview}}
{latex_escape(s['overview_plain'])}

\\subsection{{Language Breakdown}}
\\begin{{itemize}}
{lang}\\end{{itemize}}

\\section{{Architecture \\& Component Structure}}
\\begin{{itemize}}
{tree}
\\end{{itemize}}

\\subsection{{Dependency Graph}}
\\begin{{itemize}}
{deps}\\end{{itemize}}

\\section{{Core Module Specifications}}
{mods}

\\section{{Mathematical Formalization \\& Data Flow}}
Total lines of code:
\\[ L_{{\\text{{total}}}} = \\sum_{{f \\in F}} \\ell(f) = {report['total_lines']} \\]
Estimated cyclomatic complexity:
\\[ C_{{\\text{{total}}}} = \\sum_{{f \\in F}} c(f) = {report['total_complexity']} \\]
Internal dependency edges:
\\[ |E| = {len(report['deps'])} \\]

\\section{{Implementation Trade-offs \\& Limitations}}
{s['tradeoffs']}
\\end{{document}}
"""


def generate_html_paper_source(report: dict, title: str) -> str:
    s = _sections(report, title)
    top = sorted(report["files"], key=lambda f: -f["lines"])[:15]
    file_list = "".join(
        f"<li><code>{html.escape(f['rel'])}</code> &mdash; {f['lines']} LOC, "
        f"complexity {f['complexity']}</li>" for f in top)
    deps = "".join(
        f"<li><code>{html.escape(a)}</code> &rarr; <code>{html.escape(b)}</code></li>"
        for a, b in report["deps"][:15])
    lang = "".join(
        f"<tr><td><code>{html.escape(ext)}</code></td><td>{n}</td><td>{lines}</td></tr>"
        for ext, (n, lines) in report["by_ext"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(s['title'])} -- Academic Specification (WebPaper)</title>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
  <style>
    :root {{
      --bg: #f4f5f7; --paper: #ffffff; --text: #1e293b;
      --muted: #64748b; --border: #e2e8f0; --accent: #2563eb;
    }}
    body {{
      background: var(--bg); color: var(--text);
      font-family: 'Times New Roman', Times, serif;
      line-height: 1.6; margin: 0; padding: 40px 20px;
    }}
    .paper {{
      max-width: 850px; margin: 0 auto; background: var(--paper);
      padding: 60px 80px; border-radius: 4px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid var(--border);
    }}
    h1 {{ font-size: 22pt; text-align: center; margin-bottom: 4px; }}
    .subtitle {{ text-align: center; font-style: italic; color: var(--muted);
                 font-size: 11pt; margin-bottom: 24px; }}
    .abstract {{ background: #f8fafc; border-left: 4px solid var(--accent);
                 padding: 16px; margin: 24px 0; font-size: 10pt; }}
    h2 {{ font-size: 14pt; border-bottom: 1px solid var(--border);
         padding-bottom: 4px; margin-top: 32px; color: #0f172a; }}
    pre {{ background: #0f172a; color: #38bdf8; padding: 16px; border-radius: 6px;
          font-family: monospace; font-size: 9.5pt; overflow-x: auto; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 10pt; }}
    td, th {{ border: 1px solid var(--border); padding: 6px 10px; text-align: left; }}
    .math-block {{ background: #f8fafc; padding: 12px; text-align: center;
                  font-size: 12pt; border-radius: 4px; margin: 16px 0; }}
    @media print {{
      body {{ background: #fff; padding: 0; }}
      .paper {{ box-shadow: none; border: none; padding: 0; max-width: 100%; }}
    }}
  </style>
</head>
<body>
  <div class="paper">
    <h1>{html.escape(s['title'])}</h1>
    <div class="subtitle">An Automated Architectural Analysis & Specification (WebPaper)</div>
    <div class="abstract">
      <strong>Abstract</strong> -- {html.escape(s['overview'])}
    </div>

    <h2>1. System Overview</h2>
    <p>Repository <code>{html.escape(report['repo'])}</code> &mdash;
       {report['total_files']} files, {report['total_lines']} LOC,
       estimated complexity {report['total_complexity']}.</p>
    <table><tr><th>Language</th><th>Files</th><th>Lines</th></tr>{lang}</table>

    <h2>2. Architecture & Dependency Graph</h2>
    <pre>{html.escape("\n".join(f"{f['rel']} ({f['lines']} LOC)" for f in top))}</pre>
    <ul>{deps or "<li>No internal dependency edges detected.</li>"}</ul>

    <h2>3. Core Modules & Formalization</h2>
    <ul>{file_list}</ul>
    <div class="math-block">
      \\[ L_{{\\text{{total}}}} = \\sum_{{f \\in F}} \\ell(f) = {report['total_lines']} \\]
      \\[ C_{{\\text{{total}}}} = \\sum_{{f \\in F}} c(f) = {report['total_complexity']} \\]
      \\[ |E| = {len(report['deps'])} \\]
    </div>

    <h2>4. Implementation Trade-offs</h2>
    <ol>
      <li>Zero-CLI WebPaper rendering via browser print (Ctrl+P).</li>
      <li>AST packaging bound by stdlib memory capacity.</li>
      <li>Python modules analyzed via AST; other languages via regex heuristics.</li>
    </ol>
  </div>
</body>
</html>"""


def generate_markdown_source(report: dict, title: str) -> str:
    s = _sections(report, title)
    top = sorted(report["files"], key=lambda f: -f["lines"])[:15]
    rows = "".join(f"| `{f['rel']}` | {f['lines']} | {f['complexity']} | "
                   f"{', '.join(f['funcs'][:4])} |\n" for f in top)
    deps = "\n".join(f"- `{a}` -> `{b}`" for a, b in report["deps"][:15])
    lang = "\n".join(f"- `{ext}`: {n} files, {lines} lines"
                     for ext, (n, lines) in report["by_ext"])
    return f"""# {title}

> Automated architectural analysis and specification generated via code2paper.

## Abstract

{html.escape(s['overview'])}

## 1. System Overview

Repository: **{report['repo']}** -- {report['total_files']} files, {report['total_lines']} LOC,
estimated cyclomatic complexity {report['total_complexity']}.

### Language Breakdown

{lang}

## 2. Architecture & Component Structure

| Module | LOC | Complexity | Functions/Classes |
| --- | ---: | ---: | --- |
{rows}

## 3. Dependency Graph

{deps if deps else "No internal dependency edges detected."}

## 4. Mathematical Formalization & Data Flow

- Total lines of code: $L_{{total}} = \\sum_{{f \\in F}} \\ell(f) = {report['total_lines']}$
- Estimated cyclomatic complexity: $C_{{total}} = \\sum_{{f \\in F}} c(f) = {report['total_complexity']}$
- Internal dependency edges: $|E| = {len(report['deps'])}$

## 5. Implementation Trade-offs & Limitations

{html.escape(s['tradeoffs'])}
"""


def main():
    parser = argparse.ArgumentParser(description="Convert any codebase into an academic paper (Typst/LaTeX/HTML/PDF).")
    parser.add_argument("repo", nargs="?", default=".", help="Path to codebase repository")
    parser.add_argument("-o", "--output", default=None, help="Output PDF file path")
    parser.add_argument("--out-dir", default=".", help="Directory for generated source files (default: current dir)")
    parser.add_argument("--keep-typst", action="store_true", help="Keep .typ source file")
    args = parser.parse_args()

    repo_path = Path(args.repo).resolve()
    if not repo_path.exists():
        print(f"Error: path {repo_path} does not exist", file=sys.stderr)
        sys.exit(1)
    if not repo_path.is_dir():
        print(f"Error: path {repo_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    exclude_prefixes = []
    if _within(out_dir, repo_path):
        rel_parts = out_dir.relative_to(repo_path).parts
        if rel_parts:
            exclude_prefixes.append(rel_parts)

    title = repo_path.name.replace("-", " ").replace("_", " ").title()
    print(f"[code2paper] Ingesting repository: {repo_path}...")

    patterns = parse_gitignore(repo_path)
    report = build_report(repo_path, title, OUTPUT_BASENAMES, exclude_prefixes)

    print(f"[code2paper] {report['total_files']} files, {report['total_lines']} LOC, "
          f"complexity {report['total_complexity']}, {len(report['deps'])} deps")

    typst_code = generate_paper_source(report, title)
    tex_code = generate_latex_source(report, title)
    html_code = generate_html_paper_source(report, title)
    md_code = generate_markdown_source(report, title)

    typst_path = out_dir / "paper.typ"
    tex_path = out_dir / "paper.tex"
    html_path = out_dir / "paper.html"
    md_path = out_dir / "paper.md"
    typst_path.write_text(typst_code, encoding="utf-8")
    tex_path.write_text(tex_code, encoding="utf-8")
    html_path.write_text(html_code, encoding="utf-8")
    md_path.write_text(md_code, encoding="utf-8")
    for p in (typst_path, tex_path, html_path, md_path):
        print(f"[code2paper] Generated: {p}")

    typst_bin = shutil.which("typst")
    if typst_bin:
        pdf_path = Path(args.output).resolve() if args.output else (out_dir / "paper.pdf")
        res = subprocess.run([typst_bin, "compile", str(typst_path), str(pdf_path)],
                             capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[code2paper] Successfully compiled PDF: {pdf_path}")
        else:
            print(f"[code2paper] Typst compilation failed:\n{res.stderr}", file=sys.stderr)
    else:
        print("[code2paper] 'typst' CLI not found. Install Typst to auto-compile PDF (https://typst.app).")

    if not args.keep_typst and typst_bin and typst_path.exists():
        typst_path.unlink()


if __name__ == "__main__":
    main()
