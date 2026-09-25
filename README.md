# Get Your Wings

Static Cloudflare Pages migration of the public Get Your Wings website.

## Cloudflare Pages settings
- Framework preset: None
- Build command: leave empty
- Build output directory: .
- Root directory: /

## Migrated public areas
- Start
- Circle and public event discovery
- Voice
- Secure
- Well
- Health
- Health Tests with client side search and category filtering
- Magazine index
- 15 current public Magazine article routes
- About
- Partners
- Expert booking/service information
- Legal placeholder route
- Cloudflare redirects, security headers, robots.txt, sitemap and 404 page

## Dynamic Wix features
The static migration does not reproduce Wix member authentication, health dashboards, checkout, member registrations, newsletter storage, or appointment scheduling. Those require a backend or external provider integration before Wix can be fully retired.

## Assets
The frontend itself does not use the Wix runtime. Current migrated visuals are still loaded from static.wixstatic.com because the connected tools cannot export those binary Wix media files directly. Copying the owned originals into /assets/media later will make the deployment completely independent of Wix.

## Editorial content
Magazine titles, metadata, visuals and concise editorial summaries are migrated. Full long form article bodies should be imported from an owned Wix CMS export or the original editorial source files before Wix is permanently disconnected.
