#!/usr/bin/env python3
"""Harden generated aliases and RSS metadata before release validation."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from PIL import Image


SITE_URL = "https://robertdevore.com"
FEED_URL = f"{SITE_URL}/feed/index.xml"
ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"
WRITING_CARD_IMAGE = re.compile(
    r'(<a(?=[^>]*class="listing-card-image-link")[^>]*>)'
    r'<img\b(?=[^>]*class="listing-card-image")[^>]*>'
    r'(</a>)'
)
WRITING_CARD_PLACEHOLDER = re.compile(
    r'<a(?=[^>]*class="listing-card-image-link")[^>]*>'
    r'<span(?=[^>]*class="listing-card-image-placeholder")(?=[^>]*aria-hidden="true")[^>]*></span>'
    r'</a>'
)
RELATIVE_404_ASSET = re.compile(
    r'(?P<attribute>href|src)="(?P<path>'
    r'favicon\.svg|feed/index\.xml|assets/css/site\.bundle\.css\?v=[^"]+|'
    r'assets/js/(?:vendor/scramble-decode|site)\.js\?v=[^"]+'
    r')"'
)


def page_type_for(route: str) -> str:
    if route == "/":
        return "WebSite"
    if route == "/about/":
        return "AboutPage"
    if route == "/contact/":
        return "ContactPage"
    if route == "/blog/" or route.startswith(("/blog/page/", "/category/", "/tag/")) or route == "/projects/":
        return "CollectionPage"
    if route.startswith("/projects/"):
        return "SoftwareSourceCode"
    return "BlogPosting"


def meta_content(soup: BeautifulSoup, selector: str) -> str:
    node = soup.select_one(selector)
    return str(node.get("content", "")).strip() if node else ""


def set_meta(soup: BeautifulSoup, selector: str, value: str) -> None:
    node = soup.select_one(selector)
    if node:
        node["content"] = value


def ensure_meta(soup: BeautifulSoup, attribute: str, name: str, value: str) -> None:
    node = soup.find("meta", attrs={attribute: name})
    if node:
        node["content"] = value
        return
    head = soup.find("head")
    if head:
        head.append(soup.new_tag("meta", attrs={attribute: name, "content": value}))


def breadcrumb_schema(soup: BeautifulSoup, canonical: str) -> dict | None:
    breadcrumb = soup.select_one('[aria-label="Breadcrumbs"]')
    if not breadcrumb:
        return None
    items = []
    for position, node in enumerate(breadcrumb.select("li"), start=1):
        link = node.find("a", href=True)
        name = node.get_text(" ", strip=True)
        item = urljoin(canonical, link.get("href", "")) if link else canonical
        items.append({"@type": "ListItem", "position": position, "name": name, "item": item})
    if not items:
        return None
    return {
        "@type": "BreadcrumbList",
        "@id": f"{canonical}#breadcrumb",
        "itemListElement": items,
    }


def structured_data(soup: BeautifulSoup, route: str) -> dict:
    canonical_node = soup.select_one('link[rel="canonical"]')
    canonical = str(canonical_node.get("href", "")) if canonical_node else urljoin(SITE_URL, route)
    title = meta_content(soup, 'meta[property="og:title"]') or (soup.title.get_text(strip=True) if soup.title else "")
    description = meta_content(soup, 'meta[name="description"]')
    image = meta_content(soup, 'meta[property="og:image"]')
    author_name = meta_content(soup, 'meta[name="author"]') or "Robert DeVore"
    page_type = page_type_for(route)
    person_id = f"{SITE_URL}/#person"
    person = {
        "@type": "Person",
        "@id": person_id,
        "name": author_name,
        "url": f"{SITE_URL}/about/",
        "sameAs": ["https://github.com/robertdevore", "https://x.com/deviorobert"],
    }
    if page_type == "WebSite":
        website = {
            "@type": "WebSite",
            "@id": f"{SITE_URL}/#website",
            "url": f"{SITE_URL}/",
            "name": "Robert DeVore",
            "description": description,
            "publisher": {"@id": person_id},
        }
        if image:
            website["image"] = image
        return {"@context": "https://schema.org", "@graph": [website, person]}

    page: dict = {
        "@type": page_type,
        "@id": f"{canonical}#webpage",
        "url": canonical,
        "name": title,
        "description": description,
        "isPartOf": {"@id": f"{SITE_URL}/#website"},
    }
    if image:
        page["image"] = image
    breadcrumb = breadcrumb_schema(soup, canonical)
    graph = [page, person]
    if breadcrumb:
        page["breadcrumb"] = {"@id": breadcrumb["@id"]}
        graph.append(breadcrumb)
    if page_type == "BlogPosting":
        page["headline"] = title
        page["author"] = {"@id": person_id}
        page["publisher"] = {"@id": person_id}
        page["mainEntityOfPage"] = {"@id": page["@id"]}
        published = meta_content(soup, 'meta[property="article:published_time"]')
        if published:
            page["datePublished"] = published
    elif page_type == "SoftwareSourceCode":
        page["author"] = {"@id": person_id}
        repository = soup.select_one('.project-landing a[href^="https://github.com/"]')
        if repository:
            page["codeRepository"] = repository.get("href", "")
    elif page_type == "AboutPage":
        page["mainEntity"] = {"@id": person_id}
    return {"@context": "https://schema.org", "@graph": graph}


def harden_page_metadata(
    path: Path,
    output: Path,
    social_images: dict[str, str],
) -> tuple[int, int, int, int]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    removed_keywords = 0
    keywords = soup.select_one('meta[name="keywords"]')
    if keywords:
        keywords.decompose()
        removed_keywords = 1

    canonical = soup.select_one('link[rel="canonical"]')
    route = urlparse(str(canonical.get("href", ""))).path or "/" if canonical else ""
    social_updates = 0
    if canonical:
        social_route = "/404.html" if path.name == "404.html" else route
        social_path = social_images.get(social_route)
        if not social_path:
            raise SystemExit(f"Generated-output hardening refused: no HOWL social image for {social_route}")
        social_url = urljoin(SITE_URL, social_path)
        title = meta_content(soup, 'meta[property="og:title"]') or (soup.title.get_text(strip=True) if soup.title else "")
        ensure_meta(soup, "property", "og:image", social_url)
        ensure_meta(soup, "property", "og:image:type", "image/png")
        ensure_meta(soup, "property", "og:image:width", "1200")
        ensure_meta(soup, "property", "og:image:height", "630")
        ensure_meta(soup, "property", "og:image:alt", title)
        ensure_meta(soup, "name", "twitter:image", social_url)
        ensure_meta(soup, "name", "twitter:image:alt", title)
        set_meta(soup, 'meta[name="twitter:card"]', "summary_large_image")
        social_updates = 1
    title_updates = 0
    collection_metadata = {
        "/blog/": (
            "Writing | Robert DeVore",
            "Writing",
            "Field notes on software systems, developer tools, AI workflows, open source, and Robert DeVore's earlier web-development work.",
        ),
        "/category/": (
            "Writing Categories | Robert DeVore",
            "Writing Categories",
            "Browse Robert DeVore's writing by broad subject category.",
        ),
        "/tag/": (
            "Writing Tags | Robert DeVore",
            "Writing Tags",
            "Browse Robert DeVore's writing by topic tag.",
        ),
        "/projects/": (
            "Software Projects | Robert DeVore",
            "Software Projects",
            "Programming-language infrastructure, developer tools, agent workflows, and local-first systems built by Robert DeVore.",
        ),
    }
    page_number = re.fullmatch(r"/blog/page/(\d+)/", route)
    taxonomy = re.fullmatch(r"/(category|tag)/([^/]+)/", route)
    if route in collection_metadata:
        title, social_title, description = collection_metadata[route]
        soup.title.string = title
        set_meta(soup, 'meta[name="description"]', description)
        set_meta(soup, 'meta[property="og:title"]', social_title)
        set_meta(soup, 'meta[property="og:description"]', description)
        set_meta(soup, 'meta[name="twitter:title"]', social_title)
        set_meta(soup, 'meta[name="twitter:description"]', description)
        title_updates = 1
    elif page_number:
        number = page_number.group(1)
        title = f"Writing – Page {number} | Robert DeVore"
        description = f"Page {number} of Robert DeVore's writing archive: software systems, developer tools, AI workflows, open source, and earlier web-development work."
        soup.title.string = title
        set_meta(soup, 'meta[name="description"]', description)
        set_meta(soup, 'meta[property="og:title"]', f"Writing – Page {number}")
        set_meta(soup, 'meta[property="og:description"]', description)
        set_meta(soup, 'meta[name="twitter:title"]', f"Writing – Page {number}")
        set_meta(soup, 'meta[name="twitter:description"]', description)
        title_updates = 1
    elif taxonomy:
        taxonomy_type, _ = taxonomy.groups()
        heading = soup.find("h1")
        name = heading.get_text(" ", strip=True) if heading else "Archive"
        label = "Category" if taxonomy_type == "category" else "Tag"
        description = f"Browse Robert DeVore's writing filed under the {name} {taxonomy_type}."
        soup.title.string = f"{label}: {name} | Robert DeVore"
        set_meta(soup, 'meta[name="description"]', description)
        set_meta(soup, 'meta[property="og:title"]', f"{label}: {name}")
        set_meta(soup, 'meta[property="og:description"]', description)
        set_meta(soup, 'meta[name="twitter:title"]', f"{label}: {name}")
        set_meta(soup, 'meta[name="twitter:description"]', description)
        title_updates = 1

    if canonical:
        social_alt = meta_content(soup, 'meta[property="og:title"]') or (soup.title.get_text(strip=True) if soup.title else "")
        set_meta(soup, 'meta[property="og:image:alt"]', social_alt)
        set_meta(soup, 'meta[name="twitter:image:alt"]', social_alt)

    twitter_card = soup.select_one('meta[name="twitter:card"]')
    if twitter_card and not soup.select_one('meta[name="twitter:image"]'):
        twitter_card["content"] = "summary"

    if not canonical:
        path.write_text(str(soup), encoding="utf-8")
        return removed_keywords, title_updates, 0, social_updates

    dimension_updates = 0
    for image in soup.find_all("img"):
        src = str(image.get("src", ""))
        parsed = urlparse(src)
        if parsed.scheme and parsed.netloc not in {"robertdevore.com", "www.robertdevore.com"}:
            continue
        clean = parsed.path if parsed.scheme else src.split("?", 1)[0].split("#", 1)[0]
        asset = output / clean.lstrip("/") if clean.startswith("/") else (path.parent / clean).resolve()
        if (not image.get("width") or not image.get("height")) and asset.is_file():
            try:
                with Image.open(asset) as source:
                    width, height = source.size
                image["width"] = str(width)
                image["height"] = str(height)
                dimension_updates += 1
            except (OSError, ValueError):
                pass
        if not image.find_parent(class_="signal-hero__field"):
            image["loading"] = "lazy"
            image["decoding"] = "async"

    schemas = soup.find_all("script", attrs={"type": "application/ld+json"})
    if schemas:
        schemas[0].string = json.dumps(structured_data(soup, route), ensure_ascii=False, separators=(",", ":"))
        for duplicate in schemas[1:]:
            duplicate.decompose()
    path.write_text(str(soup), encoding="utf-8")
    return removed_keywords, title_updates, dimension_updates, social_updates


def main() -> int:
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
    if not output.is_dir():
        print(f"Generated-output hardening refused: missing {output}", file=sys.stderr)
        return 1

    social_map_path = output / "assets" / "social" / "social-image-map.json"
    if not social_map_path.is_file():
        print(f"Generated-output hardening refused: missing {social_map_path}", file=sys.stderr)
        return 1
    try:
        social_images = json.loads(social_map_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Generated-output hardening refused: invalid social image map: {exc}", file=sys.stderr)
        return 1
    if not isinstance(social_images, dict) or not social_images:
        print("Generated-output hardening refused: social image map is empty", file=sys.stderr)
        return 1

    root_pagination = output / "page"
    removed_root_pages = len(list(root_pagination.rglob("index.html"))) if root_pagination.is_dir() else 0
    if root_pagination.is_dir():
        shutil.rmtree(root_pagination)

    sitemap_path = output / "sitemap.xml"
    if not sitemap_path.is_file():
        print(f"Generated-output hardening refused: missing {sitemap_path}", file=sys.stderr)
        return 1
    sitemap = sitemap_path.read_text(encoding="utf-8")
    root_page_entry = re.compile(
        r"\s*<url>\s*<loc>https://robertdevore\.com/page/\d+/</loc>.*?</url>",
        re.DOTALL,
    )
    sitemap, removed_sitemap_pages = root_page_entry.subn("", sitemap)
    sitemap_path.write_text(sitemap, encoding="utf-8")
    if removed_root_pages != removed_sitemap_pages:
        print(
            "Generated-output hardening refused: root pagination and sitemap removal counts differ "
            f"({removed_root_pages} files, {removed_sitemap_pages} sitemap URLs)",
            file=sys.stderr,
        )
        return 1

    aliases = 0
    for path in sorted(output.rglob("*.html")):
        if path.name in {"index.html", "404.html"}:
            continue
        html = path.read_text(encoding="utf-8")
        if "<title>" not in html:
            marker = '<meta http-equiv="refresh"'
            if html.count(marker) != 1:
                print(
                    f"Generated-output hardening refused: malformed alias {path.relative_to(output)}",
                    file=sys.stderr,
                )
                return 1
            html = html.replace(marker, "<title>Redirecting | Robert DeVore</title>" + marker)
            path.write_text(html, encoding="utf-8")
            aliases += 1

    writing_cards = 0
    blog_root = output / "blog"
    for path in sorted(blog_root.rglob("index.html")):
        html = path.read_text(encoding="utf-8")
        existing_placeholders = len(WRITING_CARD_PLACEHOLDER.findall(html))
        html, replacements = WRITING_CARD_IMAGE.subn(
            r'\1<span class="listing-card-image-placeholder" aria-hidden="true"></span>\2',
            html,
        )
        card_count = existing_placeholders + replacements
        if replacements > 0:
            path.write_text(html, encoding="utf-8")
        writing_cards += card_count

    if writing_cards == 0:
        print(
            "Generated-output hardening refused: expected writing cards, found none",
            file=sys.stderr,
        )
        return 1

    home_path = output / "index.html"
    home_html = home_path.read_text(encoding="utf-8")
    home_placeholders = len(WRITING_CARD_PLACEHOLDER.findall(home_html))
    home_html, home_replacements = WRITING_CARD_IMAGE.subn(
        r'\1<span class="listing-card-image-placeholder" aria-hidden="true"></span>\2',
        home_html,
    )
    home_cards = home_placeholders + home_replacements
    if home_cards != 3:
        print(
            f"Generated-output hardening refused: expected three homepage writing cards, found {home_cards}",
            file=sys.stderr,
        )
        return 1
    if home_replacements > 0:
        home_path.write_text(home_html, encoding="utf-8")

    not_found_path = output / "404.html"
    if not not_found_path.is_file():
        print(f"Generated-output hardening refused: missing {not_found_path}", file=sys.stderr)
        return 1
    not_found_html = not_found_path.read_text(encoding="utf-8")
    not_found_html, not_found_assets = RELATIVE_404_ASSET.subn(
        lambda match: f'{match.group("attribute")}="/{match.group("path")}"',
        not_found_html,
    )
    if RELATIVE_404_ASSET.search(not_found_html):
        print("Generated-output hardening refused: relative 404 assets remain", file=sys.stderr)
        return 1
    for expected in (
        'href="/favicon.svg"',
        'href="/feed/index.xml"',
        'href="/assets/css/site.bundle.css?',
        'src="/assets/js/vendor/scramble-decode.js?',
        'src="/assets/js/site.js?',
    ):
        if expected not in not_found_html:
            print(
                f"Generated-output hardening refused: 404 page is missing {expected}",
                file=sys.stderr,
            )
            return 1
    if not_found_assets:
        not_found_path.write_text(not_found_html, encoding="utf-8")

    feed_path = output / "feed/index.xml"
    if not feed_path.is_file():
        print(f"Generated-output hardening refused: missing {feed_path}", file=sys.stderr)
        return 1
    feed = feed_path.read_text(encoding="utf-8")
    rss_open = '<rss version="2.0">'
    if rss_open in feed:
        feed = feed.replace(
            rss_open,
            f'<rss version="2.0" xmlns:atom="{ATOM_NAMESPACE}">',
            1,
        )
    self_link = f'<atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>'
    if self_link not in feed:
        channel_open = "<channel>"
        if feed.count(channel_open) != 1:
            print("Generated-output hardening refused: malformed RSS channel", file=sys.stderr)
            return 1
        feed = feed.replace(channel_open, channel_open + self_link, 1)
    for encoded, entity in (
        ("&amp;apos;", "&apos;"),
        ("&amp;quot;", "&quot;"),
    ):
        feed = feed.replace(encoded, entity)
    feed_path.write_text(feed, encoding="utf-8")

    removed_keywords = 0
    metadata_titles = 0
    image_dimensions = 0
    social_metadata = 0
    metadata_pages = sorted(output.rglob("index.html")) + [output / "404.html"]
    for path in metadata_pages:
        keywords, titles, dimensions, social = harden_page_metadata(path, output, social_images)
        removed_keywords += keywords
        metadata_titles += titles
        image_dimensions += dimensions
        social_metadata += social

    print(
        f"Hardened {aliases} redirect aliases, {writing_cards} writing card, "
        f"{home_cards} homepage card, {not_found_assets} nested-route 404 assets, "
        f"{removed_root_pages} duplicate root pagination routes, {removed_keywords} legacy keyword tags, "
        f"{metadata_titles} archive metadata records, {image_dimensions} image dimension records, "
        f"{social_metadata} route-specific social images, page-type JSON-LD, and RSS discovery metadata."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
