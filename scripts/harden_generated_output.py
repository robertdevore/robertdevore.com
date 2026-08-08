#!/usr/bin/env python3
"""Harden generated aliases and RSS metadata before release validation."""

from __future__ import annotations

import re
import sys
from pathlib import Path


SITE_URL = "https://robertdevore.com"
FEED_URL = f"{SITE_URL}/feed/index.xml"
ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"
FOREVER_FORWARD_CARD_IMAGE = re.compile(
    r'(<a class="listing-card-image-link" href="/forever-forward/">)'
    r'<img\b[^>]*class="listing-card-image"[^>]*>'
    r'(</a>)'
)
FOREVER_FORWARD_CARD_PLACEHOLDER = re.compile(
    r'<a class="listing-card-image-link" href="/forever-forward/">'
    r'<span class="listing-card-image-placeholder" aria-hidden="true"></span>'
    r'</a>'
)
RELATIVE_404_ASSET = re.compile(
    r'(?P<attribute>href|src)="(?P<path>'
    r'favicon\.svg|feed/index\.xml|assets/css/site\.bundle\.css\?v=[^"]+|'
    r'assets/js/(?:vendor/scramble-decode|site)\.js\?v=[^"]+'
    r')"'
)


def main() -> int:
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
    if not output.is_dir():
        print(f"Generated-output hardening refused: missing {output}", file=sys.stderr)
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
        existing_placeholders = len(FOREVER_FORWARD_CARD_PLACEHOLDER.findall(html))
        html, replacements = FOREVER_FORWARD_CARD_IMAGE.subn(
            r'\1<span class="listing-card-image-placeholder" aria-hidden="true"></span>\2',
            html,
        )
        card_count = existing_placeholders + replacements
        if card_count > 1:
            print(
                f"Generated-output hardening refused: duplicate Forever Forward cards in {path.relative_to(output)}",
                file=sys.stderr,
            )
            return 1
        if replacements == 1:
            path.write_text(html, encoding="utf-8")
        writing_cards += card_count

    if writing_cards != 1:
        print(
            f"Generated-output hardening refused: expected one Forever Forward writing card, found {writing_cards}",
            file=sys.stderr,
        )
        return 1

    home_path = output / "index.html"
    home_html = home_path.read_text(encoding="utf-8")
    home_placeholders = len(FOREVER_FORWARD_CARD_PLACEHOLDER.findall(home_html))
    home_html, home_replacements = FOREVER_FORWARD_CARD_IMAGE.subn(
        r'\1<span class="listing-card-image-placeholder" aria-hidden="true"></span>\2',
        home_html,
    )
    home_cards = home_placeholders + home_replacements
    if home_cards > 1:
        print(
            "Generated-output hardening refused: duplicate Forever Forward cards on homepage",
            file=sys.stderr,
        )
        return 1
    if home_replacements == 1:
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

    print(
        f"Hardened {aliases} redirect aliases, {writing_cards} writing card, "
        f"{home_cards} homepage card, {not_found_assets} nested-route 404 assets, "
        "and RSS discovery metadata."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
