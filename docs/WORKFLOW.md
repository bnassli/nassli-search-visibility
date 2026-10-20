# Work protocol — Basel × ChatGPT × Claude

## Source of truth
The GitHub repo is the only shared project memory. A chat response is not evidence that a file was changed: accept work only when a branch, commit, PR or Issue URL exists. `STATUS.md` gives current state, Git history tracks code, Issues track deliverables.

## Roles

| Party | Primary function | Permissions |
|---|---|---|
| Owner | Priorities, technical claim approval, spending, publish/merge decisions | Owns GitHub, production and approvals |
| ChatGPT | Audit, roadmap, content briefs, acceptance criteria, code changes via branch, PR review | No production deploy by default |
| Claude | Site code implementation, testing, integrations, performance and technical cleanup via branch | No production deploy by default |
| Technical sales/engineering | Confirm specs, catalog, certifications and case-study permissions | Explicit written approval for claims |

## Standard change lifecycle
1. **Issue**: ID, purpose, affected URLs, risk, expected impact, acceptance checks, owner.
2. **Branch**: `chatgpt/seo-012-homepage` or `claude/seo-012-homepage`. One person/agent per branch.
3. **Baseline**: capture page and metadata, current index status and conversions if available. Record unknowns.
4. **Implementation**: narrow diff, clear commit messages. Keep URL/visual design stable unless authorized.
5. **Verification**: tests + desktop/mobile + Arabic/English + validated schema + visual screenshots if applicable.
6. **PR**: link Issue, include tests, risk, rollback and next-step handoff. Do not self-merge.
7. **Approval**: human reviews content, marketing and technical claims. Merge to main.
8. **Staging → Production**: after approval, backup and rollback plan; deploy only with explicit authorization.
9. **Measurement**: observe indexed pages, nonbrand search clicks, qualified RFQs and revenue attribution.

## Collision prevention
- Pull latest `main` at session start. If another branch edits same template, coordinate issue owner.
- No force-push to `main`; use branch protection requiring at least 1 review and passing Quality gate.
- If a task is incomplete, annotate `STATUS.md` and PR draft with exact steps remaining.
- Use no shared mutable server shell or WordPress admin session without access coordination.
- Keep changes to SEO operations separate from unrelated CRM or projects.

## Definition of Ready
- Target page exists, goal and customer intent defined; content owner can approve; staging available if deployment needed.
- Rollback and analytics event known; dependency Issue resolved.

## Definition of Done
- PR linked, tests/QA passed, translation reviewed, no private data, verified claims, measured or scheduled measurement, approved.

## Handoff template
```
Date / Agent / Issue / PR / Branch:
What changed (exact files):
Tests passed (exact command/results):
Live site changed? (default NO):
Risks / unknown facts:
Next action and who owns it:
```
