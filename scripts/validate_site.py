#!/usr/bin/env python3
"""Repository-specific release checks for generated RobertDeVore.com output."""
from __future__ import annotations
import json, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

root = Path(sys.argv[1] if len(sys.argv) > 1 else "output").resolve()
errors, warnings, titles, descriptions = [], [], {}, {}
html_files = sorted(root.rglob("index.html")) + [root / "404.html"]
all_html_files = sorted(root.rglob("*.html"))
release_version = (Path(__file__).resolve().parents[1] / "VERSION").read_text().strip()
canonical_urls = set()

def route_exists(path: str) -> bool:
    clean = path.split("?", 1)[0].split("#", 1)[0]
    if clean in {"", "/"}: return (root / "index.html").exists()
    candidate = root / clean.lstrip("/")
    return candidate.is_file() or (candidate / "index.html").exists()

for path in html_files:
    soup = BeautifulSoup(path.read_text(errors="ignore"), "html.parser")
    rel = path.relative_to(root)
    if soup.find(string=re.compile(r"\{\{(?:home_path|relative_path)\}\}")): errors.append(f"{rel}: unresolved layout placeholder")
    if not soup.select_one("#main-content"): errors.append(f"{rel}: missing #main-content")
    h1s = soup.find_all("h1")
    if len(h1s) != 1: errors.append(f"{rel}: expected one h1, found {len(h1s)}")
    title = soup.title.get_text(strip=True) if soup.title else ""
    desc = soup.find("meta", attrs={"name": "description"})
    canonical = soup.find("link", rel="canonical")
    if not title: errors.append(f"{rel}: missing title")
    if not desc or not desc.get("content", "").strip(): errors.append(f"{rel}: missing description")
    if path.name != "404.html" and not canonical: errors.append(f"{rel}: missing canonical")
    if canonical and path.name != "404.html": canonical_urls.add(canonical.get("href", ""))
    titles.setdefault(title, []).append(str(rel))
    if desc: descriptions.setdefault(desc.get("content", ""), []).append(str(rel))
    ids = [x["id"] for x in soup.select("[id]")]
    if len(ids) != len(set(ids)): errors.append(f"{rel}: duplicate id")
    for image in soup.find_all("img"):
        if "alt" not in image.attrs: errors.append(f"{rel}: image without alt")
    if soup.select_one("div[aria-label]"):
        errors.append(f"{rel}: generic div uses aria-label without an allowed role")
    critical_css = soup.select_one("style[data-critical-css]")
    stylesheet_preload = soup.select_one('link[rel="preload"][as="style"]')
    if not critical_css or "build:critical-css" in critical_css.get_text():
        errors.append(f"{rel}: generated critical CSS is missing")
    if not stylesheet_preload or f"assets/css/site.bundle.css?v={release_version}" not in stylesheet_preload.get("href", ""):
        errors.append(f"{rel}: expected the async v{release_version} stylesheet bundle")
    hero = soup.select_one(".signal-hero")
    if hero:
        hero_image = hero.select_one("picture.signal-hero__field > img")
        hero_source = hero.select_one('picture.signal-hero__field > source[media="(max-width: 48rem)"]')
        if not hero_image or not hero_source:
            errors.append(f"{rel}: hero art is not discoverable picture markup")
        elif (
            hero_image.get("loading") != "eager"
            or not hero_image.get("width")
            or not hero_image.get("height")
            or f"?v={release_version}" not in hero_image.get("src", "")
            or f"?v={release_version}" not in hero_source.get("srcset", "")
        ):
            errors.append(f"{rel}: hero LCP image lacks eager intrinsic dimensions")
        if hero.select_one("picture[aria-hidden]"):
            errors.append(f"{rel}: decorative picture uses validator-incompatible aria-hidden")
        if hero_source and (hero_source.has_attr("width") or hero_source.has_attr("height")):
            errors.append(f"{rel}: responsive source uses validator-incompatible dimensions")
        if hero_image and hero_image.has_attr("fetchpriority"):
            errors.append(f"{rel}: hero image uses validator-incompatible fetchpriority")
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try: json.loads(script.string or "")
        except json.JSONDecodeError: errors.append(f"{rel}: invalid JSON-LD")
    for element, attr in (("a", "href"), ("img", "src"), ("script", "src"), ("link", "href"), ("video", "src"), ("source", "src")):
        for node in soup.find_all(element):
            url = node.get(attr)
            if not url or url.startswith(("#", "mailto:", "tel:", "data:", "javascript:")): continue
            parsed = urlparse(url)
            if parsed.scheme in {"http", "https"}: continue
            if url.startswith("/") and not route_exists(url):
                target = url.split("?", 1)[0].split("#", 1)[0]
                if target.startswith(("/wp-content/", "/recommends/")): warnings.append(f"{rel}: retained historical external path {target}")
                else: warnings.append(f"{rel}: missing historical internal target {target}")

    article_content = soup.select_one(".article-content")
    if article_content:
        previous_level = 1
        for heading in article_content.find_all(re.compile(r"^h[2-6]$")):
            level = int(heading.name[1])
            if level > previous_level + 1:
                errors.append(
                    f"{rel}: heading level jumps from h{previous_level} to h{level} at {heading.get_text(' ', strip=True)}"
                )
            previous_level = level
        if any(h.get_text(" ", strip=True).lower() == "continue reading" for h in article_content.find_all(["h2", "h3"])):
            errors.append(f"{rel}: obsolete Continue reading section")
        first_block = article_content.find(recursive=False)
        first_links = first_block.select('a[href^="/category/"], a[href^="/tag/"]') if first_block else []
        if first_block and first_block.name == "p" and first_links and len(first_links) == len(first_block.find_all("a")):
            errors.append(f"{rel}: duplicate taxonomy row at start of article content")
        related = next((h for h in article_content.find_all("h2") if h.get_text(" ", strip=True) == "Related Reading"), None)
        related_links = related.find_next_sibling("ul").find_all("a") if related and related.find_next_sibling("ul") else []
        if len(related_links) != 3: errors.append(f"{rel}: expected three Related Reading links, found {len(related_links)}")

    if soup.select_one(".project-page"):
        if len(soup.select(".project-landing h2")) < 3: errors.append(f"{rel}: project landing page lacks substantive sections")
        if not soup.select_one('.project-landing a[href^="https://github.com/kujolang/"]'):
            errors.append(f"{rel}: project landing page missing Kujo GitHub link")

