#!/usr/bin/env python3
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
from collections import deque
from pathlib import Path\nfrom bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "wix"
MIGRATION = ROOT / "migration"
OUT.mkdir(parents=True, exist_ok=True)
MIGRATION.mkdir(parents=True, exist_ok=True)

BASE = "https://www.get-your-wings.com"
SEEDS = [
    "/",
    "/circle",
    "/voice",
    "/secure",
    "/well",
    "/well-1",
    "/health-tests",
    "/magazine",
    "/aboutus",
    "/blank-4",
]
EXCLUDE_PREFIXES = (
    "/profile/",
    "/account/",
    "/login",
    "/signup",
    "/members-area",
)
UA = "Mozilla/5.0 (compatible; GYWMigrationBot/1.0; +https://www.get-your-wings.com/)"

def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        ctype = r.headers.get("content-type", "")
        data = r.read()
        return data, ctype, r.geturl()

def clean_source(s):
    s = html.unescape(s)
    s = s.replace("\\/","/").replace("\\u002F","/").replace("\\u002f","/")
    s = s.replace("\\u0026","&").replace("\\u003D","=").replace("\\u003d","=")
    return s

def get_links(text, current):
    out = set()
    for href in re.findall(r'href=["\']([^"\']+)["\']', text, re.I):
        href = html.unescape(href)
        url = urllib.parse.urljoin(current, href)
        p = urllib.parse.urlparse(url)
        if p.scheme not in ("http","https") or p.netloc not in ("www.get-your-wings.com","get-your-wings.com"):
            continue
        path = p.path or "/"
        if any(path.startswith(x) for x in EXCLUDE_PREFIXES):
            continue
        if re.search(r'\.(?:jpg|jpeg|png|webp|svg|gif|pdf|zip|xml|txt)$', path, re.I):
            continue
        out.add(BASE + path + (("?" + p.query) if p.query else ""))
    return out

def extract_wix_urls(text):
    text = clean_source(text)
    urls = set()
    for m in re.finditer(r'https://static\.wixstatic\.com/media/[^\s"\'<>]+', text, re.I):
        u = m.group(0).rstrip("),;]")
        urls.add(u)
    return urls

def media_token(url):
    m = re.search(r'https://static\.wixstatic\.com/media/([^/?#]+?\.(?:png|jpe?g|webp|svg|gif|avif))', url, re.I)
    return m.group(1) if m else None

def safe_name(token):
    stem, ext = os.path.splitext(token)
    stem = re.sub(r'[^A-Za-z0-9._-]+', '_', stem)
    return stem[:180] + ext.lower()

queue = deque(BASE + p for p in SEEDS)
seen = set()
pages = []
all_assets = {}
MAX_PAGES = 120

while queue and len(seen) < MAX_PAGES:
    url = queue.popleft()
    if url in seen:
        continue
    seen.add(url)
    try:
        data, ctype, final_url = fetch(url)
        if "text/html" not in ctype and not data.lstrip().startswith(b"<!"):
            continue
        text = data.decode("utf-8", "ignore")
    except Exception as e:
        pages.append({"url": url, "error": str(e)})
        continue

    title = ""
    tm = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    if tm:
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(tm.group(1)))).strip()

    wix_urls = extract_wix_urls(text)
    for u in wix_urls:
        token = media_token(u)
        if token:
            all_assets.setdefault(token, set()).add(u)

    links = get_links(text, final_url)
    for link in sorted(links):
        if link not in seen and len(seen) + len(queue) < MAX_PAGES * 2:
            queue.append(link)

    pages.append({
        "url": final_url,
        "title": title,
        "wix_asset_count": len(wix_urls),
        "internal_link_count": len(links),
    })
    time.sleep(0.05)

manifest = {}
for i, (token, variants) in enumerate(sorted(all_assets.items()), 1):
    filename = safe_name(token)
    target = OUT / filename
    base_url = "https://static.wixstatic.com/media/" + token
    ok = target.exists() and target.stat().st_size > 0
    error = None
    if not ok:
        candidates = [base_url] + sorted(variants, key=len)
        for candidate in candidates:
            try:
                data, ctype, _ = fetch(candidate, timeout=45)
                if len(data) < 32:
                    raise RuntimeError("response too small")
                target.write_bytes(data)
                ok = True
                break
            except Exception as e:
                error = str(e)
    manifest[token] = {
        "local": "/assets/wix/" + filename,
        "bytes": target.stat().st_size if target.exists() else 0,
        "downloaded": bool(ok),
        "source": base_url,
        "variants_seen": len(variants),
        "error": None if ok else error,
    }
    print(f"[{i}/{len(all_assets)}] {'OK' if ok else 'FAIL'} {token}")

