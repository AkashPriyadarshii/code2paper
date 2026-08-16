# NEET-CBT-SITE — A Plain-Language Guide

## What is this?

The **marketing website** for the [NEET CBT 2027 Simulator](https://neet-cbt.vercel.app/) — a free,
offline practice app that replicates the NTA computer-based test interface for India's NEET UG
medical entrance exam (which goes computer-based in 2027).

This repo is **just the landing page** — a single HTML file with no build step, hosted on
GitHub Pages. The actual simulator app lives in a different repo
([AkashPriyadarshii/neet-cbt](https://github.com/AkashPriyadarshii/neet-cbt)).

## Numbers at a glance

- **Files:** 9 (4 text, 5 image)
- **Lines of code:** ~455 (index.html is 423 lines)
- **Languages:** HTML (index.html), Markdown (README), XML (sitemap), plain text (robots.txt)
- **Stack:** Static HTML + CSS, zero JavaScript, zero dependencies, zero build step

## How to run it

There is no app to run — it's a static page. Two ways to see it:

1. **Live:** https://akashpriyadarshii.github.io/neet-cbt-site/
2. **Locally:** open `index.html` in any browser, or `python -m http.server` and visit
   `http://localhost:8000`.

To deploy: push to the repo — GitHub Pages builds automatically (no build step).

## The big picture

```
[ index.html ]  ← the entire site (HTML + embedded CSS + JSON-LD schema)
     │
     ├── styles: navy/blue gov-style theme, CSS variables
     ├── content: hero → why-2027 → features → how-it-works → screenshots → FAQ
     └── SEO: OG/Twitter meta + 3 JSON-LD blocks (WebApplication, FAQPage, BreadcrumbList)
```

It's a one-page marketing site. The page sells the simulator app (hosted elsewhere) and
drives traffic to it via two "Launch the Simulator →" CTAs.

## What each file actually does

### `index.html` (423 LOC) — the whole site
- **What it does:** Single-file landing page. Contains the complete page markup, all CSS in a
  `<style>` block (no external stylesheets), and three JSON-LD schema blocks for SEO.
- **Key pieces:** CSS custom properties (`--navy`, `--accent`, `--paper`), the hero section with
  a CSS-drawn mock of the exam UI (question palette, timer, "mark for review" states), a features
  grid, an FAQ using native `<details>/<summary>` elements.
- **Patterns:** CSS variables for theming; grid layouts with `@media (max-width:820px)` collapse
  to single column; inline SVG-free icons (emoji in feature cards); semantic `<details>` FAQ.

### `README.md` (17 LOC) — what this repo is
- **What it does:** Two-paragraph description: it's the marketing site for the simulator,
  hosted on GitHub Pages, and lists the files.
- **Patterns:** None (plain Markdown).

### `robots.txt` + `sitemap.xml` — SEO plumbing
- **What it does:** `robots.txt` allows all crawlers and points to the sitemap; `sitemap.xml`
  lists the canonical URL with a monthly change frequency for search engines.

### The 5 images — screenshots & social
- `testneetscreen.webp`, `homecbt.webp`, `login.webp`, `scorecbt.webp` — real product screenshots
  (WebP, 2048×3640) shown in the gallery section.
- `og-cover.png` — 1200×630 social-share image used by the OG/Twitter meta tags.

## Suggested reading order (start here)

1. **`index.html`** — the whole thing is one file. Read the `<style>` block first to understand
   the design system (CSS variables = the theme), then the `<body>` in order: hero, why, features,
   how, FAQ, footer. The JSON-LD blocks at the bottom show how SEO is wired.
2. **`README.md`** — confirms the deployment model and image conventions.
3. **`robots.txt` + `sitemap.xml`** — 5 seconds each; they exist for search engines.

## Concepts & patterns glossary

- **CSS custom properties (variables):** the `:root{ --navy:...; --accent:... }` block defines the
  color theme once; every rule references variables instead of hardcoded hex.
- **Progressive Web App (PWA):** the simulator app is installable on phones; this marketing page
  only advertises it.
- **JSON-LD structured data:** three `<script type="application/ld+json">` blocks tell search
  engines this is a software app, a FAQ page, and a breadcrumb trail — that's what powers rich
  results in Google.
- **Native FAQ disclosure:** `<details>/<summary>` gives collapse/expand with zero JavaScript.

## Honest limitations

- This repo contains **no product code** — the simulator itself is in
  [AkashPriyadarshii/neet-cbt](https://github.com/AkashPriyadarshii/neet-cbt).
- I read all text files fully (index.html, README, robots, sitemap). The `.webp`/`.png` images
  were not pixel-inspected; their purpose is confirmed from filenames and their usage in markup.
