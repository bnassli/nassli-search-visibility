# Changelog

## [0.3.0] — 2026-10-21 — Phase A for #21–#24 (after Codex review)
- Auditor: Arabic share measured inside `<main>` (menus/footers excluded) to separate translated pages from WPML fallbacks; `canonical_to_original_on_untranslated_review` vs critical `canonical_conflicts_with_hreflang`; `canonical_missing` / `canonical_multiple` split.
- Schema: `schema_offer_on_quote_only_page`, currency/availability reported per page, placeholder-SKU detection replaces the length>40 rule, optional `approved_sku_pattern`, missing/duplicate Product output.
- Sitemaps: `xhtml:link` hreflang parsing, Arabic URL counts per child, `sitemap_child_unreachable`, `sitemap_duplicate_urls`, `sitemap_has_no_arabic_urls`. Tests 15 → 30. Quote UI is detected from button class attributes (not site-wide CSS).
- Baseline report corrected per Codex (image claim retracted, plugin/author wording, USD/InStock facts).
- New: `docs/OWNER-DECISIONS.md`, `tracking/translation-matrix.csv`, `tracking/sitemap-inventory.csv`.
- No changes to the live website.

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
