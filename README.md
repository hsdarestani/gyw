# Get Your Wings

Clean static rebuild of the public Get Your Wings website for Cloudflare Pages.

## Cloudflare Pages

Use these settings:

- Framework preset: None
- Build command: leave empty
- Build output directory: .
- Root directory: /

The site is plain HTML, CSS and JavaScript, so no Node build is required.

## Routes

- /
- /circle/
- /voice/
- /secure/
- /well/
- /magazine/
- /about/
- /partners/

## Notes

The rebuild removes the Wix runtime and keeps the frontend intentionally lightweight. Current visual assets are referenced from the existing Get Your Wings CDN so the repository stays small. Those assets can later be downloaded into /assets if you want the deployment to be fully independent of Wix.
