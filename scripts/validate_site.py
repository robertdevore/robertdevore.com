#!/usr/bin/env python3
"""Repository-specific release checks for generated RobertDeVore.com output."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

root = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
errors, warnings, titles, descriptions = [], [], {}, {}
html_files = sorted(root.rglob("index.html")) + [root / "404.html"]

def route_exists(path: str) -> bool:
    clean = path.split("?", 1)[0].split("#", 1)[0]
    if clean in {"", "/"}: return (root / "index.html").exists()
    candidate = root / clean.lstrip("/")
    return candidate.is_file() or (candidate / "index.html").exists()

for path in html_files:
    soup = BeautifulSoup(path.read_text(errors="ignore"), "html.parser")
    rel = path.relative_to(root)
    if soup.find(string=re.compile(r"\{\{(?:home_path|relative_path)\}\}")): errors.append(f"{rel}: unresolved layout placeholder")
    if not soup.select_one("#main-content"): errors.append(f"{rel}: missing #main-content")
    h1s = soup.find_all("h1")
    if len(h1s) != 1: errors.append(f"{rel}: expected one h1, found {len(h1s)}")
    title = soup.title.get_text(strip=True) if soup.title else ""
    desc = soup.find("meta", attrs={"name": "description"})
    canonical = soup.find("link", rel="canonical")
    if not title: errors.append(f"{rel}: missing title")
    if not desc or not desc.get("content", "").strip(): errors.append(f"{rel}: missing description")
    if path.name != "404.html" and not canonical: errors.append(f"{rel}: missing canonical")
    titles.setdefault(title, []).append(str(rel))
    if desc: descriptions.setdefault(desc.get("content", ""), []).append(str(rel))
    ids = [x["id"] for x in soup.select("[id]")]
    if len(ids) != len(set(ids)): errors.append(f"{rel}: duplicate id")
    for image in soup.find_all("img"):
        if "alt" not in image.attrs: errors.append(f"{rel}: image without alt")
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try: json.loads(script.string or "")
        except json.JSONDecodeError: errors.append(f"{rel}: invalid JSON-LD")
    for element, attr in (("a", "href"), ("img", "src"), ("script", "src"), ("link", "href"), ("video", "src"), ("source", "src")):
        for node in soup.find_all(element):
            url = node.get(attr)
            if not url or url.startswith(("#", "mailto:", "tel:", "data:", "javascript:")): continue
            parsed = urlparse(url)
            if parsed.scheme in {"http", "https"}: continue
            if url.startswith("/") and not route_exists(url):
                target = url.split("?", 1)[0].split("#", 1)[0]
                if target.startswith(("/wp-content/", "/recommends/")): warnings.append(f"{rel}: retained historical external path {target}")
                else: warnings.append(f"{rel}: missing historical internal target {target}")

    article_content = soup.select_one(".article-content")
    if article_content:
        if any(h.get_text(" ", strip=True).lower() == "continue reading" for h in article_content.find_all(["h2", "h3"])):
            errors.append(f"{rel}: obsolete Continue reading section")
        first_block = article_content.find(recursive=False)
        first_links = first_block.select('a[href^="/category/"], a[href^="/tag/"]') if first_block else []
        if first_block and first_block.name == "p" and first_links and len(first_links) == len(first_block.find_all("a")):
            errors.append(f"{rel}: duplicate taxonomy row at start of article content")
        related = next((h for h in article_content.find_all("h2") if h.get_text(" ", strip=True) == "Related Reading"), None)
        related_links = related.find_next_sibling("ul").find_all("a") if related and related.find_next_sibling("ul") else []
        if len(related_links) != 3: errors.append(f"{rel}: expected three Related Reading links, found {len(related_links)}")

    if soup.select_one(".project-page"):
        if len(soup.select(".project-landing h2")) < 3: errors.append(f"{rel}: project landing page lacks substantive sections")
        if not soup.select_one('.project-landing a[href^="https://github.com/kujolang/"]'):
            errors.append(f"{rel}: project landing page missing Kujo GitHub link")

for value, paths in titles.items():
    if value and len(paths) > 1 and not all("/page/" in p or p.startswith("page/") for p in paths): warnings.append(f"duplicate title: {value} ({len(paths)})")

for path in sorted(root.rglob("*.css")):
    rel = path.relative_to(root)
    for raw_url in re.findall(r"url\(([^)]+)\)", path.read_text(errors="ignore")):
        url = raw_url.strip().strip("\"'")
        if not url or url.startswith(("data:", "http:", "https:", "#")): continue
        target = (path.parent / url.split("?", 1)[0].split("#", 1)[0]).resolve()
        if not target.is_relative_to(root) or not target.exists():
            errors.append(f"{rel}: missing CSS asset {url}")

required = ["index.html", "blog/index.html", "page/2/index.html", "about/index.html", "contact/index.html", "projects/index.html", "category/developer-tools/index.html", "tag/engineering/index.html", "404.html", "feed/index.xml", "sitemap.xml", "robots.txt", "llms.txt"]
for item in required:
    if not (root / item).exists(): errors.append(f"missing required output: {item}")

home = BeautifulSoup((root / "index.html").read_text(errors="ignore"), "html.parser")
transmission = home.select_one("#writing .section-index")
if not transmission or transmission.get_text(" ", strip=True) != "03 / Transmission log": errors.append("homepage transmission label includes pagination or is missing")
footer = home.select_one(".site-footer")
if not footer or "© 1985-2026 Robert DeVore." not in footer.get_text(" ", strip=True): errors.append("footer copyright is incorrect")
for href in ("https://x.com/deviorobert", "https://github.com/robertdevore"):
    if not footer or not footer.select_one(f'a[href="{href}"]'): errors.append(f"footer missing social link {href}")

contact = BeautifulSoup((root / "contact/index.html").read_text(errors="ignore"), "html.parser")
if len(contact.select("form[data-contact-form] label")) != 5: errors.append("contact form fields are incomplete")

llms = (root / "llms.txt").read_text(errors="ignore")
if "## Projects" not in llms or "[Projects index](https://robertdevore.com/projects/)" not in llms:
    errors.append("llms.txt missing Projects collection")
for slug in ("agents-sdk", "dispatch", "kujo", "lens", "sitekit", "ssg"):
    if f"https://robertdevore.com/projects/{slug}/" not in llms: errors.append(f"llms.txt missing project {slug}")

site_css = (root / "assets/css/site.css").read_text(errors="ignore")
for contract in ("-webkit-text-stroke:8px", ".home-page .section-heading", ".site-header{position:sticky", ".article-related-grid", ".about-page .page-content h2", ".contact-page .page-content h2", ".site-footer{border:0"):
    if contract not in site_css: errors.append(f"site CSS missing requested contract {contract}")

print(f"Validated {len(html_files)} primary HTML routes")
print(f"Warnings: {len(warnings)}")
for warning in warnings[:20]: print(f"WARN {warning}")
if errors:
    for error in errors[:100]: print(f"ERROR {error}")
    raise SystemExit(1)
print("Site validation passed")