# Generate clean local article pages from the public Wix posts.
def article_shell(title, source_url, body_html):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | Get Your Wings</title><meta name="description" content="Get Your Wings Magazine"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/assets/styles.css"></head><body>
<div class="topline">GET YOUR WINGS · THE GLOBAL PLATFORM FOR WOMEN</div>
<header class="site-header"><div class="container nav"><nav class="navlinks"><a href="/">Start</a><a href="/circle/">Circle</a><a href="/voice/">Voice</a><a href="/secure/">Secure</a><a href="/well/">Well</a><a href="/health/">Health</a></nav><a class="brand" href="/">GET YOUR WINGS</a><nav class="navlinks right"><a href="/magazine/">Magazine</a><a href="/about/">About</a><a href="/partners/">Partners</a></nav><button class="menu-btn" data-menu aria-label="Open menu">☰</button></div></header>
<div class="mobile-menu"><button class="close" data-close aria-label="Close menu">×</button><nav><a href="/">Start</a><a href="/circle/">Circle</a><a href="/voice/">Voice</a><a href="/secure/">Secure</a><a href="/well/">Well</a><a href="/health/">Health</a><a href="/magazine/">Magazine</a></nav></div>
<main class="section"><article class="container article-body"><div class="eyebrow">Magazine</div><h1 class="display">{html.escape(title)}</h1>{body_html}<p class="article-source">Migrated from <a href="{html.escape(source_url)}">the original Get Your Wings article</a>.</p></article></main>
<script src="/assets/app.js" defer></script></body></html>"""

for path, source in sorted(page_html.items()):
    if not path.startswith("/post/"):
        continue
    soup = BeautifulSoup(source, "html.parser")
    h1 = soup.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else path.rsplit("/", 1)[-1].replace("-", " ").title()
    main = soup.find("main") or soup.body or soup
    for bad in main.find_all(["script","style","nav","header","footer","form","svg","noscript"]):
        bad.decompose()
    chunks = []
    seen_text = set()
    for el in main.find_all(["h2","h3","p","ul","ol","img"]):
        if el.name == "img":
            src = el.get("src") or el.get("data-src")
            alt = el.get("alt","")
            if src and "static.wixstatic.com/media/" in src:
                chunks.append(f'<img src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy">')
            continue
        text_value = " ".join(el.get_text(" ", strip=True).split())
        if not text_value or len(text_value) < 2 or text_value in seen_text:
            continue
        seen_text.add(text_value)
        if el.name in ("h2","h3"):
            chunks.append(f"<{el.name}>{html.escape(text_value)}</{el.name}>")
        elif el.name in ("ul","ol"):
            items = [" ".join(li.get_text(" ", strip=True).split()) for li in el.find_all("li", recursive=False)]
            items = [x for x in items if x]
            if items:
                chunks.append("<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in items) + "</ul>")
        else:
            chunks.append(f"<p>{html.escape(text_value)}</p>")
    if chunks:
        dest = ROOT / path.lstrip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(article_shell(title, BASE + path, "".join(chunks)), encoding="utf-8")

# Replace all Wix image references already used by the clean frontend with local files.
text_files = list(ROOT.glob("*.html")) + list(ROOT.glob("*/*.html")) + list((ROOT / "assets").glob("*.css"))
for path in text_files:
    try:
        original = path.read_text(encoding="utf-8")
    except Exception:
        continue
    updated = original
    for token, info in manifest.items():
        if not info["downloaded"]:
            continue
        pat = r'https://static\.wixstatic\.com/media/' + re.escape(token) + r'[^\s"\')<>]*'
        updated = re.sub(pat, info["local"], updated)
    if updated != original:
        path.write_text(updated, encoding="utf-8")

(MIGRATION / "asset-manifest.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
)
(MIGRATION / "page-inventory.json").write_text(
    json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8"
)
summary = {
    "pages_crawled": len([p for p in pages if "error" not in p]),
    "page_errors": len([p for p in pages if "error" in p]),
    "unique_wix_assets": len(manifest),
    "assets_downloaded": sum(1 for x in manifest.values() if x["downloaded"]),
    "assets_failed": sum(1 for x in manifest.values() if not x["downloaded"]),
}
(MIGRATION / "summary.json").write_text(
    json.dumps(summary, indent=2), encoding="utf-8"
)
print(json.dumps(summary, indent=2))
