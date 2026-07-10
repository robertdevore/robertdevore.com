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

for value, paths in titles.items():
    if value and len(paths) > 1 and not all("/page/" in p or p.startswith("page/") for p in paths): warnings.append(f"duplicate title: {value} ({len(paths)})")

required = ["index.html", "blog/index.html", "page/2/index.html", "about/index.html", "contact/index.html", "projects/index.html", "category/developer-tools/index.html", "tag/engineering/index.html", "404.html", "feed/index.xml", "sitemap.xml", "robots.txt", "llms.txt"]
for item in required:
    if not (root / item).exists(): errors.append(f"missing required output: {item}")

print(f"Validated {len(html_files)} primary HTML routes")
print(f"Warnings: {len(warnings)}")
for warning in warnings[:20]: print(f"WARN {warning}")
if errors:
    for error in errors[:100]: print(f"ERROR {error}")
    raise SystemExit(1)
print("Site validation passed")