for value, paths in titles.items():
    if value and len(paths) > 1 and not all("/page/" in p or p.startswith("page/") for p in paths): warnings.append(f"duplicate title: {value} ({len(paths)})")

for path in sorted(root.rglob("*.css")):
    rel = path.relative_to(root)
    for raw_url in re.findall(r"url\(([^)]+)\)", path.read_text(errors="ignore")):
        url = raw_url.strip().strip("\"'")
        if not url or url.startswith(("data:", "http:", "https:", "#")): continue
        clean_url = url.split("?", 1)[0].split("#", 1)[0]
        target = (root / clean_url.lstrip("/")).resolve() if clean_url.startswith("/") else (path.parent / clean_url).resolve()
        if not target.is_relative_to(root) or not target.exists():
            errors.append(f"{rel}: missing CSS asset {url}")

required = ["index.html", "blog/index.html", "page/2/index.html", "about/index.html", "contact/index.html", "projects/index.html", "category/developer-tools/index.html", "tag/engineering/index.html", "404.html", "feed/index.xml", "sitemap.xml", "robots.txt", "llms.txt"]
for item in required:
    if not (root / item).exists(): errors.append(f"missing required output: {item}")

for path in all_html_files:
    soup = BeautifulSoup(path.read_text(errors="ignore"), "html.parser")
    if not soup.title or not soup.title.get_text(strip=True):
        errors.append(f"{path.relative_to(root)}: HTML document is missing a title")

try:
    sitemap_root = ET.parse(root / "sitemap.xml").getroot()
    sitemap_urls = {
        node.text.strip()
        for node in sitemap_root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if node.text
    }
except ET.ParseError as exc:
    errors.append(f"sitemap.xml is not well formed: {exc}")
    sitemap_urls = set()
if sitemap_urls != canonical_urls:
    for url in sorted(canonical_urls - sitemap_urls):
        errors.append(f"canonical URL missing from sitemap.xml: {url}")
    for url in sorted(sitemap_urls - canonical_urls):
        errors.append(f"sitemap.xml URL lacks a matching canonical route: {url}")

try:
    feed_root = ET.parse(root / "feed/index.xml").getroot()
    atom_self = feed_root.find("./channel/{http://www.w3.org/2005/Atom}link")
    if atom_self is None or atom_self.get("rel") != "self" or atom_self.get("href") != "https://robertdevore.com/feed/index.xml":
        errors.append("feed/index.xml is missing its atom:link self-discovery URL")
except ET.ParseError as exc:
    errors.append(f"feed/index.xml is not well formed: {exc}")
feed_text = (root / "feed/index.xml").read_text(errors="ignore")
if "&amp;apos;" in feed_text or "&amp;quot;" in feed_text:
    errors.append("feed/index.xml contains double-escaped HTML entities")

robots_text = (root / "robots.txt").read_text(errors="ignore")
if "User-agent: *" not in robots_text or "Allow: /" not in robots_text or "Sitemap: https://robertdevore.com/sitemap.xml" not in robots_text:
    errors.append("robots.txt does not expose the public crawl and sitemap directives")

