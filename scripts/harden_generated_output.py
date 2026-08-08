#!/usr/bin/env python3
"""Harden generated aliases and RSS metadata before release validation."""

from __future__ import annotations

import sys
from pathlib import Path


SITE_URL = "https://robertdevore.com"
FEED_URL = f"{SITE_URL}/feed/index.xml"
ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"


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

    print(f"Hardened {aliases} redirect aliases and RSS discovery metadata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
