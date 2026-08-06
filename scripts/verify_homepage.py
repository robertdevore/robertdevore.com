#!/usr/bin/env python3
"""Verify the homepage flagship structure and mono typography contract."""

from __future__ import annotations

import sys
from pathlib import Path

from bs4 import BeautifulSoup


def fail(message: str) -> None:
    print(f"ERROR {message}")
    raise SystemExit(1)


root = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
home_path = root / "index.html"
css_path = root / "assets/css/site.css"
if not home_path.is_file():
    fail(f"missing generated homepage: {home_path}")
if not css_path.is_file():
    fail(f"missing generated site CSS: {css_path}")

home = BeautifulSoup(home_path.read_text(errors="ignore"), "html.parser")
flagship = home.select_one(".home-flagship")
layout = flagship.select_one(".flagship-layout") if flagship else None
identity = layout.select_one(".flagship-identity") if layout else None
content = layout.select_one(".flagship-content") if layout else None
if not all((flagship, layout, identity, content)):
    fail("homepage is missing the Kujo flagship layout, identity, or content column")

if len(content.find_all("h2")) != 1:
    fail("flagship content must contain exactly one title")
if not content.select_one("h2#flagship-title"):
    fail("flagship title is missing its stable id")
if len(content.select("p")) != 1:
    fail("flagship content must contain exactly one subtitle paragraph")
actions = content.select(".project-feature__actions a")
if len(actions) != 2:
    fail("flagship content must contain exactly two action links")
if not identity.select_one(".section-index") or not identity.select_one(".card-signal"):
    fail("flagship identity is missing its section or Kujo signal")
if identity.select_one("h3").get_text(" ", strip=True) != "Kujo":
    fail("flagship identity name is not Kujo")
if identity.select("h2, .flagship-content, .project-feature__actions"):
    fail("flagship identity contains right-column content")
if flagship.select_one(".flagship-panel"):
    fail("legacy flagship-panel markup is still present")

css = css_path.read_text(errors="ignore")
required_css = (
    '@font-face{font-family:"Departure Mono"',
    ".home-page h1,.home-page h2,.home-page h3,.home-page h4{font-family:var(--sk-font-mono)",
    ".home-page .home-flagship,.home-page .home-focus,.home-page .home-principles,.home-page .writing-index,.home-page .home-closing{font-family:var(--sk-font-mono)",
    ".flagship-layout{display:grid",
    ".flagship-content h2",
)
for contract in required_css:
    if contract not in css:
        fail(f"site CSS is missing typography/layout contract: {contract}")

print("Homepage flagship structure and mono typography contract passed")