removed_devio_slug = "why-im-launching-devio-chat-and-letting-you-in-early"
if (root / removed_devio_slug).exists():
    errors.append("removed Devio Chat article route still exists")
for path in html_files:
    if removed_devio_slug in path.read_text(errors="ignore"):
        errors.append(f"{path.relative_to(root)}: still links to the removed Devio Chat article")
for item in ("feed/index.xml", "sitemap.xml", "llms.txt"):
    if removed_devio_slug in (root / item).read_text(errors="ignore"):
        errors.append(f"{item}: still includes the removed Devio Chat article")

home = BeautifulSoup((root / "index.html").read_text(errors="ignore"), "html.parser")
writing_label = home.select_one("#writing .section-index")
if not writing_label or writing_label.get_text(" ", strip=True) != "04 / Writing": errors.append("homepage writing label includes pagination or is missing")
footer = home.select_one(".site-footer")
if not footer or "© 1985-2026 Robert DeVore." not in footer.get_text(" ", strip=True): errors.append("footer copyright is incorrect")
for href in ("https://x.com/deviorobert", "https://github.com/robertdevore"):
    if not footer or not footer.select_one(f'a[href="{href}"]'): errors.append(f"footer missing social link {href}")

contact = BeautifulSoup((root / "contact/index.html").read_text(errors="ignore"), "html.parser")
if len(contact.select("form[data-contact-form] label")) != 5: errors.append("contact form fields are incomplete")
if contact.select_one("input[inputmode]"): errors.append("contact form uses a legacy-validator compatibility warning attribute")
if contact.select_one('.page-content a[href="https://github.com/robertdevore"]'):
    errors.append("contact content still includes the removed GitHub link")

projects = BeautifulSoup((root / "projects/index.html").read_text(errors="ignore"), "html.parser")
snips = next((article for article in projects.select(".project-secondary article") if article.find("h3") and article.find("h3").get_text(" ", strip=True) == "Snips"), None)
if not snips or "without losing the required context" not in snips.get_text(" ", strip=True):
    errors.append("projects page Snips description is incorrect")
active_system_titles = [heading.get_text(" ", strip=True) for heading in projects.select(".project-secondary h3")]
if active_system_titles != ["Strata", "Snips", "RepoRadar"]:
    errors.append(f"projects active-system titles are incorrect: {active_system_titles}")
tool_links = {link.get_text(" ", strip=True): link.get("href") for link in projects.select(".project-link-bank__columns a")}
for removed_tool in ("Repo Radar", "Agent Skills", "PlaneWatch", "AI Agents", "Learn Chess", "Content Creator", "Don't Break The Chain"):
    if removed_tool in tool_links: errors.append(f"projects tool archive still includes removed tool {removed_tool}")
for label, href in (
    ("Paperclip Goal Issues", "https://github.com/robertdevore/paperclip-goal-issues"),
    ("Paperclip Starred Issues", "https://github.com/robertdevore/paperclip-starred-issues"),
    ("HolySheet", "https://github.com/robertdevore/holy-sheet"),
    ("TreasureTrail", "https://github.com/robertdevore/treasure-trail"),
    ("LaravelCMS", "https://github.com/robertdevore/laravel-cms"),
    ("Prompts Library", "https://prompts.robertdevore.com"),
    ("Learn Python", "https://python.robertdevore.com"),
):
    if tool_links.get(label) != href: errors.append(f"projects tool archive is missing {label}")
tool_order = [link.get_text(" ", strip=True) for link in projects.select(".project-link-bank__columns a")]
if tool_order[:3] != ["Snips", "Paperclip Goal Issues", "Paperclip Starred Issues"]:
    errors.append(f"projects tool archive does not place the Paperclip tools after Snips: {tool_order[:3]}")

kujo = BeautifulSoup((root / "projects/kujo/index.html").read_text(errors="ignore"), "html.parser")
if "Kujo 1.0 is released." not in kujo.get_text(" ", strip=True):
    errors.append("Kujo project boundary does not describe the 1.0 release")
kujo_site_link = kujo.select_one('.project-landing a[href="https://kujolang.ai"]')
if not kujo_site_link or kujo_site_link.get("target") != "_blank" or set(kujo_site_link.get("rel", [])) != {"noopener", "noreferrer"}:
    errors.append("Kujo project introduction is missing the safe new-window kujolang.ai link")
for slug in ("agents-sdk", "dispatch", "kujo", "lens", "sitekit", "ssg"):
    project = BeautifulSoup((root / f"projects/{slug}/index.html").read_text(errors="ignore"), "html.parser")
    if project.select_one("main.project-page > article"):
        errors.append(f"project {slug} uses an outer article that triggers a legacy-validator heading warning")

