#!/usr/bin/env python3
"""Build and verify the site's single, release-versioned CSS bundle."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
BUNDLE = ROOT / "assets/css/site.bundle.css"
CRITICAL = ROOT / "assets/css/site.critical.css"
SOURCES = (
    ROOT / "assets/css/sitekit/reset.css",
    ROOT / "assets/css/sitekit/tokens.css",
    ROOT / "assets/css/sitekit/themes.css",
    ROOT / "assets/css/sitekit/base.css",
    ROOT / "assets/css/sitekit/components.css",
    ROOT / "assets/css/sitekit/utilities.css",
    ROOT / "assets/css/site.css",
)
URL_PATTERN = re.compile(r"url\((?P<quote>['\"]?)(?P<url>[^)'\"]+)(?P=quote)\)")
LEGACY_CRITICAL_CSS = """
@font-face{font-family:"Departure Mono";src:url("/assets/fonts/DepartureMono-Regular.woff2?v={version}") format("woff2");font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:"Inter";src:url("/assets/fonts/inter-latin-400.woff2?v={version}") format("woff2");font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:"Inter";src:url("/assets/fonts/inter-latin-700.woff2?v={version}") format("woff2");font-weight:700;font-style:normal;font-display:swap}
html{box-sizing:border-box;text-size-adjust:100%}
*,*::before,*::after{box-sizing:inherit}
body{margin:0;min-height:100vh;display:flex;flex-direction:column;background:#fff;color:#111;font-family:"Inter",Arial,sans-serif;line-height:1.5}
main{flex:1 0 auto}
img,svg,video{display:block;max-width:100%}
a{text-underline-offset:.2em}
.site-header a,.signal-hero a{color:#111}
.sk-skip-link{position:absolute;left:-9999px;top:auto}
.sk-skip-link:focus{left:1rem;top:1rem;z-index:1000;padding:.75rem 1rem;background:#fff;color:#111}
.site-header{position:relative;z-index:20;border-bottom:1px solid #d9d9d9;background:#fff}
.site-header .sk-header__inner{display:flex;align-items:center;justify-content:space-between;width:100%;max-width:90rem;min-height:4.5rem;margin:0 auto;padding:1rem 2rem}
.site-brand,.site-nav a,.site-menu{font-family:"Departure Mono",monospace;font-size:.875rem;text-transform:uppercase}
.site-brand{display:inline-flex;text-decoration:none}.site-brand span{margin-right:.5rem;color:#c40000}
.site-nav a{margin-left:1.5rem;text-decoration:none}.site-menu{display:none}
.signal-hero{position:relative;display:grid;align-items:center;min-height:34rem;overflow:hidden;background:#111}
.signal-hero__field{position:absolute;top:0;right:0;bottom:0;left:0;margin:0;overflow:hidden}
.signal-hero__field img{width:100%;height:100%;object-fit:cover}
.signal-hero__inner{position:relative;z-index:1;width:100%;max-width:90rem;margin:0 auto;padding:6rem 2rem}
.signal-kicker,.signal-lede,.signal-hero .sk-breadcrumbs,.article-terms{display:table;width:auto;padding:.15rem .35rem;background:#fff;color:#111}
.signal-kicker,.article-terms,.sk-breadcrumbs{font-family:"Departure Mono",monospace;font-size:.8rem;text-transform:uppercase}
.signal-title{max-width:18ch;margin:0 0 1.5rem;color:#111;font-family:"Departure Mono",monospace;font-size:5rem;font-weight:400;line-height:.9}
.signal-lede{max-width:64ch;margin:0 0 1.5rem;font-size:1.25rem}
.signal-actions{display:flex;flex-wrap:wrap}.signal-hero .sk-button{display:inline-flex;padding:.75rem 1rem;border:1px solid #111;background:#111;color:#fff;font-family:"Departure Mono",monospace;text-decoration:none;text-transform:uppercase}.signal-actions .sk-button+.sk-button{margin-left:.75rem;background:#fff;color:#111}
.home-page>.signal-hero .signal-hero__inner{text-align:center}.home-page>.signal-hero .signal-title,.home-page>.signal-hero .signal-kicker,.home-page>.signal-hero .signal-lede,.home-page>.signal-hero .signal-actions{margin-right:auto;margin-left:auto}.home-page>.signal-hero .signal-title{position:relative;z-index:1}.home-page>.signal-hero .signal-title::before{content:attr(data-text);position:absolute;z-index:-1;top:0;right:0;bottom:0;left:0;color:transparent;-webkit-text-stroke:8px #fff;pointer-events:none}
@media(max-width:48rem){.site-header .sk-header__inner{padding-right:1rem;padding-left:1rem}.site-nav--desktop{display:none}.site-menu{display:block}.signal-hero{min-height:30rem}.signal-hero__inner{padding:5rem 1rem 2.5rem}.signal-title{font-size:3rem}.signal-lede{font-size:1rem}}
"""


def rewrite_urls(css: str, source: Path, *, absolute: bool = False) -> str:
    """Resolve local URLs from each source file relative to the bundle."""

    def replace(match: re.Match[str]) -> str:
        url = match.group("url").strip()
        if url.startswith(("data:", "http:", "https:", "#")):
            return match.group(0)
        path, separator, fragment = url.partition("#")
        path, query_separator, _query = path.partition("?")
        target = (source.parent / path).resolve()
        if absolute:
            relative = "/" + target.relative_to(ROOT).as_posix()
        else:
            relative = Path(os.path.relpath(target, BUNDLE.parent)).as_posix()
        suffix = f"?v={VERSION}"
        if separator:
            suffix += f"#{fragment}"
        quote = match.group("quote")
        return f"url({quote}{relative}{suffix}{quote})"

    return URL_PATTERN.sub(replace, css)


def flatten_layers(css: str) -> str:
    """Unwrap top-level cascade layers while preserving their source order."""

    output: list[str] = []
    cursor = 0
    layer_pattern = re.compile(r"@layer\s+[a-zA-Z0-9_.-]+\s*\{")
    while match := layer_pattern.search(css, cursor):
        output.append(css[cursor : match.start()])
        opening = match.end() - 1
        depth = 0
        for index in range(opening, len(css)):
            if css[index] == "{":
                depth += 1
            elif css[index] == "}":
                depth -= 1
                if depth == 0:
                    output.append(css[opening + 1 : index])
                    cursor = index + 1
                    break
        else:
            raise ValueError("unbalanced CSS cascade layer")
    output.append(css[cursor:])
    return "\n".join(line.rstrip() for line in "".join(output).splitlines())


def render_bundle() -> str:
    sections = [
        f"/* RobertDeVore.com v{VERSION}; generated by scripts/bundle_css.py. */"
    ]
    for source in SOURCES:
        if not source.is_file():
            raise FileNotFoundError(f"missing CSS source: {source.relative_to(ROOT)}")
        css = flatten_layers(source.read_text(encoding="utf-8")).strip()
        sections.append(
            f"/* source: {source.relative_to(ROOT).as_posix()} */\n"
            f"{rewrite_urls(css, source)}"
        )
    return "\n".join(sections) + "\n"


def render_critical() -> str:
    """Render a small legacy-compatible shell while the complete bundle loads."""

    header = f"/* RobertDeVore.com v{VERSION} critical CSS; generated by scripts/bundle_css.py. */"
    return header + "\n" + LEGACY_CRITICAL_CSS.strip().replace("{version}", VERSION) + "\n"


def write_atomically(destination: Path, payload: str) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="fail when the committed bundle is stale"
    )
    args = parser.parse_args()
    expected = {BUNDLE: render_bundle(), CRITICAL: render_critical()}
    if args.check:
        stale = [
            path.relative_to(ROOT)
            for path, payload in expected.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != payload
        ]
        if stale:
            print("CSS bundle is stale; run: python3 scripts/bundle_css.py", file=sys.stderr)
            print("Stale: " + ", ".join(str(path) for path in stale), file=sys.stderr)
            return 1
        print(f"CSS bundle checks passed for RobertDeVore.com v{VERSION}.")
        return 0
    for path, payload in expected.items():
        write_atomically(path, payload)
        print(f"Wrote {path.relative_to(ROOT)} for RobertDeVore.com v{VERSION}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
