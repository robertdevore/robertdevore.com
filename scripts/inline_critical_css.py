#!/usr/bin/env python3
"""Inline the release critical CSS into generated HTML pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER = "/* build:critical-css */"
STYLE_PATTERN = re.compile(r'<style data-critical-css>.*?</style>', re.DOTALL)


def main() -> int:
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
    if not output.is_dir():
        print(f"Critical CSS injection refused: missing output directory {output}", file=sys.stderr)
        return 1
    css_path = ROOT / "assets/css/site.critical.css"
    if not css_path.is_file():
        print(f"Critical CSS injection refused: missing {css_path}", file=sys.stderr)
        return 1
    critical_css = css_path.read_text(encoding="utf-8").strip()
    replacement = f'<style data-critical-css>{critical_css}</style>'
    expected = f'<style data-critical-css>{MARKER}</style>'
    html_files = sorted(output.rglob("*.html"))
    changed = 0
    for path in html_files:
        html = path.read_text(encoding="utf-8")
        marker_count = html.count(expected)
        if marker_count == 0 and "site.bundle.css" not in html:
            continue
        style_count = len(STYLE_PATTERN.findall(html))
        if marker_count == 1:
            updated = html.replace(expected, replacement)
        elif marker_count == 0 and style_count == 1:
            updated = STYLE_PATTERN.sub(replacement, html, count=1)
        else:
            print(
                f"Critical CSS injection refused: expected one critical style in {path.relative_to(output)}",
                file=sys.stderr,
            )
            return 1
        path.write_text(updated, encoding="utf-8")
        changed += 1
    print(f"Inlined critical CSS into {changed} generated HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
