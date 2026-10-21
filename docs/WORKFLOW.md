# Work protocol — Basel × Codex × Claude

## Source of truth
The GitHub repo is the only shared project memory. A chat response is not evidence that a file was changed: accept work only when a branch, commit, PR or Issue URL exists. `STATUS.md` gives current state, Git history tracks code, Issues track deliverables.

## Roles

| Party | Primary function | Permissions |
|---|---|---|
| Owner | Priorities, technical claim approval, spending, publish/merge decisions | Owns GitHub, production and approvals |
| Codex | **Reviewer.** Step 1: reviews every Issue first (facts, risks, proposed approach, acceptance criteria). Step 4: confirms Claude's PR | **Comments only — never edits files, pushes branches or opens PRs** |
| Claude | **Second reviewer + sole implementer.** Step 2: reviews Codex's comment and posts the agreed plan. Step 3: makes all file changes on a branch and opens the PR | Only agent that writes to the repo; no production deploy by default |
| Technical sales/engineering | Confirm specs, catalog, certifications and case-study permissions | Explicit written approval for claims |

## Review order for every Issue (owner decision 2026-10-21)

The Issue's label shows whose turn it is. Whoever finishes a step swaps the label to the next one.

| Label | Who | Does what | Output |
|---|---|---|---|
| `step-1:codex-review` | Codex | Reads the Issue, `STATUS.md`, relevant files and the live page; checks facts, risks and missing acceptance criteria; proposes an approach | One Issue comment starting `CODEX REVIEW` |
| `step-2:claude-review` | Claude | Checks Codex's points against sources and code; agrees, corrects or adds; writes the final plan | One Issue comment starting `AGREED PLAN` (lists any disagreement for the owner) |
| `step-3:claude-build` | Claude | Implements the agreed plan on `claude/seo-XXX-...`, runs tests and the audit, opens PR | PR linked to the Issue |
| `step-4:codex-confirm` | Codex | Reviews the PR diff against the agreed plan; reruns tests if it can | PR comment `CODEX CONFIRMED` or `CODEX CHANGES REQUESTED` with reasons |
| — | Owner | Reads both reviews, approves facts/content, merges | Merge |

If Codex requests changes at step 4, Claude fixes on the same branch and the PR goes back to step 4. Disagreements the agents cannot settle with evidence go to the owner with `needs-owner-approval`.

## Standard change lifecycle
1. **Issue**: ID, purpose, affected URLs, risk, expected impact, acceptance checks, owner.
2. **Branch**: `claude/seo-012-homepage`. Only Claude creates branches; Codex works through comments.
3. **Baseline**: capture page and metadata, current index status and conversions if available. Record unknowns.
4. **Implementation**: narrow diff, clear commit messages. Keep URL/visual design stable unless authorized.
5. **Verification**: tests + desktop/mobile + Arabic/English + validated schema + visual screenshots if applicable.
6. **PR**: link Issue and the `AGREED PLAN` comment, include tests, risk, rollback and next-step handoff. Do not self-merge.
6b. **Codex confirmation** (step 4) before the owner reviews.
7. **Approval**: human reviews content, marketing and technical claims. Merge to main.
8. **Staging → Production**: after approval, backup and rollback plan; deploy only with explicit authorization.
9. **Measurement**: observe indexed pages, nonbrand search clicks, qualified RFQs and revenue attribution.

## Collision prevention
- Pull latest `main` at session start. If another branch edits same template, coordinate issue owner.
- `main` is protected by GitHub (owner decision 2026-10-21, repo made public to allow it on the free plan): PR required, `unit-tests` must pass on the latest commit, no direct or force pushes, admins included. The owner merges only after `CODEX CONFIRMED` on the latest PR revision.
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
