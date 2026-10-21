#!/usr/bin/env bash
set -euo pipefail
# Optional helper after git push and `gh auth login`.
# This seeds issues without assigning owners; review and modify them in GitHub.
repo='bnassli/nassli-search-visibility'
command -v gh >/dev/null || { echo 'Install GitHub CLI (gh) first'; exit 1; }
# Labels show who owns an issue so Claude and Codex never edit the same files at once.
gh label create 'agent:claude' --repo "$repo" --color 'D97757' --description 'Assigned to Claude' --force
gh label create 'agent:codex' --repo "$repo" --color '10A37F' --description 'Assigned to Codex' --force
gh label create 'needs-owner-approval' --repo "$repo" --color 'B60205' --description 'Blocked until the owner approves' --force
gh label create 'P0' --repo "$repo" --color 'B60205' --force
gh label create 'P1' --repo "$repo" --color 'FBCA04' --force
gh label create 'P2' --repo "$repo" --color '0E8A16' --force
for line in \
  'SEO-001|P0|Set up private GitHub collaboration rules' \
  'SEO-002|P0|Read-only website source and infrastructure inventory' \
  'SEO-003|P0|Capture search/index/performance/RFQ baseline' \
  'SEO-004|P0|Approve official Nassli identity and factual claims' \
  'SEO-005|P0|Homepage metadata, copy, author artifact cleanup' \
  'SEO-006|P0|Canonical, robots, sitemap and indexing defects' \
  'SEO-007|P1|Translate and map bilingual priority pages' \
  'SEO-008|P1|Organization and Product JSON-LD pilot' \
  'SEO-009|P0|High-intent LED UP LIGHT product/RFQ pilot' \
  'SEO-010|P0|RFQ conversion measurement with privacy' \
  'SEO-011|P1|Priority categories and internal links' \
  'SEO-012|P1|Product rollout after pilot' \
  'SEO-013|P1|Five project case studies with permissions' \
  'SEO-014|P1|Engineering GEO content' \
  'SEO-015|P1|Off-site entity consistency' \
  'SEO-016|P1|Media and photometric library' \
  'SEO-017|P1|Performance and responsive regression' \
  'SEO-018|P2|AI citation query panel' \
  'SEO-019|P2|Editorial and distribution process' \
  'SEO-020|P1|90-day dashboard and review' \
  'SEO-021|P0|Arabic canonical fix in WPML' \
  'SEO-022|P0|WPML-compatible SEO plugin' \
  'SEO-023|P0|Sitemap cleanup' \
  'SEO-024|P0|Product schema truthfulness across 70 products'; do
  IFS='|' read -r id priority title <<< "$line"
  if gh issue list --repo "$repo" --state all --limit 200 --json title --jq '.[].title' | grep -Fq "[$id]"; then
    echo "Skipping existing $id"
  else
    body=$(printf 'See tracking/ISSUE-BACKLOG.md section %s for full scope and acceptance criteria.\n\nOwner: TBD (add agent:claude or agent:codex). Production changes require explicit human approval.' "$id")
    gh issue create --repo "$repo" --title "[$id][$priority] $title" --label "$priority" --body "$body"
  fi
done
