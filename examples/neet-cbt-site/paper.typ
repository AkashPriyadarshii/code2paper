#set page(paper: "us-letter", margin: (x: 1.8cm, y: 2.2cm))
#set text(font: ("Times New Roman", "Liberation Serif", "Arial", "DejaVu Serif"), size: 10pt)

#align(center)[
  #text(18pt, weight: "bold")[NEET CBT 2027 Simulator -- Marketing Site] \
  #v(4pt)
  #text(11pt, style: "italic")[Academic Specification -- Automated Architectural Analysis via code2paper] \
]

#v(10pt)

#block(fill: rgb("#f8f9fa"), inset: 12pt, radius: 4pt, stroke: 0.5pt + rgb("#e9ecef"))[
  #text(weight: "bold")[Abstract] -- The repository hosts the static marketing site for the NEET CBT 2027
  Simulator, a free, offline-first progressive web application that replicates the National Testing
  Agency (NTA) computer-based test interface for the NEET UG medical entrance examination. The site is a
  single-file HTML document (423 lines, 23.5 KB) with embedded CSS and JSON-LD structured data, deployed
  via GitHub Pages with no build pipeline. The repository contains 9 files across HTML, Markdown, XML,
  plain-text, and raster image assets; source lines total approximately 455.
]

== 1. System Overview

#table(
  columns: 2,
  [Metric], [Value],
  [Total files], [9],
  [Text files], [4 (index.html, README.md, robots.txt, sitemap.xml)],
  [Image assets], [5 (.webp screenshots, og-cover.png)],
  [Source lines (text)], [~455],
  [Build step], [None (static)],
  [Hosting], [GitHub Pages (autodeploy on push)],
  [Dependencies], [Zero],
)

Language breakdown: HTML (index.html, 423 lines), Markdown (README, 17 lines), XML (sitemap.xml, 9 lines), plain text (robots.txt).

== 2. Architecture & Component Structure

The site is a linear one-page document:

```
index.html
├── <head>    primary/OG/Twitter meta + <style> design system
├── <body>
│   ├── .topbar      — announcement strip
│   ├── header.main  — brand + nav
│   ├── .hero        — headline, lead, dual CTA, stats badges, CSS mock-UI
│   ├── #why         — 4-card rationale grid
│   ├── #features    — 6-feature grid
│   ├── #how         — 3-step + 4-screenshot gallery
│   ├── #faq         — 6-item <details> disclosure
│   └── footer       — links + NTA trademark disclaimer
└── 3 × JSON-LD blocks — WebApplication, FAQPage, BreadcrumbList
```

=== Dependency Graph

- `index.html` -> references 4 gallery WebP + `og-cover.png`
- `index.html` -> links to https://neet-cbt.vercel.app/ (the app) + same-page anchors
- `robots.txt` -> `sitemap.xml`

== 3. Core Module Specifications

=== index.html — single-file landing page

- **Role:** the entire marketing site.
- **Design system:** CSS custom properties in `:root` (navy, accent gold, blue, paper), responsive at 820px.
- **CTA strategy:** two "Launch the Simulator" buttons funnel to the app; "Why the change?" scroll anchor.
- **Trust architecture:** stat badges, six FAQ disclosures, non-affiliation disclaimer.
- **SEO:** descriptive meta, OG + Twitter cards, canonical, three JSON-LD entities, theme-color.

=== README.md

Confirms GitHub Pages hosting and image conventions (WebP at 2048x3640).

=== robots.txt / sitemap.xml

Allow all crawlers; sitemap with monthly change frequency, dated 2026-08-10.

== 4. Mathematical Formalization & Data Flow

Let $F$ be the set of files and $ell(f)$ the line count of file $f$.

$ L_text(total) = sum_(f in F) ell(f) = 423 + 17 + 9 + 5 approx 455 $

Asset size footprint (bytes):

$ S = 23,479 + 86,034 + 70,260 + 82,508 + 71,064 + 330,486 approx 664 "KB" $

Data flow is unidirectional and static: the browser fetches `index.html` plus lazily-loaded
gallery images; JSON-LD blocks are parsed by crawlers, not executed. No runtime computation occurs here.

== 5. Implementation Trade-offs & Limitations

1. Single-file simplicity vs. maintainability: zero build, zero deps, at the cost of a 423-line file.
2. Isolation from the product: marketing site and simulator are separate repos.
3. Static screenshots: WebP captures cannot reflect future UI changes automatically.
4. Scope: no test suite or CI beyond Pages autodeploy; appropriate for a static page.
