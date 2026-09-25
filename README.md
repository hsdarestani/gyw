# Get Your Wings

Static Cloudflare Pages migration of the public Get Your Wings website.

## Cloudflare Pages settings
- Framework preset: None
- Build command: leave empty
- Build output directory: .
- Root directory: /

## Current migration
- 36 static HTML pages
- 74 local media assets in `assets/wix/`
- Start
- Circle with current public events
- 5 current public event detail routes
- Voice
- Secure
- Well
- Health
- Health Tests with client-side search and category filtering
- Magazine index
- 15 current public Magazine article routes
- About Us
- Partners
- Expert booking overview
- 3 expert service detail routes
- Legal page preserving the current Imprint, Privacy Policy and Affiliate Disclosure visual documents
- Cloudflare redirects, security headers, robots.txt, sitemap and 404 page

## Asset independence
All Wix media currently referenced by the migrated frontend has been downloaded into this repository and the HTML/CSS has been rewritten to use local `/assets/wix/` paths. A code audit returns no remaining `static.wixstatic.com/media` references.

## Dynamic Wix features
The static migration does not reproduce server-side Wix functionality such as member authentication, private member data, personal health dashboards, checkout/payment processing, saved event registrations, newsletter storage or live appointment scheduling. Those require a backend or external provider integration before the Wix application layer can be retired.

## Editorial content
The public Magazine index, routes, titles, metadata, visuals and concise editorial context are migrated. Full long-form article bodies should be imported from an owned Wix CMS export or original editorial source files before the Wix CMS itself is permanently retired.

## Migration tooling
`scripts/import_wix_assets.py` and the GitHub Actions workflow under `.github/workflows/` can localize newly referenced Wix media and refresh the migration inventory.
