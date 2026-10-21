# Technical SEO & website implementation checklist

## 1. Discovery and index controls (audit first)
- Verify official canonical host and redirects for HTTP/HTTPS, www/non-www, trailing slash, product variation URLs and filtering/pagination.
- Inspect actual `robots.txt`, any CMS meta noindex, CDN/firewall rules, XML sitemap index, and Search Console coverage; do not guess from search preview.
- Use `robots.txt` for crawl instructions, not private content security. Don't disallow vital CSS/JS/media required for rendering.
- Check Googlebot, Bingbot and relevant AI search crawlers according to official policies; avoid blanket blocks without commercial decision.
- Sitemaps must list preferred indexable 200 pages, with accurate `lastmod` only when substantive change occurred.
- No blind `noindex` on product variations or category archives; review pagination & business value case-by-case.

## 2. SEO page anatomy
- One descriptive `<title>` and primary on-page H1 with customer intent, not generic ‘Welcome’.
- Original meta description and natural supporting headings; do not stuff keywords or mechanically enforce character counts.
- 200 HTTP status, valid self/appropriate canonical, indexable if intended, logical internal links.
- Visible product specifications in HTML tables plus downloadable PDF, accurate filenames and accessible photos.
- Intent-specific B2B conversion: **Request Quote / Submit RFQ / Download Datasheet**; avoid confusing cart if not supported by the sales workflow.
- Technical PDFs remain supporting assets; publish relevant readable HTML for search and AI citation retrieval.

## 3. Bilingual (English and Arabic)
- Decide on canonical URL pattern `/ar/`, language domain, or CMS language URLs; do not invent a path before inspecting CMS.
- For translated pairs: reciprocal alternate hreflang values `ar-SA` and `en-SA` (or suitable approved codes), each canonical to itself; x-default optionally home selector.
- `lang="ar" dir="rtl"` when appropriate; alt text in page language, correct fonts/RTL UI.
- No automatic machine translation of unverified technical specifications or certifications.
- Map each specific EN URL to equivalent AR URL; don't point all alternate pages at homepage.

## 4. Structured data (JSON-LD)
- `Organization` and appropriate `LocalBusiness` type, `BreadcrumbList`, `Product` where real product content exists, `Article` for valid guides. Validate with Rich Results Test and Schema.org validator.
- Only real attributes seen by users; no fake review stars, stock quantities or Offer/price fields on quote-only products.
- Do not claim that schema guarantees rich results or AI mentions.
- Example requiring real values: `examples/organization.schema.template.json` and `examples/product.schema.template.json`.

## 5. Performance and UX
- Capture PageSpeed Insights / Lighthouse mobile & desktop: LCP, INP, CLS, TTFB plus real CrUX data when available.
- Compress images, serve correct dimensions/formats, ensure hero LCP image is not lazy, defer noncritical scripts, avoid duplicate sliders/plugins.
- Measure after deployment and verify menus, Arabic layouts, product table, PDF links and quote form still work.
- Record screenshots and QA evidence in the PR; never change design unless approved.

## 6. CMS strategy
- Stack confirmed 2026-10-21: WordPress + WooCommerce + WPML + Porto child theme + Elementor Pro, **no SEO plugin**. Inspect WPML SEO settings, Woo templates, custom fields and caching/CDN in admin before choosing integration.
- Any SEO plugin chosen must support WPML (per-language titles, hreflang, sitemaps) and must replace — not duplicate — WooCommerce's Product JSON-LD.
- Prefer child theme / small versioned plugin over direct changes to parent theme or database content by SQL.
- Detect existing schema output and avoid duplicate Organization/Product JSON-LD injection.
- Deploy on staging, backup first, include rollback steps and record edited WordPress content separately.

## 7. Validation gates
- HTTP behavior, redirect loops, 404s, sitemap XML and index rules.
- Structured data syntax plus visible claim match.
- RFQ form validation, spam mitigation, success/error events, phone/WhatsApp click tracking.
- WCAG basics: heading order, alt, focus, contrast, mobile tap targets.
- SEO release watch: GSC coverage and 404 after 48h/7d/30d, baseline comparison.
