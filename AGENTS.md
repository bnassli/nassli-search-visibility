# Instructions for ChatGPT / coding agents

Read in order: `README.md` → `STATUS.md` → `docs/WORKFLOW.md` → relevant Issue → source/config/tests.

## Mission
Improve qualified B2B RFQs for Nassli LED Factory through safe technical SEO, Arabic/English content, digital authority and citation readiness for AI-assisted search. SEO outcomes are probabilistic; never promise ranking or AI mention.

## Non-negotiables
1. Do not modify production infrastructure or website unless a human explicitly authorizes scope, approves staging evidence, and confirms rollback.
2. Do not invent product specifications, certifications, project client approvals, prices, founder dates, warranties, BIM/IES availability, ratings, or business addresses. Mark unknowns `PENDING_VERIFICATION`.
3. Don't create mass AI-generated doorway pages, keyword stuffing, fake backlinks/reviews or fabricate citations.
4. Never commit API keys, credentials, emails from RFQ contacts, analytics raw user identifiers, server backups, or proprietary customer data.
5. Work through issue branch + PR, no overlapping edits to shared files without pulling latest main. Respect `STATUS.md` handoff.
6. Validate code and run tests, update docs, record evidence. Avoid dependency/hosting migration without explicit approval.
7. Preserve existing site look, functionality, current public URLs, product codes, and admin workflow by default.
8. Arabic and English are first-class: native copy, validated hreflang, accurate terminology, RTL checks.
9. Structured data must accurately reflect visible content. Do not promise any Google rich result.
10. For facts about AI crawlers, index requirements and platform capabilities, verify with latest official docs before changing production settings.

## Expected per task
- Issue linked; baseline captured; minimal change proposed; implementation; test output; desktop/mobile & AR/EN checks; risk/rollback; PR; update STATUS.
- If current site source is not present, write adapter/requirements only; don't pretend live implementation exists.

## Done criteria
Code passes tests + manual checks, human-approved content/specs, no new critical SEO regression, QA evidenced, rollback plan recorded, measurement event defined.
