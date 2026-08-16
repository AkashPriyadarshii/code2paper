# NEET CBT 2027 Simulator — Marketing Site: Academic Specification

> Automated architectural analysis generated via the code2paper skill. All metrics measured
> from the actual repository; every claim verified by reading the source.

## Abstract

The repository hosts the static marketing site for the NEET CBT 2027 Simulator, a free,
offline-first progressive web application that replicates the National Testing Agency (NTA)
computer-based test interface for the NEET UG medical entrance examination, which transitions
to computer-based delivery in 2027. The site is a single-file HTML document (423 lines, 23.5 KB)
with embedded CSS and JSON-LD structured data, deployed via GitHub Pages with no build pipeline.
The repository contains 9 files across HTML, Markdown, XML, plain-text, and raster image assets;
source lines total approximately 455.

## 1. System Overview

| Metric | Value |
| --- | --- |
| Total files | 9 |
| Text files | 4 (index.html, README.md, robots.txt, sitemap.xml) |
| Image assets | 5 (.webp screenshots, og-cover.png) |
| Source lines (text) | ~455 |
| Build step | None (static) |
| Hosting | GitHub Pages (autodeploy on push) |
| Dependencies | Zero |

Language breakdown: HTML (index.html, 423 lines), Markdown (README, 17 lines), XML
(sitemap.xml, 9 lines), plain text (robots.txt).

## 2. Architecture & Component Structure

The site is a linear one-page document. Its structural units:

```
index.html
├── <head>
│   ├── primary/OG/Twitter meta (title, description, canonical, og:image)
│   └── <style> — CSS design system (custom properties + layout rules)
├── <body>
│   ├── .topbar        — announcement strip ("CBT begins 2027")
│   ├── header.main    — brand + nav (Why/Features/How/FAQ anchors)
│   ├── .hero          — headline, lead, dual CTA, stats badges, CSS mock-UI
│   ├── #why           — 4-card "OMR sheets are out" rationale grid
│   ├── #features      — 6-feature grid (NTA interface, timer, PWA, PYQ import, privacy)
│   ├── #how           — 3-step + 4-screenshot gallery
│   ├── #faq           — 6-item <details>/<summary> disclosure
│   └── footer         — links + NTA trademark disclaimer
└── 3 × JSON-LD blocks — WebApplication, FAQPage, BreadcrumbList
```

### Dependency Graph

- `index.html` → (references) → `testneetscreen.webp`, `homecbt.webp`, `login.webp`,
  `scorecbt.webp`, `og-cover.png`
- `index.html` → (links) → `https://neet-cbt.vercel.app/` (the simulator app), `#why`,
  `#features`, `#how`, `#faq` (same-page anchors)
- `robots.txt` → `sitemap.xml`
- No inter-repo code dependencies; the site is intentionally isolated from the app.

## 3. Core Module Specifications

### index.html — single-file landing page
- **Role:** the entire marketing site.
- **Design system:** CSS custom properties in `:root` (navy `#1a2b4a`, accent gold `#e8b23a`,
  blue `#1a56db`, paper `#f4f6fa`) giving a government-portal aesthetic; responsive breakpoint at
  820px collapsing all grids to single column.
- **CTA strategy:** two "Launch the Simulator →" buttons (hero + footer) funnel to the app;
  a secondary "Why the change?" scroll anchor for skeptical visitors.
- **Trust architecture:** stat badges (200+ questions, 100% offline, ₹0), six FAQ disclosures,
  and an explicit non-affiliation disclaimer with NTA trademark notice.
- **SEO:** descriptive title/description/keywords, OG + Twitter cards, canonical URL, three
  JSON-LD entities (WebApplication with `offers.price=0`, FAQPage with 5 questions,
  BreadcrumbList), theme-color meta.

### README.md — repository documentation
- Confirms deployment (GitHub Pages), documents image conventions (WebP at source size
  2048×3640), and the replace-and-push workflow.

### robots.txt / sitemap.xml — search-engine plumbing
- `robots.txt`: allow all, point to sitemap. `sitemap.xml`: canonical URL, monthly change
  frequency, dated 2026-08-10.

### Image assets
- Product screenshots (simulator in action, home, NTA-style login, score report) and an
  OpenGraph cover — all referenced by the gallery and social meta.

## 4. Mathematical Formalization & Data Flow

Let $F$ be the set of files and $\ell(f)$ the line count of file $f$.

Total text lines:
$$ L_{total} = \sum_{f \in F} \ell(f) = 423 + 17 + 9 + 5 \approx 455 $$

The data flow is unidirectional and static: a visitor's browser fetches `index.html` (plus the
four gallery WebP images, lazily loaded via `loading="lazy"`), the browser renders the embedded
CSS, and the three JSON-LD blocks are parsed by search-engine crawlers rather than executed.

Asset size footprint (bytes):
$$ S = 23{,}479 + 86{,}034 + 70{,}260 + 82{,}508 + 71{,}064 + 330{,}486 \approx 664\text{ KB} $$

No runtime computation occurs in this repository; all behavior lives in the external simulator
application.

## 5. Implementation Trade-offs & Limitations

1. **Single-file simplicity vs. maintainability:** zero build step and zero dependencies make
   the site trivially deployable and fast, at the cost of mixing markup, styles, and schema in
   one 423-line file.
2. **Isolation from the product:** the marketing page and the simulator are separate repos, so
   feature changes to the app do not touch the site; conversely the site cannot display app
   state dynamically.
3. **Static screenshots:** gallery images are static WebP captures; they cannot reflect future
   UI changes without regenerating assets.
4. **Scope:** this repository contains no test suite or CI beyond Pages autodeploy; appropriate
   given a static, dependency-free page.
