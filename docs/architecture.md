# Architecture and implementation record

## Repository audit

The target repository previously tracked generated Stattic output rather than authoring sources: 138 public posts, 12 listed pages, two additional public directories, 28 pagination pages, and roughly 1 GB of duplicated media variants. There was no source build configuration. The replacement is a source-first Kujo SSG project. `output/` is generated and ignored.

The previous site exposed stale or unverifiable 2025 availability, response-time and timeline promises, revenue/user/project metrics, certifications, testimonials, case-study results, service positioning, and an old copyright year. Those claims are not used on the new homepage, about, contact, or projects surfaces. Ten service/legacy routes remain available with a visible archival warning. Historical posts remain historical.

## Kujo SSG audit and decisions

Canonical SSG surfaces reviewed: `README.md`, `AGENTS.md`, `build.kujo`, configuration, templates, content examples, generated-output contracts, CI gate, accessibility audit, and parity audit.

The site uses the supported contracts directly:

- `content/pages`, `content/posts`, and custom collections (`projects`, `category`, `tag`)
- `layout.html`, page/listing overrides, content-type listing overrides, and per-item templates
- unified frontmatter for title, description, author, date, canonical, template, excerpt, categories, tags, draft state, ordering, and navigation visibility
- root pages, root post permalinks, blog/home pagination, custom collection routes, flat aliases, and 404 output
- canonical, Open Graph, Twitter Card, BlogPosting/WebSite JSON-LD, RSS, sitemap, robots, favicon, and llms.txt with posts, pages, and custom collections
- local asset copying, deterministic font/image handling, and output validation

Two general platform gaps were proven. Public posts needed to remain at `/<slug>/` while the writing listing remained at `/blog/`; Kujo SSG supports that through the tested `posts_at_root` change in commit `8641a71`. Custom collections were missing from `llms.txt`; the SSG now emits a deterministic section, collection-index URL, and non-draft item URLs for every built custom collection through local commit `d17ed50`. No site-specific parallel router or machine-readable index was created.

Native taxonomy archive generation is not yet an SSG feature. Archives are materialized through the supported custom-collection contract at `/category/<term>/` and `/tag/<term>/`. The migration script regenerates them from canonical post frontmatter.

## SiteKit audit and reuse map

SiteKit's generated design guide, tokens, Kujo Light theme, standards, personal/blog layouts, schemas, templates, and CSS were reviewed. Departure Mono ships as regular WOFF2 (22 KB) and WOFF (25 KB), uses `font-display: swap`, and retains the documented monospace fallback stack.

| SiteKit primitive | Site use | Decision |
| --- | --- | --- |
| tokens + Kujo Light | color, type, spacing, borders, focus, motion | direct compiled distribution |
| skip link | global shell | direct |
| header + navigation | global desktop/mobile shell | semantic site composition using component classes |
| footer | global shell | direct composition |
| button | homepage/contact/404 actions | direct |
| card + grid | focus areas and project surfaces | direct |
| breadcrumbs | article and project heroes | direct |
| metadata panel | article metadata | direct |
| table, code block, quote | long-form content | component CSS plus progressive enhancement |
| alert | archived legacy warning | semantic Markdown quote styled as a warning surface |
| pagination | SSG-generated listings | SSG markup styled with SiteKit tokens |

No SiteKit source changes were needed. Compiled distribution assets are synced rather than copying component source into the theme. Their source revisions and hashes are locked in `workspace-dependencies.json`; `scripts/sync_dependencies.sh` performs the portable, atomic sync and `scripts/workspace.py doctor` verifies provenance. RobertDeVore.com-specific artwork, composition, crops, motion, and editorial rhythm stay in `assets/css/site.css` and site templates.

## Information architecture and templates

Primary navigation is Writing, Projects, About, Contact. Machine-readable and secondary routes are in the footer. Category/tag archives and retained legacy pages remain reachable without inflating primary navigation.

| Content | Template/routes |
| --- | --- |
| homepage + pagination | `page-home.html`, `/`, `/page/N/` |
| writing + pagination | `page-blog.html`, `/blog/`, `/blog/page/N/` |
| article variants | `post-signal-a/b/c.html`, retained root permalink |
| standard/about/contact/legacy | page templates at their retained routes |
| projects | custom collection listing + project item template |
| category/tag | custom collection listing + archive item template |
| errors | `404.html` |

## Design system

The art direction is systems editorial design with controlled digital decay. Order remains dominant: white canvas, black/gray structure, thin rules, generous space, narrow reading measure, SiteKit tokens, and Departure Mono throughout. Red is restricted to small signal labels, active markers, and acquisition residue.

Three supplied fragmentation works form the background system. Each has a 1920px WebP (92–128 KB), a 720px mobile WebP (24–25 KB), and the original PNG fallback. A/B/C variants use different focal positions and mobile crops across home, writing, article, page, project, and error heroes. The centered homepage hero shows the source art without a left or lower fade and uses a 3px white letter stroke instead of a faded title panel.

Signal-acquisition motion uses two CSS pseudo-layers for 640–720 ms, runs once, does not replace the real heading, causes no layout shift, and is removed under `prefers-reduced-motion`. The site remains navigable and readable without JavaScript. JavaScript adds current-page state, heading anchors/TOC, accessible copy-code controls, related-reading card enhancement, and a privacy-preserving mailto draft for the contact form.

## Content migration and routes

`scripts/migrate_legacy.py` parses the previous llms.txt/sitemap and rendered HTML, converts article bodies to Markdown, normalizes frontmatter, preserves 138 post routes, creates three related-reading links, and materializes category/tag archives. Category and tag metadata remains in article heroes; the redundant body taxonomy row and previous/next “Continue reading” section are intentionally omitted. The route-by-route record is [content-migration.csv](content-migration.csv).

All 138 listed post URLs remain unchanged. The current homepage, blog, about, contact, free tools, seven service routes, portfolio, and unlisted `contact-new` route remain available. No route required a redirect. Old generated pagination routes continue through Kujo SSG. Historical broken project/tag/media/recommendation links are reported as warnings rather than silently rewritten.

## Accessibility, performance, and operations

The shell uses landmarks, one page-level H1, skip link, native `<details>` mobile navigation, visible focus, large targets, semantic lists/tables, image alt validation, reduced motion, forced-color fallback, print styles, and no-JavaScript navigation/content. Heading anchors, TOC, and copy controls are progressive enhancements.

Current authored payloads: site CSS 22,926 bytes, site JS 4,723 bytes, Departure Mono WOFF2 22,496 bytes, and each desktop hero 93–128 KB. Legacy article media totals 195 MB in the repository/output but loads only when referenced by an individual historical article; it is never globally requested. No framework, animation library, tracking script, or third-party font request was added.

Deployment assumption: a static host publishes `output/` at `https://robertdevore.com`. No production deployment was performed.

For local operations, the Kujo runtime and SSG/SiteKit source paths are resolved from the project-local dependency manifest rather than a developer-specific absolute path. The validator's Python dependency is declared in `requirements.txt`. See [dependencies.md](dependencies.md) for the sync and doctor contracts.