forever_forward = BeautifulSoup((root / "forever-forward/index.html").read_text(errors="ignore"), "html.parser")
forever_og = forever_forward.select_one('meta[property="og:image"]')
forever_twitter = forever_forward.select_one('meta[name="twitter:image"]')
forever_og_url = forever_og.get("content", "") if forever_og else ""
if not forever_og_url or not forever_twitter or forever_twitter.get("content") != forever_og_url:
    errors.append("Forever Forward is missing matching Open Graph and Twitter social images")
else:
    parsed_forever_og = urlparse(forever_og_url)
    if parsed_forever_og.netloc != "robertdevore.com" or not route_exists(parsed_forever_og.path):
        errors.append(f"Forever Forward social image is not a local production asset: {forever_og_url}")

about = BeautifulSoup((root / "about/index.html").read_text(errors="ignore"), "html.parser")
if about.select_one(".tools-hero-card, .about-map, .clarity-grid"):
    errors.append("about page still includes a removed box section")
if any(heading.get_text(" ", strip=True) == "Where the work shows up" for heading in about.find_all("h2")):
    errors.append("about page still includes the removed selected-surfaces heading")
about_proof_titles = [heading.get_text(" ", strip=True) for heading in about.select(".about-proof h3")]
if about_proof_titles != ["Field Notes", "Projects", "Contact"]:
    errors.append(f"about selected surfaces are incorrect or out of order: {about_proof_titles}")
if any(not heading.has_attr("data-no-heading-anchor") for heading in about.select(".about-proof h3")):
    errors.append("about selected-surface titles do not suppress heading anchors")
if not about.select_one(".about-timeline h2") or about.select_one(".about-timeline h2").get_text(" ", strip=True) != "Through-line":
    errors.append("about timeline heading is missing")

llms = (root / "llms.txt").read_text(errors="ignore")
if "## Projects" not in llms or "[Projects index](https://robertdevore.com/projects/)" not in llms:
    errors.append("llms.txt missing Projects collection")
for slug in ("agents-sdk", "dispatch", "kujo", "lens", "sitekit", "ssg"):
    if f"https://robertdevore.com/projects/{slug}/" not in llms: errors.append(f"llms.txt missing project {slug}")

site_css = (root / "assets/css/site.bundle.css").read_text(errors="ignore")
if "paint-order:" in site_css: errors.append("site CSS contains paint-order, which fails the Nu HTML/CSS checker")
if "@layer" in site_css: errors.append("site CSS contains cascade layers that would lose to the inline compatibility shell")
critical_source = (root / "assets/css/site.critical.css").read_text(errors="ignore")
for unsupported in ("@layer", "paint-order:", "translate:", "var(", "clamp(", "color-mix("):
    if unsupported in critical_source:
        errors.append(f"critical CSS contains HTML5-validator-incompatible syntax: {unsupported}")
for contract in ("-webkit-text-stroke:8px", ".home-page .section-heading", ".site-header{position:sticky", ".article-related-grid", ".about-page .page-content h2", ".contact-page .page-content h2", ".site-footer{border:0"):
    if contract not in site_css: errors.append(f"site CSS missing requested contract {contract}")
home_title_rule = re.search(r"\.home-page>\.signal-hero \.signal-title\{([^}]*)\}", site_css)
if not home_title_rule or "-webkit-text-stroke" in home_title_rule.group(1):
    errors.append("homepage hero title applies its stroke inside the live text fill")
if ".home-page>.signal-hero .signal-title::before{content:attr(data-text);position:absolute;z-index:-1;inset:0;color:transparent;-webkit-text-stroke:8px" not in site_css:
    errors.append("homepage hero title is missing its outside-only stroke layer")
for contract in (".leap-callout{max-inline-size:93ch", "font-size:1rem;text-align:center}", ".home-closing{position:relative;isolation:isolate;overflow:hidden}", ".timeline-list{inline-size:100%;max-inline-size:none", ".timeline-list li{max-inline-size:none", ".archive-list{max-inline-size:var(--sk-size-content-xl)}", ".archive-list li{max-inline-size:none", ".project-link-bank__eyebrow{color:var(--sk-color-gray-200)}", ".article-related-grid,.project-feature__panel,.project-secondary__grid,.project-landing ul"):
    if contract not in site_css: errors.append(f"site CSS missing current review contract {contract}")

print(f"Validated {len(html_files)} primary HTML routes")
print(f"Warnings: {len(warnings)}")
for warning in warnings[:20]: print(f"WARN {warning}")
if errors:
    for error in errors[:100]: print(f"ERROR {error}")
    raise SystemExit(1)
print("Site validation passed")
