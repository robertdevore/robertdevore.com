#!/usr/bin/env python3
"""Create reproducible local and production SEO audit datasets for this site."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError


SITE_ORIGIN = "https://robertdevore.com"
USER_AGENT = "RobertDeVore-SEOBaseline/1.0 (+https://robertdevore.com/)"
CSV_FIELDS: dict[str, list[str]] = {
    "metadata-audit.csv": [
        "phase", "url", "source_file", "page_type", "title", "title_length",
        "meta_description", "description_length", "canonical", "robots_directives",
        "lang", "author", "og_title", "og_description", "og_url", "og_type",
        "og_image", "twitter_card", "twitter_title", "twitter_description",
        "twitter_image", "duplicate_title", "duplicate_description", "issues",
    ],
    "content-audit.csv": [
        "phase", "url", "source_file", "page_type", "primary_purpose", "search_intent",
        "target_audience", "central_entity", "primary_query_theme", "supporting_topics",
        "h1", "heading_structure", "word_count", "published_date", "modified_date",
        "first_hand_signals", "content_gap", "competing_internal_url", "recommended_action",
    ],
    "keyword-map.csv": [
        "phase", "url", "primary_topic", "primary_entity", "search_intent",
        "primary_query_theme", "secondary_queries", "related_entities", "relevant_questions",
        "competing_internal_url", "content_gap", "recommended_action",
    ],
    "internal-links.csv": [
        "phase", "source_url", "destination_url", "anchor_text", "link_context",
        "destination_status", "source_depth", "destination_depth",
    ],
    "external-links.csv": [
        "phase", "source_url", "destination_url", "anchor_text", "link_context",
        "http_status", "final_url", "verification", "nofollow", "sponsored", "ugc",
    ],
    "broken-links.csv": [
        "phase", "source_url", "destination_url", "link_type", "anchor_text",
        "http_status", "evidence", "recommended_action",
    ],
    "schema-audit.csv": [
        "phase", "url", "schema_types", "json_ld_blocks", "valid_json", "visible_match",
        "google_rich_result_eligible", "issues", "recommended_action",
    ],
    "indexability.csv": [
        "phase", "url", "local_status", "production_status", "indexable", "robots_directives",
        "canonical", "canonical_target_status", "sitemap_included", "sitemap_lastmod",
        "duplicate_title", "duplicate_description", "reason",
    ],
    "crawlability.csv": [
        "phase", "url", "page_depth", "internal_inbound_links", "internal_outbound_links",
        "external_outbound_links", "orphan", "pages_over_three_clicks", "broken_internal_links",
        "redirect_chain", "crawlable_html_links", "issues",
    ],
    "image-audit.csv": [
        "phase", "page_url", "image_url", "alt_text", "alt_present", "decorative",
        "width", "height", "loading", "format", "local_exists", "file_bytes", "issues",
    ],
    "redirects.csv": [
        "phase", "source_url", "http_status", "target_url", "chain_length", "canonical_target",
        "issues",
    ],
    "performance.csv": [
        "phase", "url", "html_bytes", "css_bytes", "js_bytes", "image_bytes",
        "font_bytes", "estimated_page_bytes", "local_request_count", "lcp_ms", "cls", "inp_ms",
        "ttfb_ms", "source", "notes",
    ],
}


@dataclass
class Link:
    url: str
    anchor: str
    context: str
    rel: set[str] = field(default_factory=set)


@dataclass
class Page:
    url: str
    output_file: Path
    source_file: str
    page_type: str
    soup: BeautifulSoup
    title: str
    description: str
    canonical: str
    robots: str
    lang: str
    author: str
    h1: list[str]
    headings: list[str]
    word_count: int
    published: str
    modified: str
    breadcrumbs: bool
    schemas: list[str]
    schema_valid: bool
    internal_links: list[Link]
    external_links: list[Link]
    images: list[dict[str, Any]]
    metadata: dict[str, str]
    sitemap_lastmod: str
    depth: int | None = None


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if not Path(path).suffix and not path.endswith("/"):
        path += "/"
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, ""))


def route_to_file(root: Path, url: str) -> Path:
    path = urllib.parse.urlsplit(url).path
    if path == "/":
        return root / "index.html"
    direct = root / path.lstrip("/")
    if direct.is_file():
        return direct
    return direct / "index.html"


def local_destination_exists(root: Path, url: str) -> bool:
    path = urllib.parse.urlsplit(url).path
    candidate = root / path.lstrip("/")
    return candidate.is_file() or (candidate / "index.html").is_file()


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(errors="ignore")
    if not text.startswith("---\n"):
        return {}
    _, raw, _ = text.split("---", 2)
    result: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line[:1].isspace():
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"\'')
    return result


def source_map(repo: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for path in sorted((repo / "content").rglob("*.md")):
        meta = read_frontmatter(path)
        slug = meta.get("custom_url") or path.stem
        rel = path.relative_to(repo).as_posix()
        parent = path.parent.name
        if parent == "posts":
            route = f"/{slug}/"
        elif parent == "pages":
            route = f"/{slug}/"
        else:
            route = f"/{parent}/{slug}/"
        mapping[route] = rel
    mapping.update({
        "/": "templates/page-home.html",
        "/blog/": "templates/page-blog.html",
        "/projects/": "templates/page-projects.html",
    })
    return mapping


def page_type_for(url: str, source: str) -> str:
    path = urllib.parse.urlsplit(url).path
    if path == "/":
        return "homepage"
    if path.startswith("/page/") or path.startswith("/blog/page/"):
        return "pagination"
    if path == "/blog/":
        return "blog-index"
    if path == "/projects/":
        return "project-index"
    if path.startswith("/projects/"):
        return "project"
    if path.startswith("/category/"):
        return "category-archive"
    if path.startswith("/tag/"):
        return "tag-archive"
    if source.startswith("content/pages/"):
        return "page"
    return "article"


def meta_content(soup: BeautifulSoup, selector: str) -> str:
    node = soup.select_one(selector)
    return clean_text(str(node.get("content", ""))) if node else ""


def link_context(node: Any) -> str:
    parent = node.find_parent(["nav", "header", "footer", "aside", "article", "section", "main"])
    if not parent:
        return "body"
    if parent.name == "nav":
        return "navigation"
    classes = " ".join(parent.get("class", []))
    if "related" in classes:
        return "related-content"
    return parent.name


def extract_schema_types(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        kind = value.get("@type")
        if isinstance(kind, list):
            found.extend(str(item) for item in kind)
        elif kind:
            found.append(str(kind))
        for child in value.values():
            found.extend(extract_schema_types(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(extract_schema_types(child))
    return found


def resolve_href(page_url: str, href: str) -> str:
    return normalize_url(urllib.parse.urljoin(page_url, href))


def local_asset(root: Path, page_file: Path, raw_url: str) -> Path | None:
    if not raw_url or raw_url.startswith(("data:", "http://", "https://", "//")):
        return None
    clean = raw_url.split("?", 1)[0].split("#", 1)[0]
    if clean.startswith("/"):
        return root / clean.lstrip("/")
    return (page_file.parent / clean).resolve()


def parse_pages(repo: Path, output: Path) -> tuple[list[Page], dict[str, str]]:
    sitemap_path = output / "sitemap.xml"
    sitemap = ET.parse(sitemap_path).getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_dates: dict[str, str] = {}
    for node in sitemap.findall("sm:url", ns):
        loc_node = node.find("sm:loc", ns)
        if loc_node is None or not loc_node.text:
            continue
        loc = normalize_url(loc_node.text.strip())
        lastmod = node.find("sm:lastmod", ns)
        sitemap_dates[loc] = lastmod.text.strip() if lastmod is not None and lastmod.text else ""
    sources = source_map(repo)
    pages: list[Page] = []
    for url in sorted(sitemap_dates):
        path = route_to_file(output, url)
        if not path.exists():
            continue
        soup = BeautifulSoup(path.read_text(errors="ignore"), "html.parser")
        title = clean_text(soup.title.get_text(" ", strip=True)) if soup.title else ""
        description = meta_content(soup, 'meta[name="description"]')
        canonical_node = soup.select_one('link[rel="canonical"]')
        canonical = normalize_url(urllib.parse.urljoin(url, canonical_node.get("href", ""))) if canonical_node else ""
        robots = meta_content(soup, 'meta[name="robots"]') or "index, follow (default)"
        lang = str(soup.html.get("lang", "")) if soup.html else ""
        author = meta_content(soup, 'meta[name="author"]')
        h1 = [clean_text(node.get_text(" ", strip=True)) for node in soup.find_all("h1")]
        headings = [f"{node.name.upper()}: {clean_text(node.get_text(' ', strip=True))}" for node in soup.find_all(re.compile(r"^h[1-6]$"))]
        main = soup.find("main") or soup.body or soup
        word_count = len(re.findall(r"\b[\w’'-]+\b", main.get_text(" ", strip=True)))
        published = meta_content(soup, 'meta[property="article:published_time"]')
        modified = meta_content(soup, 'meta[property="article:modified_time"]')
        schemas: list[str] = []
        schema_valid = True
        schema_blocks = soup.find_all("script", attrs={"type": "application/ld+json"})
        for block in schema_blocks:
            try:
                schemas.extend(extract_schema_types(json.loads(block.string or "")))
            except json.JSONDecodeError:
                schema_valid = False
        internal: list[Link] = []
        external: list[Link] = []
        for node in soup.find_all("a", href=True):
            href = str(node.get("href", "")).strip()
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            absolute = resolve_href(url, href)
            link = Link(absolute, clean_text(node.get_text(" ", strip=True)) or "[non-text link]", link_context(node), set(node.get("rel", [])))
            if urllib.parse.urlsplit(absolute).netloc in {"robertdevore.com", "www.robertdevore.com"}:
                internal.append(link)
            else:
                external.append(link)
        images: list[dict[str, Any]] = []
        for image in soup.find_all("img"):
            src = str(image.get("src", ""))
            asset = local_asset(output, path, src)
            exists = bool(asset and asset.is_file() and asset.stat().st_size > 0) if asset else True
            size = asset.stat().st_size if asset and asset.exists() else 0
            alt_present = image.has_attr("alt")
            alt = str(image.get("alt", ""))
            suffix = Path(urllib.parse.urlsplit(src).path).suffix.lstrip(".").lower()
            issues = []
            if not alt_present:
                issues.append("missing alt attribute")
            if not image.get("width") or not image.get("height"):
                issues.append("missing intrinsic dimensions")
            if not exists:
                issues.append("missing local image")
            elif asset and asset.is_file():
                try:
                    with Image.open(asset) as source:
                        source.verify()
                except (OSError, ValueError, UnidentifiedImageError):
                    exists = False
                    issues.append("unreadable local image")
            images.append({
                "image_url": resolve_href(url, src) if src else "",
                "alt_text": alt,
                "alt_present": alt_present,
                "decorative": alt_present and alt == "",
                "width": image.get("width", ""),
                "height": image.get("height", ""),
                "loading": image.get("loading", "default"),
                "format": suffix,
                "local_exists": exists,
                "file_bytes": size,
                "issues": "; ".join(issues),
            })
        path_key = urllib.parse.urlsplit(url).path
        source = sources.get(path_key, "generated listing/archive")
        metadata = {
            "og_title": meta_content(soup, 'meta[property="og:title"]'),
            "og_description": meta_content(soup, 'meta[property="og:description"]'),
            "og_url": meta_content(soup, 'meta[property="og:url"]'),
            "og_type": meta_content(soup, 'meta[property="og:type"]'),
            "og_image": meta_content(soup, 'meta[property="og:image"]'),
            "twitter_card": meta_content(soup, 'meta[name="twitter:card"]'),
            "twitter_title": meta_content(soup, 'meta[name="twitter:title"]'),
            "twitter_description": meta_content(soup, 'meta[name="twitter:description"]'),
            "twitter_image": meta_content(soup, 'meta[name="twitter:image"]'),
            "keywords": meta_content(soup, 'meta[name="keywords"]'),
            "json_ld_blocks": str(len(schema_blocks)),
        }
        pages.append(Page(
            url=url, output_file=path, source_file=source, page_type=page_type_for(url, source),
            soup=soup, title=title, description=description, canonical=canonical, robots=robots,
            lang=lang, author=author, h1=h1, headings=headings, word_count=word_count,
            published=published, modified=modified, breadcrumbs=bool(soup.select_one('[aria-label="Breadcrumbs"]')),
            schemas=sorted(set(schemas)), schema_valid=schema_valid, internal_links=internal,
            external_links=external, images=images, metadata=metadata, sitemap_lastmod=sitemap_dates[url],
        ))
    return pages, sitemap_dates


def compute_depths(pages: list[Page]) -> None:
    known = {page.url for page in pages}
    graph: dict[str, set[str]] = defaultdict(set)
    for page in pages:
        for link in page.internal_links:
            target = normalize_url(link.url)
            if target in known:
                graph[page.url].add(target)
    root = normalize_url(f"{SITE_ORIGIN}/")
    depth = {root: 0}
    queue = deque([root])
    while queue:
        current = queue.popleft()
        for target in sorted(graph[current]):
            if target not in depth:
                depth[target] = depth[current] + 1
                queue.append(target)
    for page in pages:
        page.depth = depth.get(page.url)


def http_probe(url: str, timeout: int = 15) -> dict[str, Any]:
    started = time.perf_counter()
    context = ssl.create_default_context()
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"}
    request = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            return {"status": response.status, "final_url": response.geturl(), "ttfb_ms": round((time.perf_counter() - started) * 1000, 1), "error": ""}
    except urllib.error.HTTPError as exc:
        if exc.code not in {403, 405, 429}:
            return {"status": exc.code, "final_url": exc.geturl(), "ttfb_ms": round((time.perf_counter() - started) * 1000, 1), "error": str(exc)}
    except Exception:
        pass
    request = urllib.request.Request(url, headers={**headers, "Range": "bytes=0-4096"}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            response.read(4096)
            return {"status": response.status, "final_url": response.geturl(), "ttfb_ms": round((time.perf_counter() - started) * 1000, 1), "error": ""}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "final_url": exc.geturl(), "ttfb_ms": round((time.perf_counter() - started) * 1000, 1), "error": str(exc)}
    except Exception as exc:
        return {"status": 0, "final_url": "", "ttfb_ms": round((time.perf_counter() - started) * 1000, 1), "error": f"{type(exc).__name__}: {exc}"}


def probe_many(urls: Iterable[str], workers: int = 8) -> dict[str, dict[str, Any]]:
    unique = sorted(set(urls))
    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(http_probe, url): url for url in unique}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    return results


def topic_for(page: Page) -> str:
    value = page.h1[0] if page.h1 else page.title.replace(" | Robert DeVore", "")
    return clean_text(value)


def intent_for(page: Page) -> str:
    if page.page_type in {"homepage", "project-index"}:
        return "navigational / commercial investigation"
    if page.page_type == "project":
        return "commercial investigation / adoption"
    if page.page_type in {"category-archive", "tag-archive", "blog-index", "pagination"}:
        return "navigational / topic discovery"
    if re.search(r"\b(how|guide|tutorial|build|customize|block|improve|use)\b", page.title, re.I):
        return "informational / problem-solving"
    if re.search(r"\b(introducing|release|launched|v\d|plugin|tool)\b", page.title, re.I):
        return "commercial investigation / product discovery"
    return "informational"


def query_theme(page: Page) -> str:
    topic = topic_for(page)
    topic = re.sub(r"\s*[|–—:-]\s*Robert DeVore$", "", topic, flags=re.I)
    return topic.lower()


def citable_signal(page: Page) -> str:
    text = page.soup.get_text(" ", strip=True).lower()
    signals = []
    if page.word_count >= 900:
        signals.append("substantive depth")
    if page.soup.find("code") or page.soup.find("pre"):
        signals.append("code/example")
    if any(term in text for term in ("i built", "i use", "i learned", "my ", "we built")):
        signals.append("first-hand narrative")
    if page.external_links:
        signals.append("outbound sources")
    return "; ".join(signals) or "not clearly demonstrated"


def asset_totals(page: Page, output: Path) -> dict[str, int]:
    totals = Counter({"css": 0, "js": 0, "image": 0, "font": 0, "requests": 0})
    seen: set[Path] = set()
    candidates: list[tuple[str, str]] = []
    for node, attr, kind in (("link", "href", "css"), ("script", "src", "js"), ("img", "src", "image"), ("source", "srcset", "image")):
        for tag in page.soup.find_all(node):
            raw = str(tag.get(attr, "")).split(",", 1)[0].split(" ", 1)[0]
            candidates.append((raw, kind))
    css_files: list[Path] = []
    for raw, kind in candidates:
        asset = local_asset(output, page.output_file, raw)
        if not asset or not asset.exists() or asset in seen:
            continue
        seen.add(asset)
        totals[kind] += asset.stat().st_size
        totals["requests"] += 1
        if kind == "css":
            css_files.append(asset)
    for css_file in css_files:
        text = css_file.read_text(errors="ignore")
        for raw in re.findall(r"url\(([^)]+)\)", text):
            value = raw.strip().strip('"\'').split("?", 1)[0]
            asset = (css_file.parent / value).resolve()
            if asset.exists() and asset not in seen:
                seen.add(asset)
                kind = "font" if asset.suffix.lower() in {".woff", ".woff2", ".ttf", ".otf"} else "image"
                totals[kind] += asset.stat().st_size
                totals["requests"] += 1
    return dict(totals)


def csv_write(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def create_datasets(repo: Path, output: Path, audit: Path, phase: str, production: bool, external: bool) -> dict[str, Any]:
    pages, sitemap = parse_pages(repo, output)
    compute_depths(pages)
    known = {page.url for page in pages}
    by_url = {page.url: page for page in pages}
    inbound: Counter[str] = Counter()
    for page in pages:
        for link in page.internal_links:
            target = normalize_url(link.url)
            if target in known:
                inbound[target] += 1
    title_counts = Counter(page.title for page in pages if page.title)
    description_counts = Counter(page.description for page in pages if page.description)

    production_results = probe_many((page.url for page in pages)) if production else {}
    external_urls = [link.url for page in pages for link in page.external_links]
    external_results = probe_many(external_urls, workers=6) if external else {}

    rows: dict[str, list[dict[str, Any]]] = {name: [] for name in CSV_FIELDS}
    full_rows: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    for page in pages:
        duplicate_title = title_counts[page.title] > 1
        duplicate_description = description_counts[page.description] > 1
        production_status = production_results.get(page.url, {}).get("status", "NOT AVAILABLE — DATA ACCESS REQUIRED")
        canonical_status = 200 if page.canonical in known else production_results.get(page.canonical, {}).get("status", "not checked")
        missing_internal = [
            link for link in page.internal_links
            if normalize_url(link.url) not in known
            and not local_destination_exists(output, link.url)
            and not urllib.parse.urlsplit(link.url).path.startswith(("/wp-content/", "/recommends/"))
        ]
        indexable = "noindex" not in page.robots.lower() and bool(page.canonical)
        orphan = page.url != f"{SITE_ORIGIN}/" and inbound[page.url] == 0
        metadata_issues = []
        if not page.title:
            metadata_issues.append("missing title")
        if not page.description:
            metadata_issues.append("missing description")
        if not page.canonical:
            metadata_issues.append("missing canonical")
        if len(page.h1) != 1:
            metadata_issues.append(f"H1 count {len(page.h1)}")
        if duplicate_title:
            metadata_issues.append("duplicate title")
        if duplicate_description:
            metadata_issues.append("duplicate description")
        if page.metadata["keywords"]:
            metadata_issues.append("legacy meta keywords present")
        if page.metadata["og_url"] and normalize_url(page.metadata["og_url"]) != page.canonical:
            metadata_issues.append("Open Graph URL differs from canonical")
        if page.metadata["twitter_card"] == "summary_large_image" and not page.metadata["twitter_image"]:
            metadata_issues.append("large Twitter card has no image")
        rows["metadata-audit.csv"].append({
            "phase": phase, "url": page.url, "source_file": page.source_file, "page_type": page.page_type,
            "title": page.title, "title_length": len(page.title), "meta_description": page.description,
            "description_length": len(page.description), "canonical": page.canonical,
            "robots_directives": page.robots, "lang": page.lang, "author": page.author,
            **page.metadata, "duplicate_title": duplicate_title, "duplicate_description": duplicate_description,
            "issues": "; ".join(metadata_issues),
        })

        topic = topic_for(page)
        intent = intent_for(page)
        gap = []
        action = "retain; monitor search and citation performance"
        if page.page_type in {"article", "project", "page"} and page.word_count < 300:
            gap.append("thin for a substantive destination")
            action = "editorial review: clarify purpose and add only evidence-backed useful detail"
        if page.page_type == "project" and not page.published:
            gap.append("project freshness/version not machine-readable")
        if not page.modified and page.page_type in {"article", "project"}:
            gap.append("no verified modified date")
        if not page.breadcrumbs and page.page_type not in {"homepage", "pagination"}:
            gap.append("no visible breadcrumb")
        supporting = [clean_text(node.get_text(" ", strip=True)) for node in page.soup.find_all(["h2", "h3"])[:8]]
        rows["content-audit.csv"].append({
            "phase": phase, "url": page.url, "source_file": page.source_file, "page_type": page.page_type,
            "primary_purpose": topic, "search_intent": intent,
            "target_audience": "developers, technical leaders, WordPress/WooCommerce users, and project evaluators",
            "central_entity": topic, "primary_query_theme": query_theme(page),
            "supporting_topics": " | ".join(supporting), "h1": " | ".join(page.h1),
            "heading_structure": " | ".join(page.headings), "word_count": page.word_count,
            "published_date": page.published, "modified_date": page.modified,
            "first_hand_signals": citable_signal(page), "content_gap": "; ".join(gap),
            "competing_internal_url": "", "recommended_action": action,
        })
        rows["keyword-map.csv"].append({
            "phase": phase, "url": page.url, "primary_topic": topic, "primary_entity": topic,
            "search_intent": intent, "primary_query_theme": query_theme(page),
            "secondary_queries": "; ".join(supporting[:4]), "related_entities": "; ".join(supporting[4:8]),
            "relevant_questions": f"What is {topic}?; How does {topic} work?; Who is {topic} for?",
            "competing_internal_url": "", "content_gap": "; ".join(gap), "recommended_action": action,
        })

        for link in page.internal_links:
            target = normalize_url(link.url)
            destination_status = 200 if target in known or local_destination_exists(output, link.url) else "missing from build"
            rows["internal-links.csv"].append({
                "phase": phase, "source_url": page.url, "destination_url": target,
                "anchor_text": link.anchor, "link_context": link.context,
                "destination_status": destination_status, "source_depth": page.depth if page.depth is not None else "orphan",
                "destination_depth": by_url[target].depth if target in by_url and by_url[target].depth is not None else "unknown",
            })
            if target not in known and not local_destination_exists(output, link.url) and not urllib.parse.urlsplit(target).path.startswith(("/wp-content/", "/recommends/")):
                rows["broken-links.csv"].append({
                    "phase": phase, "source_url": page.url, "destination_url": target, "link_type": "internal",
                    "anchor_text": link.anchor, "http_status": "missing from build",
                    "evidence": "destination absent from canonical generated routes", "recommended_action": "update, restore, or intentionally redirect the destination",
                })
        for link in page.external_links:
            probe = external_results.get(link.url, {})
            status = probe.get("status", "not checked")
            verification = "verified" if status and status not in {403, 429} else ("blocked/indeterminate" if status in {403, 429} else "not checked")
            rows["external-links.csv"].append({
                "phase": phase, "source_url": page.url, "destination_url": link.url,
                "anchor_text": link.anchor, "link_context": link.context, "http_status": status,
                "final_url": probe.get("final_url", ""), "verification": verification,
                "nofollow": "nofollow" in link.rel, "sponsored": "sponsored" in link.rel, "ugc": "ugc" in link.rel,
            })
            if isinstance(status, int) and (status == 0 or 400 <= status < 600) and status not in {401, 403, 405, 429}:
                rows["broken-links.csv"].append({
                    "phase": phase, "source_url": page.url, "destination_url": link.url, "link_type": "external",
                    "anchor_text": link.anchor, "http_status": status, "evidence": probe.get("error", "HTTP failure"),
                    "recommended_action": "verify manually, then update or remove stale destination",
                })

        schema_issues = []
        if not page.schema_valid:
            schema_issues.append("invalid JSON-LD")
        if not page.schemas:
            schema_issues.append("no JSON-LD")
        if page.page_type == "project" and "BlogPosting" in page.schemas:
            schema_issues.append("project represented as BlogPosting")
        if page.page_type in {"category-archive", "tag-archive", "pagination", "blog-index"} and "WebSite" in page.schemas:
            schema_issues.append("listing represented as WebSite")
        visible_match = not any("represented as" in issue for issue in schema_issues)
        rich_eligible = "Article" if "BlogPosting" in page.schemas else "site-name only" if page.url == f"{SITE_ORIGIN}/" else "none identified"
        rows["schema-audit.csv"].append({
            "phase": phase, "url": page.url, "schema_types": "; ".join(page.schemas),
            "json_ld_blocks": page.metadata["json_ld_blocks"], "valid_json": page.schema_valid,
            "visible_match": visible_match, "google_rich_result_eligible": rich_eligible,
            "issues": "; ".join(schema_issues),
            "recommended_action": "use page-type-appropriate, visible, factual schema" if schema_issues else "retain and validate",
        })
        reason = "indexable canonical HTML" if indexable else "missing canonical or noindex"
        rows["indexability.csv"].append({
            "phase": phase, "url": page.url, "local_status": 200, "production_status": production_status,
            "indexable": indexable, "robots_directives": page.robots, "canonical": page.canonical,
            "canonical_target_status": canonical_status, "sitemap_included": page.url in sitemap,
            "sitemap_lastmod": page.sitemap_lastmod, "duplicate_title": duplicate_title,
            "duplicate_description": duplicate_description, "reason": reason,
        })
        crawl_issues = []
        if orphan:
            crawl_issues.append("orphan")
        if page.depth is not None and page.depth > 3:
            crawl_issues.append("more than three clicks from homepage")
        if missing_internal:
            crawl_issues.append(f"{len(missing_internal)} broken internal links")
        rows["crawlability.csv"].append({
            "phase": phase, "url": page.url, "page_depth": page.depth if page.depth is not None else "unreachable",
            "internal_inbound_links": inbound[page.url], "internal_outbound_links": len(page.internal_links),
            "external_outbound_links": len(page.external_links), "orphan": orphan,
            "pages_over_three_clicks": bool(page.depth is not None and page.depth > 3),
            "broken_internal_links": len(missing_internal), "redirect_chain": False,
            "crawlable_html_links": True, "issues": "; ".join(crawl_issues),
        })
        for image in page.images:
            rows["image-audit.csv"].append({"phase": phase, "page_url": page.url, **image})

        asset = asset_totals(page, output)
        html_bytes = page.output_file.stat().st_size
        probe = production_results.get(page.url, {})
        rows["performance.csv"].append({
            "phase": phase, "url": page.url, "html_bytes": html_bytes, "css_bytes": asset["css"],
            "js_bytes": asset["js"], "image_bytes": asset["image"], "font_bytes": asset["font"],
            "estimated_page_bytes": html_bytes + asset["css"] + asset["js"] + asset["image"] + asset["font"],
            "local_request_count": asset["requests"], "lcp_ms": "NOT AVAILABLE — LAB MEASUREMENT REQUIRED",
            "cls": "NOT AVAILABLE — LAB MEASUREMENT REQUIRED", "inp_ms": "NOT AVAILABLE — FIELD DATA REQUIRED",
            "ttfb_ms": probe.get("ttfb_ms", "NOT AVAILABLE — DATA ACCESS REQUIRED"),
            "source": "local generated asset inventory; production HEAD/GET probe where enabled",
            "notes": "Estimated uncompressed bytes; browser transfer and cache behavior differ.",
        })

        full_rows.append({
            "phase": phase, "url": page.url, "source_file": page.source_file, "page_type": page.page_type,
            "local_status": 200, "production_status": production_status, "indexable": indexable,
            "robots_directives": page.robots, "canonical": page.canonical, "canonical_target_status": canonical_status,
            "title": page.title, "title_length": len(page.title), "meta_description": page.description,
            "description_length": len(page.description), "h1": " | ".join(page.h1),
            "h2_h3_structure": " | ".join(item for item in page.headings if item.startswith(("H2", "H3"))),
            "word_count": page.word_count, "language": page.lang, "publication_date": page.published,
            "modified_date": page.modified, "author": page.author, "breadcrumbs": page.breadcrumbs,
            "schema_types": "; ".join(page.schemas), "internal_inbound_links": inbound[page.url],
            "internal_outbound_links": len(page.internal_links), "external_outbound_links": len(page.external_links),
            "broken_links": len(missing_internal), "image_count": len(page.images),
            "images_missing_alt": sum(1 for item in page.images if not item["alt_present"]),
            "images_missing_dimensions": sum(1 for item in page.images if not item["width"] or not item["height"]),
            "page_depth": page.depth if page.depth is not None else "unreachable", "orphan": orphan,
            "sitemap_inclusion": page.url in sitemap, "duplicate_title": duplicate_title,
            "duplicate_description": duplicate_description, "content_sha256": hashlib.sha256(clean_text((page.soup.find("main") or page.soup).get_text(" ", strip=True)).encode()).hexdigest(),
        })
        for category, found in (("metadata", metadata_issues), ("schema", schema_issues), ("crawlability", crawl_issues)):
            for detail in found:
                severity = "P1" if detail in {"missing canonical", "orphan"} else "P2" if any(key in detail for key in ("broken", "represented", "H1")) else "P3"
                issues.append({
                    "phase": phase, "priority": severity, "category": category, "affected_pages": page.url,
                    "evidence": detail, "expected_benefit": "clearer discovery, interpretation, or result presentation",
                    "confidence": "high" if category != "content" else "medium", "difficulty": "low to medium",
                    "recommended_action": "resolve using factual page-specific or systemic markup", "status": "open",
                })

    # Generated aliases are redirect artifacts and are intentionally excluded from the canonical crawl.
    canonical_files = {page.output_file.resolve() for page in pages}
    for html in sorted(output.rglob("*.html")):
        if html.resolve() in canonical_files or html.name == "404.html":
            continue
        soup = BeautifulSoup(html.read_text(errors="ignore"), "html.parser")
        refresh = soup.select_one('meta[http-equiv="refresh"]')
        canonical_node = soup.select_one('link[rel="canonical"]')
        if not refresh and not canonical_node:
            continue
        raw_target = canonical_node.get("href", "") if canonical_node else ""
        if refresh and not raw_target:
            match = re.search(r"url=(.+)$", str(refresh.get("content", "")), re.I)
            raw_target = match.group(1) if match else ""
        source_path = "/" + html.relative_to(output).as_posix()
        rows["redirects.csv"].append({
            "phase": phase, "source_url": urllib.parse.urljoin(SITE_ORIGIN, source_path), "http_status": "client-side alias",
            "target_url": urllib.parse.urljoin(SITE_ORIGIN, raw_target), "chain_length": 1,
            "canonical_target": urllib.parse.urljoin(SITE_ORIGIN, raw_target),
            "issues": "Static host serves HTTP 200; meta refresh is weaker than an HTTP 301/308 redirect.",
        })

    baseline_detail = audit / "baseline-details.json"
    current_detail = {"phase": phase, "datasets": rows}
    if phase == "baseline":
        baseline_detail.parent.mkdir(parents=True, exist_ok=True)
        baseline_detail.write_text(json.dumps(current_detail, indent=2, ensure_ascii=False) + "\n")
    elif baseline_detail.exists():
        baseline_data = json.loads(baseline_detail.read_text())
        for name in CSV_FIELDS:
            rows[name] = baseline_data.get("datasets", {}).get(name, []) + rows[name]

    inventory_fields = list(full_rows[0].keys()) if full_rows else []
    csv_write(audit / ("baseline.csv" if phase == "baseline" else "after.csv"), inventory_fields, full_rows)
    if phase == "baseline":
        csv_write(audit / "site-inventory.csv", inventory_fields, full_rows)
    for name, fields in CSV_FIELDS.items():
        csv_write(audit / name, fields, rows[name])
    issue_fields = ["phase", "priority", "category", "affected_pages", "evidence", "expected_benefit", "confidence", "difficulty", "recommended_action", "status"]
    if phase == "after" and (audit / "issues.csv").exists():
        with (audit / "issues.csv").open(newline="", encoding="utf-8") as handle:
            existing_issues = list(csv.DictReader(handle))
            preserved_issues = [
                row for row in existing_issues
                if row.get("phase") == "baseline"
                or (
                    row.get("phase") == "after"
                    and row.get("category") in {"infrastructure", "measurement", "external links"}
                )
            ]
            issues = preserved_issues + issues
    csv_write(audit / "issues.csv", issue_fields, issues)

    summary = {
        "phase": phase,
        "audit_date": "2026-08-09",
        "pages_audited": len(pages),
        "production_pages_probed": len(production_results),
        "external_urls_probed": len(external_results),
        "indexable_pages": sum(1 for row in full_rows if row["indexable"]),
        "missing_titles": sum(1 for page in pages if not page.title),
        "duplicate_titles": sum(1 for page in pages if title_counts[page.title] > 1),
        "missing_descriptions": sum(1 for page in pages if not page.description),
        "duplicate_descriptions": sum(1 for page in pages if description_counts[page.description] > 1),
        "missing_canonicals": sum(1 for page in pages if not page.canonical),
        "broken_internal_link_instances": sum(1 for row in rows["broken-links.csv"] if row.get("phase") == phase and row.get("link_type") == "internal"),
        "broken_internal_links": len({row["destination_url"] for row in rows["broken-links.csv"] if row.get("phase") == phase and row.get("link_type") == "internal"}),
        "broken_external_link_instances": sum(1 for row in rows["broken-links.csv"] if row.get("phase") == phase and row.get("link_type") == "external"),
        "broken_external_links": len({row["destination_url"] for row in rows["broken-links.csv"] if row.get("phase") == phase and row.get("link_type") == "external"}),
        "orphan_pages": sum(1 for row in full_rows if row["orphan"]),
        "pages_over_three_clicks": sum(1 for row in full_rows if isinstance(row["page_depth"], int) and row["page_depth"] > 3),
        "missing_h1": sum(1 for page in pages if not page.h1),
        "multiple_h1": sum(1 for page in pages if len(page.h1) > 1),
        "images_missing_alt": sum(sum(1 for image in page.images if not image["alt_present"]) for page in pages),
        "images_missing_dimensions": sum(sum(1 for image in page.images if not image["width"] or not image["height"]) for page in pages),
        "broken_images": sum(sum(1 for image in page.images if not image["local_exists"]) for page in pages),
        "schema_errors": sum(1 for page in pages if not page.schema_valid),
        "pages_with_valid_schema": sum(1 for page in pages if page.schema_valid and page.schemas),
        "legacy_meta_keywords_pages": sum(1 for page in pages if page.metadata["keywords"]),
        "redirect_aliases": sum(1 for row in rows["redirects.csv"] if row.get("phase") == phase),
        "robots_sha256": hashlib.sha256((output / "robots.txt").read_bytes()).hexdigest(),
        "sitemap_sha256": hashlib.sha256((output / "sitemap.xml").read_bytes()).hexdigest(),
    }
    (audit / f"{phase}-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit-dir", type=Path, required=True)
    parser.add_argument("--phase", choices=("baseline", "after"), required=True)
    parser.add_argument("--production", action="store_true")
    parser.add_argument("--external", action="store_true")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent.parent
    summary = create_datasets(repo, args.output.resolve(), args.audit_dir.resolve(), args.phase, args.production, args.external)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
