#!/usr/bin/env python3
"""Build the complete HOWL manifest from the site's authored content."""

from __future__ import annotations

import ast
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "howl.json"
CONTENT = ROOT / "content"
FONT = "assets/fonts/DepartureMono-Regular.woff2"
BACKGROUNDS = {
    "signal-a": "assets/art/signal-a-1920.webp",
    "signal-b": "assets/art/signal-b-1920.webp",
    "signal-c": "assets/art/signal-c-1920.webp",
}
SPECIAL_BACKGROUNDS = {
    "forever-forward": "assets/social/forever-forward-background.webp",
}
SPECIAL_LABELS = {
    "forever-forward": "THE JIDOKA FILES",
}


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.DOTALL)
    if not match:
        raise SystemExit(f"Missing frontmatter: {path.relative_to(ROOT)}")
    result: dict[str, object] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        value = raw.strip()
        if not value:
            result[key.strip()] = ""
            continue
        try:
            result[key.strip()] = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            result[key.strip()] = value
    return result


def text(meta: dict[str, object], key: str, fallback: str = "") -> str:
    value = meta.get(key, fallback)
    return str(value).strip() if value is not None else fallback


def terms(meta: dict[str, object], key: str) -> list[str]:
    value = meta.get(key, [])
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def fit_for_howl(value: str, max_chars: int, max_lines: int) -> str:
    """Fit text before HOWL wrapping so the current VM never slices overflow lines."""
    words = value.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    if len(lines) <= max_lines:
        return " ".join(lines)
    kept = lines[:max_lines]
    final_words = kept[-1].split()
    while final_words and len(" ".join(final_words)) + 2 > max_chars:
        final_words.pop()
    kept[-1] = (" ".join(final_words) or kept[-1][: max_chars - 2]).rstrip() + " …"
    return " ".join(kept)


def card(
    *,
    card_id: str,
    route: str,
    title: str,
    tagline: str,
    source: str,
    label: str,
    background: str,
    concepts: list[str] | None = None,
    language: str = "markdown",
) -> dict[str, object]:
    visual_title = fit_for_howl(title, 20, 3)
    visual_tagline = fit_for_howl(tagline, 47, 2)
    return {
        "id": card_id,
        "title": visual_title,
        "tagline": visual_tagline,
        "file": source,
        "language": language,
        "concepts": concepts or [label.lower()],
        "caption": f"{title}: {tagline}" if tagline else title,
        "cta": "Read more on RobertDeVore.com.",
        "url": f"https://robertdevore.com{route}",
        "variant": "social",
        "label": label.upper(),
        "background_image": background,
        "font_file": FONT,
        "show_url": False,
    }


def content_card(path: Path, kind: str) -> dict[str, object]:
    meta = frontmatter(path)
    slug = text(meta, "custom_url", path.stem)
    title = text(meta, "title")
    tagline = text(meta, "description", text(meta, "excerpt"))
    template = text(meta, "template", "signal-a")
    background = SPECIAL_BACKGROUNDS.get(slug, BACKGROUNDS.get(template, BACKGROUNDS["signal-a"]))
    relative = path.relative_to(ROOT).as_posix()

    if kind == "post":
        route = f"/{slug}/"
        categories = terms(meta, "categories")
        tags = terms(meta, "tags")
        label = SPECIAL_LABELS.get(slug, categories[0] if categories else "WRITING")
        concepts = categories + tags
        card_id = slug
    elif kind == "page":
        route = f"/{slug}/"
        label = "PROFILE" if slug == "about" else "CONNECT"
        concepts = [slug, "Robert DeVore"]
        card_id = slug
    elif kind == "project":
        route = f"/projects/{slug}/"
        label = "SOFTWARE PROJECT"
        concepts = terms(meta, "tags") or ["software project"]
        card_id = f"project-{slug}"
    elif kind == "category":
        route = f"/category/{slug}/"
        label = "WRITING CATEGORY"
        concepts = [title, "writing archive"]
        card_id = f"category-{slug}"
    elif kind == "tag":
        route = f"/tag/{slug}/"
        label = "WRITING TAG"
        concepts = [title, "writing archive"]
        card_id = f"tag-{slug}"
    else:
        raise ValueError(f"Unsupported content kind: {kind}")

    return card(
        card_id=card_id,
        route=route,
        title=title,
        tagline=tagline,
        source=relative,
        label=label,
        background=background,
        concepts=concepts,
    )


