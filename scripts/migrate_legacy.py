#!/usr/bin/env python3
"""Deterministically migrate the previous rendered site into Kujo SSG sources."""
from __future__ import annotations

import argparse, csv, html, json, re, shutil, unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
from bs4 import BeautifulSoup, NavigableString, Tag
import html2text

SITE = "https://robertdevore.com"
LEGACY_PAGES = {"contact-new", "free-ai-tools", "laravel-development", "mvp-app-build", "nextjs-development", "page-speed-optimization", "portfolio", "react-native-development", "security-audit", "wordpress-development"}

@dataclass
class Entry:
    kind: str; route: str; title: str; date: str; description: str; body: str
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    template: str = "signal-a"
    issues: list[str] = field(default_factory=list)

def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "untitled"

def parse_llms(path: Path) -> tuple[list[str], list[str]]:
    posts, pages, section = [], [], ""
    for line in path.read_text(errors="ignore").splitlines():
        if line.startswith("## Posts"): section = "post"
        elif line.startswith("## Pages"): section = "page"
        elif line.startswith("## "): section = ""
        for url in re.findall(r"\((https://robertdevore\.com/[^)]*)\)", line):
            route = urlparse(html.unescape(url)).path.strip("/")
            if route and section == "post": posts.append(route)
            if route and section == "page": pages.append(route)
    return list(dict.fromkeys(posts)), list(dict.fromkeys(pages))

def parse_sitemap(path: Path) -> dict[str, str]:
    soup, out = BeautifulSoup(path.read_text(errors="ignore"), "xml"), {}
    for item in soup.find_all("url"):
        if item.loc and item.lastmod: out[urlparse(item.loc.text).path.strip("/")] = item.lastmod.text[:10]
    return out

def local_path(url: str) -> str | None:
    if not url or url.startswith(("data:", "http://", "https://")): return None
    path = unquote(urlparse(url).path)
    while path.startswith("../"): path = path[3:]
    return path.lstrip("/").replace("//", "/") or None

def rewrite_url(url: str, route: str) -> str:
    if not url or url.startswith(("#", "mailto:", "tel:", "data:")): return url
    absolute, parsed = urljoin(f"{SITE}/{route}/", html.unescape(url)), None
    parsed = urlparse(absolute)
    if parsed.netloc in {"robertdevore.com", "www.robertdevore.com"}:
        return (parsed.path or "/") + (("?" + parsed.query) if parsed.query else "") + (("#" + parsed.fragment) if parsed.fragment else "")
    return absolute

def clean(root: Tag, route: str, legacy: Path) -> tuple[str, list[str]]:
    issues, factory = [], root
    while factory.parent is not None: factory = factory.parent
    for bad in root.select("script,style,noscript"): bad.decompose()
    for node in root.find_all(True):
        for attr in list(node.attrs):
            if attr in {"class", "style", "srcset", "sizes"} or attr.startswith(("x-", "@", ":", "data-")): del node.attrs[attr]
        if node.name == "a" and node.get("href"): node["href"] = rewrite_url(str(node["href"]), route)
        if node.name in {"img", "video", "source"} and node.get("src"):
            original, path = str(node["src"]), local_path(str(node["src"]))
            if path and (legacy / path).exists(): node["src"] = f"/assets/legacy-images/{Path(path).name}"
            else: node["src"] = rewrite_url(original, route)
            if node.name == "img":
                if "alt" not in node.attrs: node["alt"] = ""; issues.append("source image lacked alt text")
                node["loading"], node["decoding"] = "lazy", "async"
        if node.name == "iframe":
            if node.get("src"): node["src"] = rewrite_url(str(node["src"]), route)
            node["title"], node["loading"] = node.get("title", "Embedded media"), "lazy"
    for h1 in root.find_all("h1"): h1.name = "h2"
    for pre in list(root.find_all("pre")):
        code = pre.get_text("", strip=False).strip("\n")
        pre.replace_with(NavigableString(f"\n\n```\n{code}\n```\n\n"))
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_images = False
    converter.ignore_links = False
    return converter.handle(str(root)).strip(), list(dict.fromkeys(issues))

    # The code below documents the richer HTML normalization path to restore if
    # Kujo's Markdown contract gains trusted raw-HTML support.
    used, headings = set(), []
    for heading in root.find_all(["h2", "h3", "h4"]):
        label, base = heading.get_text(" ", strip=True), slug(heading.get_text(" ", strip=True))
        if not label: continue
        ident, index = base, 2
        while ident in used: ident, index = f"{base}-{index}", index + 1
        used.add(ident); heading["id"] = ident
        anchor = factory.new_tag("a", href=f"#{ident}"); anchor["class"] = "heading-anchor"; anchor["aria-label"] = f"Link to {label}"; anchor.string = "#"
        heading.append(NavigableString(" ")); heading.append(anchor); headings.append(heading)
    for table in list(root.find_all("table")):
        wrap = factory.new_tag("div"); wrap["class"] = "sk-table"; table.wrap(wrap)
    for pre in list(root.find_all("pre")):
        if pre.parent and pre.parent.name == "figure": continue
        wrap = factory.new_tag("figure"); wrap["class"] = "sk-code-block"; pre.wrap(wrap)
    if len(headings) >= 3:
        nav = factory.new_tag("nav"); nav["class"] = "article-toc"; nav["aria-labelledby"] = "article-toc-title"
        title = factory.new_tag("h2", id="article-toc-title"); title.string = "On this page"; nav.append(title)
        listing = factory.new_tag("ol")
        for heading in headings:
            item, link = factory.new_tag("li"), factory.new_tag("a", href=f"#{heading['id']}")
            if heading.name == "h3": item["class"] = "article-toc__nested"
            link.string = heading.get_text(" ", strip=True).removesuffix(" #"); item.append(link); listing.append(item)
        nav.append(listing); first = next((x for x in root.children if isinstance(x, Tag)), None)
        first.insert_before(nav) if first else root.append(nav)
    return "\n".join(str(x) for x in root.children).strip(), list(dict.fromkeys(issues))

