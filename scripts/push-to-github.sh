#!/usr/bin/env bash
set -euo pipefail
# Historical: repo already exists at bnassli/nassli-search-visibility (public, protected main).
[ -d .git ] || git init -b main
git add .
if ! git diff --cached --quiet; then git commit -m 'chore: initialize Nassli search visibility project'; fi
if ! git remote get-url origin >/dev/null 2>&1; then git remote add origin https://github.com/bnassli/nassli-search-visibility.git; fi
git push -u origin main
echo 'Configure main branch protection / PR rules on GitHub.'
