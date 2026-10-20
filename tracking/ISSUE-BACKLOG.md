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