def build_manifest() -> dict[str, object]:
    cards: list[dict[str, object]] = [
        card(
            card_id="home",
            route="/",
            title="Robert DeVore",
            tagline="Systems, tools, and writing for work that has to hold up",
            source="templates/page-home.html",
            label="HOME",
            background=BACKGROUNDS["signal-a"],
            concepts=["software systems", "developer tools", "agentic workflows"],
            language="html",
        ),
        card(
            card_id="not-found",
            route="/404.html",
            title="Page Not Found",
            tagline="The requested signal could not be located",
            source="templates/404.html",
            label="SYSTEM / 404",
            background=BACKGROUNDS["signal-c"],
            concepts=["404", "not found"],
            language="html",
        ),
        card(
            card_id="writing",
            route="/blog/",
            title="Writing",
            tagline="Field notes on software systems, developer tools, AI workflows, and open source",
            source="templates/page-blog.html",
            label="WRITING ARCHIVE",
            background=BACKGROUNDS["signal-b"],
            language="html",
        ),
        card(
            card_id="category-index",
            route="/category/",
            title="Writing Categories",
            tagline="Browse the archive by broad subject category",
            source="templates/page-category.html",
            label="WRITING ARCHIVE",
            background=BACKGROUNDS["signal-c"],
            language="html",
        ),
        card(
            card_id="tag-index",
            route="/tag/",
            title="Writing Tags",
            tagline="Browse the archive by topic tag",
            source="templates/page-tag.html",
            label="WRITING ARCHIVE",
            background=BACKGROUNDS["signal-a"],
            language="html",
        ),
        card(
            card_id="projects",
            route="/projects/",
            title="Software Projects",
            tagline="Programming-language infrastructure, developer tools, agent workflows, and local-first systems",
            source="templates/page-projects.html",
            label="PROJECT INDEX",
            background=BACKGROUNDS["signal-c"],
            language="html",
        ),
    ]

    posts = sorted((CONTENT / "posts").glob("*.md"))
    posts_per_page = 12
    config = (ROOT / "kujo-ssg.yml").read_text(encoding="utf-8")
    match = re.search(r"(?m)^posts_per_page:\s*(\d+)\s*$", config)
    if match:
        posts_per_page = int(match.group(1))
    page_count = math.ceil(len(posts) / posts_per_page)
    for number in range(2, page_count + 1):
        cards.append(
            card(
                card_id=f"writing-page-{number}",
                route=f"/blog/page/{number}/",
                title=f"Writing — Page {number}",
                tagline="Software systems, developer tools, AI workflows, open source, and the web-development archive",
                source="templates/page-blog.html",
                label="WRITING ARCHIVE",
                background=BACKGROUNDS[("signal-a", "signal-b", "signal-c")[(number - 2) % 3]],
                language="html",
            )
        )

    for kind in ("page", "project", "category", "tag", "post"):
        directory = CONTENT / ("pages" if kind == "page" else f"{kind}s" if kind in {"project", "post"} else kind)
        cards.extend(content_card(path, kind) for path in sorted(directory.glob("*.md")))

    cards.sort(key=lambda item: str(item["url"]))
    ids = [str(item["id"]) for item in cards]
    urls = [str(item["url"]) for item in cards]
    if len(ids) != len(set(ids)):
        raise SystemExit("HOWL manifest generation produced duplicate card IDs.")
    if len(urls) != len(set(urls)):
        raise SystemExit("HOWL manifest generation produced duplicate route URLs.")
    return {
        "project": {
            "name": "RobertDeVore.com",
            "tagline": "Systems, tools, and writing for work that has to hold up.",
            "url": "https://robertdevore.com",
        },
        "theme": {"name": "signal", "mode": "light"},
        "cards": cards,
    }


def write_manifest() -> int:
    manifest = build_manifest()
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Synced {len(manifest['cards'])} HOWL card definitions.")
    return len(manifest["cards"])


if __name__ == "__main__":
    write_manifest()
