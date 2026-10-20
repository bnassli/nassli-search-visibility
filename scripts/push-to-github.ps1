# Run only AFTER creating empty PRIVATE repo bnassli/nassli-search-visibility.
$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.git')) { git init -b main }
git add .
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { git commit -m 'chore: initialize Nassli search visibility project' }
$remote = git remote get-url origin 2>$null
if (-not $remote) { git remote add origin 'https://github.com/bnassli/nassli-search-visibility.git' }
git push -u origin main
Write-Host 'Review GitHub repository settings and branch protection after push.'
