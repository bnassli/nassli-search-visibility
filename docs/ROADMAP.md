# 90-day roadmap — 2026-10-20 baseline

**North star:** qualified B2B requests for quotation (RFQ), technical consultations and project pipeline. Targets are execution goals, not predicted Google ranking or traffic.

## Priority matrix

| ID | Deliverable | Priority | Dependency | Objective acceptance |
|---|---|---|---|---|
| SEO-001 | GitHub private repo + PR controls + owners | P0 | None | Repo accessible to owner and agents; protection & CI verified |
| SEO-002 | Source/stack inventory + staging backup | P0 | 001 | CMS/plugins/theme/server inventory, verified backup recovery test |
| SEO-003 | Baseline: crawl, indexed URLs, GSC/Bing/GA4 | P0 | 001 | 4 sources documented; no extrapolated numbers |
| SEO-004 | Legal brand/identity fact sheet | P0 | 001 | Founder/date, name/address/contact verified and approved |
| SEO-005 | Homepage cleanup EN/AR | P0 | 002,004 | Clear H1/title/meta, editor artifacts removed, no design regressions |
| SEO-006 | Indexation/canonical/sitemaps/robots audit | P0 | 002,003 | Valid discovery and intentional directives; no accidental noindex |
| SEO-007 | Multi-language hreflang + canonical map | P1 | 002,003 | Reciprocal annotations with correct language/region and translated page mapping |
| SEO-008 | Organization/LocalBusiness schema | P1 | 004,005 | Correct validated JSON-LD reflecting visible facts |
| SEO-009 | Product template & RFQ conversion UX | P0 | 002,003 | 1 pilot product with technical data, PDFs and tracked RFQ; approvals |
| SEO-010 | Analytics GA4/Bing/GSC and CRM RFQ attribution | P0 | 003,009 | Reliable events and deduplication; consent/privacy checks |
| SEO-011 | Category landing pages | P1 | 007,009 | 5 priority B2B categories with original useful Arabic/English text |
| SEO-012 | Product expansion | P1 | 009,011 | 10 priority products reviewed; valid specs no missing canonical |
| SEO-013 | Project case studies | P1 | 004 | 5 approved evidence-based case studies; legal permissions |
| SEO-014 | Engineering knowledge hub | P1 | 011 | 8 expert Q&A pages with review sign-off and original diagrams/claims |
| SEO-015 | Local/entity citations | P1 | 004 | Google Business Profile, social and supplier profiles consistent |
| SEO-016 | Media/images/BIM/IES audit | P1 | 009 | Actual downloadable files mapped to products; accurate file labels |
| SEO-017 | Lighthouse & performance | P1 | 002,005 | Mobile and desktop baseline & after metrics; no layout drift |
| SEO-018 | Structured AI citation tracking | P2 | 003,013,014 | Repeatable fixed-prompt/manual citation log, no unverifiable claims |
| SEO-019 | Editorial and review cadence | P2 | 014 | Monthly original updates, clear reviewers, publish log |
| SEO-020 | 30/60/90-day management report | P1 | 010 | RFQ funnel and verified SEO metrics; documented changes |

## Sprint 0 — first 14 days: Foundation & truth
- Create Private GitHub, protect `main`, configure Issues and manual/weekly auditing.
- Import current website source *after* checking license, private data and deployment.
- Inventory actual CMS (possibly WordPress/WooCommerce, **not confirmed**), theme/plugin versions, environment, redirects, htaccess/CDN.
- Baseline URLs, robots and XML sitemaps, page titles, index reports, Core Web Vitals, conversions.
- Approve unified brand facts, fix accidental author/date disclosures in page if verified.
- **Exit**: backups tested, staging reachable, claims approved, prioritized URL list.

## Sprint 1 — days 15–30: High-intent foundation
- Optimize homepage and 5 critical categories, bilingual navigation/metadata.
- Publish one pilot complete technical product page with datasheet and RFQ funnel.
- Fix canonical/hreflang/sitemap issues verified in baseline; add valid business breadcrumbs/schema.
- Instrument quote submission and essential engagement events, no PII in analytics.
- **Exit**: 1 product pilot live after QA + first tracking events captured.

## Sprint 2 — days 31–60: Engineering authority
- Expand to 10 priority products with truthful specs and download links; add links from categories.
- Publish 5 case studies with authorized project references and project-specific evidence.
- Write 8 engineering answers based on engineer-approved examples (DALI/DMX, IP, facade, high bay).
- Audit image alt, filenames, responsive formats, Core Web Vitals and slow templates.
- **Exit**: all copy is real, internally linked, localized, crawlable, measurable.

## Sprint 3 — days 61–90: Distribution, measurement and iterate
- Strengthen GBP, LinkedIn and credible supplier directories, no paid/fake backlinks.
- Distribute approved project video and useful BIM/IES content, only if these assets exist.
- Run citation tests and compare with baseline; test search traffic by page and quality of leads.
- Write 90-day report; prioritize work based on actual RFQ attribution.
- **Exit**: clear owner-run cadence and next-quarter backlog.

## Important business gates
- No mass product changes before the pilot proves the template works.
- No fake price, certification, IES/BIM or client logo assertions.
- No unreviewed translations. No API or CRM private datasets stored in Git.
