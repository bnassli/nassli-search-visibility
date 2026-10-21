# First issues to create in GitHub

Issue titles must include stable ID to avoid duplication. Each item is a deliverable with verification, not a vague reminder. Owners are unassigned until owner decides.

## SEO-001 · Set up private GitHub collaboration rules (P0)
**Description:** Publish repo, ensure access for owner and both assistant connectors, require PRs and passing CI on `main`.
**Acceptance:** owner confirms repo; 2 agent workflows can read; branch protection configured; test PR passes. No production deployment.

## SEO-002 · Read-only website source and infrastructure inventory (P0)
**Description:** Identify CMS/framework/version, hosting, site source repo, template system, SEO/multilingual/forms/plugins, backup/staging/CDN.
**Acceptance:** documented stack + rollback + accessible staging and a successful restore dry-run; do not commit private production data.

## SEO-003 · Capture search/index/performance/RFQ baseline (P0)
**Description:** Run configured audit; inspect GSC/Bing/GA4 (with owner), export metrics to sanitized aggregates, document sampling limitations.
**Acceptance:** evidence of canonical host, crawl status, sitemap, top pages, Core Web Vitals and qualified leads baseline. Unknowns labeled.

## SEO-004 · Approve official Nassli identity and factual claims (P0)
**Description:** Verify dates (factory vs group), official name, factory address/phone/email, legal product claims, approved project references.
**Acceptance:** signed off by authorized management/technical reviewers, stored as reviewed source-of-truth. No fabricated certifications.

## SEO-005 · Homepage metadata, copy, author artifact cleanup (P0)
**Description:** Fix generic `Welcome` message, confirm author/date leak, validate EN/AR copy and CTA while preserving visual design.
**Acceptance:** title/H1/message clearly says Saudi LED manufacturer; artifact gone after confirming it is a bug; CWV not worse; owner approves.

## SEO-006 · Canonical, robots, sitemap and indexing defects (P0)
**Description:** Crawl actual URL sample and map desired indexable pages; fix verified defects only.
**Acceptance:** HTTP canonical consistency, sitemap populated, no unexpected noindex, no redirected URLs in sitemap, owner approval for changes.

## SEO-007 · Translate & map bilingual priority pages (P1)
**Description:** Define exact Arabic/English equivalents, URL conventions and hreflang for 5 business pages.
**Acceptance:** reciprocal language tags, indexable canonical, RTL reviewed, no same-language/duplicate mismatches.

## SEO-008 · Organization & Product JSON-LD pilot (P1)
**Description:** Detect existing schema, implement a verified fact-based Organization block and one real Product with proper Offer omission.
**Acceptance:** page-visible match, validation passes, no duplicate competing blocks or invented offers.

## SEO-009 · High-intent LED UP LIGHT product/RFQ pilot (P0)
**Description:** Create an engineer-reviewed SKU page with table, PDF, real imagery, FAQ and quote path; avoid unverified ratings.
**Acceptance:** real datasheet, working quote form and tracking, responsive design, documented technical approval.

## SEO-010 · RFQ conversion measurement with privacy (P0)
**Description:** Track form starts, successful server-validated submissions, technical downloads and contact clicks to GA4 and CRM where applicable.
**Acceptance:** no personal data in GA4, confirmed event once per successful RFQ, spam/noise control, test evidence.

## SEO-011 · Priority categories & internal links (P1)
**Description:** Original EN/AR pages for Custom Linear, Facade, Office, High Bay and Outdoor lighting.
**Acceptance:** buyer-oriented helpful text, real related products, sensible schema, consistent link hierarchy.

## SEO-012 · Product rollout after pilot (P1)
**Description:** 10 engineer-reviewed priority products with real downloadable documents and index metadata.
**Acceptance:** CSV page inventory approved; no false IES/BIM/certification claims; mobile/table QA.

## SEO-013 · Five project case studies with permissions (P1)
**Description:** Publish authorized project results from existing factory portfolio.
**Acceptance:** client/logo/photo permissions, accurate products, case-specific proof, links to relevant product pages.

## SEO-014 · Engineering GEO content (P1)
**Description:** Eight original answer pages with reviewed examples and supporting data.
**Acceptance:** human subject-matter approval; useful answers; no mass templated doorways; citation links.

## SEO-015 · Off-site entity consistency (P1)
**Description:** Align official company profiles and approved directory references.
**Acceptance:** business details match source of truth and publication log records authoritative URL/date.

## SEO-016 · Media & photometric library (P1)
**Description:** Inventory actual owned product images, BIM/Revit and IES files, identify missing items as missing.
**Acceptance:** each link resolves and maps to an actual SKU; alt/image rights verified.

## SEO-017 · Performance & responsive regression (P1)
**Description:** Lighthouse mobile/desktop optimization on approved templates.
**Acceptance:** before/after evidence with unchanged design, no lost features or degraded conversion.

## SEO-018 · AI citation query panel (P2)
**Description:** Fixed, reproducible bilingual prompt panel with evidence logging.
**Acceptance:** screenshots/URLs, cite/no cite and verified referrers distinguished; variance reported.

## SEO-019 · Editorial & distribution process (P2)
**Description:** Monthly engineering FAQ/video approvals and credible sector publication.
**Acceptance:** approved calendar, asset owners and posting evidence; no paid link schemes.

## SEO-020 · 90-day dashboard and review (P1)
**Description:** Reconcile analytics/search and sales funnel, prioritize next quarter on actual impact.
**Acceptance:** baseline vs changes, qualified RFQ trend, unknowns and attribution limitations recorded.

---

# Added 2026-10-21 after live audit (`reports/baseline-2026-10-21.md`) — do these before SEO-005

## SEO-021 · Arabic canonical fix in WPML (P0)
**Description:** `/ar/`, `/ar/our-lighting/`, `/ar/product/led-up-light/` declare `hreflang="ar"` but `rel=canonical` points to the English URL. Find the source (WPML SEO settings, theme or a filter in `porto-child`) and make each translation canonicalize to itself.
**Acceptance:** audit reports zero `canonical_conflicts_with_hreflang` across all configured pages; hreflang pairs still reciprocal; verified on staging first; rollback recorded.

## SEO-022 · WPML-compatible SEO plugin (P0)
**Description:** No SEO plugin is active (no meta descriptions, site title = domain, `og:title` = `front`). Owner chooses Rank Math or Yoast; install on staging, set brand site name (Nassli LED / مصنع نسلي للإنارة), per-language titles and descriptions for the priority pages, multilingual sitemap, and hide generator version tags.
**Acceptance:** owner decision recorded; no duplicate Organization/Product schema with WooCommerce; titles/meta present EN+AR on priority pages; audit shows no `generic_title`/`missing_meta_description` on them.

## SEO-023 · Sitemap cleanup (P0)
**Description:** Remove the 28 `porto_builder` template URLs and the user archive sitemap (exposes a WordPress login name); ensure Arabic URLs are listed.
**Acceptance:** audit shows no `sitemap_lists_theme_templates` / `sitemap_exposes_user_archives`; Arabic URLs present; sitemap resubmitted in Search Console.

## SEO-024 · Product schema truthfulness across 70 products (P0)
**Description:** Product JSON-LD publishes `price: 0.00`, a placeholder SKU (`1234567812-1-1-…`) and a mismatched image. Set real order codes as SKU, drop Offer for quote-only products (or publish real prices only if management approves), fix featured images.
**Acceptance:** audit shows no `schema_offer_price_zero` / `schema_sku_suspicious` on sampled products; Rich Results Test passes on 3 samples; sales engineer confirms SKU list.
