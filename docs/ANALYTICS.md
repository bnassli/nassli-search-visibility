# Measurement and attribution plan

## North-star KPI
**Qualified RFQs originated/assisted by search**, tracked together with quotation value and eventual Won pipeline where lawful and technically feasible.

## Minimum dashboard

| Metric | Source | Cadence | Note |
|---|---|---|---|
| Organic nonbrand clicks & impressions | Google Search Console/Bing | Weekly | Group branded vs nonbrand, Arabic vs English where possible |
| Indexed intended landing pages | Google indexing reports + audit | Weekly | Report trend and reasons for excluded pages |
| Qualified quote requests | Form backend/CRM | Weekly | Validate deduplication, not GA4 alone |
| Phone/WhatsApp intent clicks | GA4 events | Weekly | Click is not a confirmed sale/lead |
| Datasheet downloads | GA4 event | Weekly | Intent proxy; don't count as RFQ |
| Lead response / qualified leads | CRM | Monthly | Avoid storing personal data in repo |
| Quote value and win-rate | CRM | Monthly | Attribution limitations documented |
| Core Web Vitals | GSC/CrUX/Lighthouse | Monthly | Real user vs lab metrics distinguished |
| AI referral traffic | GA4 referrers | Monthly | Incomplete if AI traffic not tagged |
| AI citation panel | Manual + platform reports | Monthly | Directional and variable; no guaranteed lift |

## Proposed event contract (review with web developer)
- `generate_lead` when a **validated successful** RFQ is accepted by backend, once per unique submission; no duplicate on reload.
- `select_content` or site-specific `rfq_start` for opening RFQ form (mark separately from success).
- `file_download` with `file_type`, `asset_category`, product category, no email/mobile/name.
- `contact_click` with `method`: `phone`, `whatsapp`, `email`.
- Optionally `rfq_source` in CRM with server-side attribution after consent and policy review.
- Do **not** send PII into GA4, GitHub Issues or analytics URLs. Avoid creating new cookies without consent/privacy review.

## Baseline data sheet (fill actuals)

| KPI | Baseline | Measurement period | Owner |
|---|---|---|---|
| Nonbrand organic clicks | PENDING | Last 28 days | Marketing |
| Indexed useful pages | PENDING | Current GSC | Web |
| Qualified organic RFQs | PENDING | Last 30 days | Sales |
| Average lead quality | PENDING | Last 30 days | Sales |
| Organic conversion rate | PENDING | Last 30 days | Marketing |
| AI sourced referrals | PENDING | Last 30 days | Analytics |

## Data integration steps
1. Claim GSC domain property (DNS ownership verification) and Bing Webmaster Tools.
2. Export current index/queries/page metrics; redact proprietary query details if shared outside team.
3. Validate GA4 event instrumentation on staging, use debug tools.
4. Test real RFQ test submit → CRM mapping; ensure no PII collected in analytics.
5. Set a monthly evidence-backed dashboard and publish read-only aggregate summaries in the repo.
