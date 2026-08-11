#!/usr/bin/env python3
"""Render the site's HOWL social cards into committed SVG and PNG assets."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "howl.json"
SVG_OUTPUT = ROOT / "assets" / "social" / "howl"
PNG_OUTPUT = ROOT / "assets" / "social"
HOWL_BRAND_PREFIX = "KUJOLANG.AI  //  "
GRAIN_OVERLAY = '<rect width="1200" height="630" filter="url(#grain)" opacity=".7"/>\n'
EMBEDDED_FONT_STACK = "font-family:'HowlMono','Departure Mono',monospace"
PORTABLE_FONT_STACK = "font-family:'Departure Mono',monospace"


def howl_binary() -> str:
    configured = os.environ.get("HOWL_BIN", "").strip()
    if configured:
        return configured
    discovered = shutil.which("howl")
    if discovered:
        return discovered
    raise SystemExit("HOWL is unavailable; install it on PATH or set HOWL_BIN.")


def site_brand(manifest: dict) -> str:
    project = manifest.get("project", {})
    host = urlparse(str(project.get("url", ""))).hostname
    if host:
        return host.removeprefix("www.").upper()
    name = str(project.get("name", "")).strip()
    if name:
        return name.upper()
    raise SystemExit("HOWL project.url or project.name is required for site branding.")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = manifest.get("cards", [])
    if not cards:
        raise SystemExit("HOWL manifest has no cards to render.")

    binary = howl_binary()
    subprocess.run(
        [binary, "validate", "--manifest", str(MANIFEST)],
        cwd=ROOT,
        check=True,
    )

    SVG_OUTPUT.mkdir(parents=True, exist_ok=True)
    PNG_OUTPUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="robertdevore-howl-") as temporary:
        rendered = Path(temporary)
        font_config = rendered / "fonts.conf"
        font_config.write_text(
            '<?xml version="1.0"?>\n'
            '<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n'
            f'<fontconfig><dir>{ROOT / "assets" / "fonts"}</dir></fontconfig>\n',
            encoding="utf-8",
        )
        os.environ["FONTCONFIG_FILE"] = str(font_config)
        import cairosvg

        subprocess.run(
            [
                binary,
                "render",
                "--manifest",
                str(MANIFEST),
                "--out",
                str(rendered),
                "--format",
                "svg",
            ],
            cwd=ROOT,
            check=True,
        )

        brand_prefix = f"{site_brand(manifest)}  //  "
        for card in cards:
            card_id = str(card["id"])
            source = rendered / f"{card_id}.svg"
            svg = source.read_text(encoding="utf-8")
            if HOWL_BRAND_PREFIX not in svg:
                raise SystemExit(f"HOWL brand marker is missing from {source.name}.")
            branded_svg = svg.replace(HOWL_BRAND_PREFIX, brand_prefix, 1)
            svg_target = SVG_OUTPUT / source.name
            svg_target.write_text(branded_svg, encoding="utf-8")

            # CairoSVG renders HOWL's turbulence filter as a gray veil. The
            # committed SVG retains that browser-safe grain; the PNG omits it.
            # CairoSVG also needs the repository font exposed through
            # fontconfig instead of HOWL's browser-oriented @font-face data.
            portable_svg = branded_svg.replace(GRAIN_OVERLAY, "", 1).replace(
                EMBEDDED_FONT_STACK,
                PORTABLE_FONT_STACK,
                1,
            )
            cairosvg.svg2png(
                bytestring=portable_svg.encode("utf-8"),
                write_to=str(PNG_OUTPUT / f"{card_id}-social.png"),
                output_width=1200,
                output_height=630,
            )

    print(f"Rendered {len(cards)} branded HOWL social cards.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
