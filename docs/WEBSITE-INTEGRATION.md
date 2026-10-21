# Integrating actual Nassli website source

## What this repo does NOT contain
No original theme/site export, assets, WordPress DB, CMS plugin list or server credentials. It is not safe to claim a site change is complete until actual source is inspected and deployed on staging.

## Confirmed from public site (2026-10-21)
WordPress 7.0.7, WooCommerce 11.2, WPML 4.6.11 (`/ar/`), Porto + `porto-child`, Elementor Pro, Slider Revolution, YITH Request a Quote Premium, Contact Form 7, Fluent Forms, Chaty. **No SEO plugin.** Server header `hcdn` (likely Hostinger — confirm). Changes should go through `porto-child` or a small versioned plugin, never the parent theme.

## Required read-only intake
1. Repository URL or sanitized site export of current deployed source (not database dumps with user/customer data).
2. CMS/framework version and theme/child theme info; staging URL; plugin list and versions if WordPress.
3. SEO plugin, multilingual plugin, caching/CDN, forms (RFQ), WooCommerce and schema plugin if installed.
4. Production deployment workflow and restore checklist; backup owner.
5. Search Console/Bing/GA4 access or safe exports, business verified facts.

## Recommended structure after intake
- Keep marketing operations/content/docs in this repo.
- Website source goes in a **separate private** `nassli-website` repo (if licensing/ownership allow). **Never** add it to this repo — this repo is public.
- Set up CI and staging from exact source before changing templates.
- In the private website repo, import only code/assets you are permitted to store, never database passwords, customer submissions or admin exports.
- Cross-reference issues or link PRs from this repo to website repo.

## Deployment gate
**Never deploy to production by default.** Create staging snapshot, test responsive desktop+mobile AR/EN, measure, get approval. Production cutover needs permission, backup verification and rollback path.
