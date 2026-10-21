# Instructions for all agents (Codex, Claude) — single source of rules

`CLAUDE.md` only points here. Change rules in this file, never in two places.

Read in order: `README.md` → `STATUS.md` → `docs/WORKFLOW.md` → relevant Issue → source/config/tests. When the owner says "continue", read `STATUS.md` and open Issues/PRs, not only chat context.

## Mission
Improve qualified B2B RFQs for Nassli LED Factory (مصنع نسلي للإنارة) through safe technical SEO, Arabic/English content, digital authority and citation readiness for AI-assisted search. SEO outcomes are probabilistic; never promise ranking or AI mention.

## Known facts (verified 2026-10-21 — see `reports/baseline-2026-10-21.md`)
- Live site: WordPress + WooCommerce + WPML (`/ar/`) + Porto child theme + Elementor Pro. No SEO plugin yet.
- Arabic brand spelling is **نسلي** (owner decision). Never write «ناسلي».
- This repo is NOT the website source. Never claim a live change happened unless the owner confirms it.

## Session startup
1. `git pull --ff-only`; review open PRs, Issues labeled for you, and `STATUS.md`.
2. Pick only an Issue labeled `agent:codex` (Codex) or `agent:claude` (Claude). Unlabeled → ask the owner. Never edit files another open PR is changing.
3. Branch: `codex/seo-XXX-short-name` or `claude/seo-XXX-short-name`. One agent per branch.
4. Run `python -m unittest discover -s tests -v` before and after changes.
5. One focused PR: what changed, why, tests, expected search effect (not guaranteed), rollback. Update `STATUS.md` handoff. Never merge your own PR.

## Non-negotiables
1. Do not modify production infrastructure or website unless a human explicitly authorizes scope, approves staging evidence, and confirms rollback.
2. Do not invent product specifications, certifications, project client approvals, prices, founder dates, warranties, BIM/IES availability, ratings, or business addresses. Mark unknowns `PENDING_VERIFICATION`.
3. Don't create mass AI-generated doorway pages, keyword stuffing, fake backlinks/reviews or fabricate citations.
4. Never commit API keys, credentials, emails from RFQ contacts, analytics raw user identifiers, server backups, or proprietary customer data.
5. Never change, without owner approval: DNS, Search Console verification, robots.txt, redirects, WPML/SEO plugin settings, product spec sheets, customer/project names, certifications, prices, published content. Never silently install plugins.
6. Validate code and run tests, update docs, record evidence. Avoid dependency/hosting migration without explicit approval.
7. Preserve existing site look, functionality, current public URLs, product codes, and admin workflow by default. Prefer `porto-child` or a small versioned plugin over parent-theme edits.
8. Arabic and English are first-class: native copy, validated hreflang, accurate terminology, RTL checks.
9. Structured data must accurately reflect visible content. Do not promise any Google rich result.
10. For facts about AI crawlers, index requirements and platform capabilities, verify with latest official docs before changing production settings.

## Expected per task
- Issue linked; baseline captured; minimal change proposed; implementation; test output; desktop/mobile & AR/EN checks; risk/rollback; PR; update STATUS.
- If site source is not present, write adapter/requirements only; don't pretend live implementation exists.

## Done criteria
Code passes tests + manual checks, human-approved content/specs, no new critical SEO regression (re-run the audit), QA evidenced, rollback plan recorded, measurement event defined.
