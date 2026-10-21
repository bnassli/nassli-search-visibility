# Changelog

## [0.2.0] — 2026-10-21 — Live baseline
- Read-only live audit of nassli-led.com.sa: confirmed WordPress/WooCommerce/WPML/Porto stack and no SEO plugin (`reports/baseline-2026-10-21.md`).
- Audit tool: canonical vs hreflang conflict, hreflang return links, duplicate titles, generic/domain titles and og:title, Arabic RTL, Product schema content (zero price, placeholder SKU), X-Robots-Tag, host-variant redirects, full sitemap walk with theme-template/user-archive detection. Arabic pages added to config. 6 → 15 tests.
- New P0 issues SEO-021…024; issue script creates agent/priority labels and fixes literal `
` in bodies.
- `AGENTS.md` is now the single rule file for Codex and Claude; unified branch names `codex/…` / `claude/…`; PR template asks whether the live site changed.
- Arabic brand spelling fixed as «نسلي» (owner decision).
- No changes to the live website.

## [0.1.0] — 2026-10-20 — Foundation
- Created bilingual project overview, agent coordination protocol, technical SEO and AI visibility strategy.
- Added bounded, read-only Python audit tool with tests and GitHub Actions.
- Seeded high-intent keyword clusters, page inventory, AI query panel, issue backlog, product and case-study templates.
- Added public-site initial observations and explicit verification requirements.
- No changes to live website or production hosting. Not pushed to GitHub yet.