def taxonomy(title: str, body: str) -> tuple[list[str], list[str]]:
    text, title_l = f"{title} {body[:3000]}".lower(), title.lower()
    if any(x in text for x in ("wordpress", "woocommerce", "gutenberg", "plugin")):
        return ["WordPress Archive"], ["WordPress"] + (["WooCommerce"] if "woocommerce" in text else [])
    if any(x in text for x in ("prompt", "artificial intelligence", "chatgpt")) or any(x in title_l for x in ("ai ", " ai", "content")):
        return ["AI & Content Systems"], ["AI"]
    if any(x in text for x in ("python", "laravel", "flask", "cli", "static site", "code")):
        return ["Developer Tools"], ["Engineering"]
    if any(x in text for x in ("leadership", "focus", "patience", "relentless", "anarchism")):
        return ["Field Notes"], ["Essays"]
    return ["Engineering Archive"], ["Archive"]

def post_entry(path: Path, route: str, date: str, index: int, legacy: Path) -> Entry:
    soup = BeautifulSoup(path.read_text(errors="ignore"), "html.parser"); sections = soup.select("#main-content > section")
    if len(sections) != 2: raise ValueError(f"unexpected post structure: {path}")
    title = html.unescape(sections[0].find("h1").get_text(" ", strip=True)); time = sections[0].find("time")
    if time and time.get("datetime"):
        for fmt in ("%B %d, %Y", "%Y-%m-%d"):
            try: date = datetime.strptime(str(time["datetime"]), fmt).strftime("%Y-%m-%d"); break
            except ValueError: pass
    article = sections[1].find("article") or sections[1]; plain = " ".join(article.get_text(" ", strip=True).split())
    description = (plain[:220].rsplit(" ", 1)[0] + "…") if len(plain) > 220 else plain
    categories, tags = taxonomy(title, plain); body, issues = clean(article, route, legacy)
    return Entry("post", route, title, date or "1970-01-01", description, body, categories, tags, ("signal-a", "signal-b", "signal-c")[index % 3], issues)

def legacy_entry(path: Path, route: str, date: str, legacy: Path) -> Entry:
    soup = BeautifulSoup(path.read_text(errors="ignore"), "html.parser"); main = soup.select_one("#main-content")
    title = html.unescape(main.find("h1").get_text(" ", strip=True)); body, issues = clean(main, route, legacy)
    notice = "> **Archived page:** This page is retained for URL continuity. Availability, service claims, timelines, metrics, and testimonials have not been re-verified.\n\n"
    return Entry("legacy-page", route, title, date or "2025-08-12", f"Archived page retained for URL continuity: {title}.", notice + body, template="legacy", issues=["stale claims require human review"] + issues)

