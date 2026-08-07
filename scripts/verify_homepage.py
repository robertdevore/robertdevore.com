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
if len(identity.select(".section-index")) != 1 or len(identity.find_all("p")) != 1:
    fail("flagship identity must contain only its single section index")
if identity.select(".card-signal, h2, h3, .flagship-content, .project-feature__actions"):
    fail("flagship identity contains removed or right-column content")
if flagship.select_one(".flagship-panel"):
    fail("legacy flagship-panel markup is still present")

if home.select_one("#flagship-title").get_text(" ", strip=True) != "Language, runtime, and local software workflows.":
    fail("flagship title copy is incorrect")
if home.select_one("#systems-title").get_text(" ", strip=True) != "Tools with a visible operating record.":
    fail("selected systems title copy is incorrect")
if home.select_one(".home-focus h3").find(string=lambda value: value and "Repo Radar" in value):
    fail("selected systems still uses spaced Repo Radar label")
if not home.find(string=lambda value: value and "RepoRadar" in value):
    fail("selected systems is missing RepoRadar label")
if not home.find(string=lambda value: value and "Pressure-test the ecosystem" in value):
    fail("leadership principle copy is incorrect")
if not home.find(string=lambda value: value and "Systems should explain the assumptions, input, output, and failures without vocal explanations being required." in value):
    fail("context principle copy is incorrect")
writing_cards = home.select("#writing .listing-card")
if len(writing_cards) != 3:
    fail(f"homepage writing section must contain exactly three recent posts, found {len(writing_cards)}")
if not home.select_one(".home-closing"):
    fail("homepage closing statement is missing")

css = css_path.read_text(errors="ignore")
required_css = (
    '@font-face{font-family:"Departure Mono"',
    ".home-page h1,.home-page h2,.home-page h3,.home-page h4{font-family:var(--sk-font-mono)",
    ".home-page .home-flagship,.home-page .home-focus,.home-page .home-principles,.home-page .writing-index,.home-page .home-closing{font-family:var(--sk-font-mono)",
    ".flagship-layout{display:grid",
    "border-block-end:var(--sk-border-1) solid var(--sk-border-default)",
    ".flagship-content h2",
)
for contract in required_css:
    if contract not in css:
        fail(f"site CSS is missing typography/layout contract: {contract}")

print("Homepage flagship structure and mono typography contract passed")