def add_navigation(posts: list[Entry]) -> None:
    ordered = sorted(posts, key=lambda x: (x.date, x.route), reverse=True); groups = defaultdict(list)
    for entry in ordered: groups[entry.categories[0]].append(entry)
    for entry in ordered:
        related = [x for x in groups[entry.categories[0]] if x is not entry][:3]
        if len(related) < 3:
            for candidate in ordered:
                if candidate is not entry and candidate not in related:
                    related.append(candidate)
                if len(related) == 3:
                    break
        related_md = "\n".join(f"- [{x.title}](/%s/)" % x.route for x in related)
        entry.body = f"{entry.body}\n\n## Related Reading\n\n{related_md}"

def write(entry: Entry, path: Path) -> None:
    meta = {"title": entry.title, "description": entry.description, "custom_url": entry.route, "author": "Robert DeVore", "date": entry.date, "canonical": f"{SITE}/{entry.route}/", "template": entry.template, "nav_hide": True}
    if entry.kind == "post": meta |= {"excerpt": entry.description, "categories": entry.categories, "tags": entry.tags}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in meta.items()) + "\n---\n\n" + entry.body + "\n", encoding="utf-8")

def archives(posts: list[Entry], content: Path) -> None:
    for kind, attr in (("category", "categories"), ("tag", "tags")):
        groups = defaultdict(list)
        for entry in posts:
            for term in getattr(entry, attr): groups[term].append(entry)
        for term, entries in groups.items():
            items = "\n".join(f"- {x.date} [{x.title}](/%s/)" % x.route for x in sorted(entries, key=lambda y: y.date, reverse=True))
            archive = Entry(f"{kind}-archive", slug(term), term, max(x.date for x in entries), f"Writing filed under {term}.", f"## Articles\n\n{items}", template="archive")
            write(archive, content / kind / f"{slug(term)}.md")

def copy_images(entries: list[Entry], legacy: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        for media in BeautifulSoup(entry.body, "html.parser").select('[src^="/assets/legacy-images/"]'):
            name = Path(str(media["src"])).name
            if (target / name).exists(): continue
            candidates = list((legacy / "images").glob(name)) + list((legacy / "assets/images").glob(name))
            if candidates: shutil.copy2(candidates[0], target / name)

def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--legacy-root", type=Path, default=Path.cwd()); parser.add_argument("--content-root", type=Path, default=Path("migrated-content")); parser.add_argument("--manifest", type=Path, default=Path("docs/content-migration.csv")); args = parser.parse_args()
    legacy, content = args.legacy_root.resolve(), args.content_root
    posts, pages = parse_llms(legacy / "llms.txt"); dates = parse_sitemap(legacy / "sitemap.xml")
    entries = [post_entry(legacy / route / "index.html", route, dates.get(route, ""), i, legacy) for i, route in enumerate(posts)]
    add_navigation(entries); post_entries = list(entries)
    for route in sorted((set(pages) | LEGACY_PAGES) - {"about", "blog", "contact"}):
        if (legacy / route / "index.html").exists(): entries.append(legacy_entry(legacy / route / "index.html", route, dates.get(route, ""), legacy))
    if content.exists(): shutil.rmtree(content)
    for entry in entries: write(entry, content / ("posts" if entry.kind == "post" else "pages") / f"{entry.route}.md")
    archives(post_entries, content); copy_images(entries, legacy, Path("assets/legacy-images"))
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest.open("w", newline="", encoding="utf-8") as handle:
        out = csv.writer(handle); out.writerow(["source_url", "target_url", "content_file", "content_type", "layout", "frontmatter", "featured_image", "redirect", "known_issue", "verification"])
        for entry in sorted(entries, key=lambda x: x.route):
            directory = "posts" if entry.kind == "post" else "pages"; out.writerow([f"{SITE}/{entry.route}/", f"{SITE}/{entry.route}/", f"content/{directory}/{entry.route}.md", entry.kind, entry.template, "normalized", "decorative signal art", "retained", "; ".join(entry.issues), "pending build"])
    print(f"Migrated {len(post_entries)} posts and {len(entries)-len(post_entries)} legacy pages")

if __name__ == "__main__": main()
