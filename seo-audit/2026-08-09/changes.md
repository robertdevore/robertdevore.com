# Implemented changes

Audit date: 2026-08-09.

## Crawl, indexation, and architecture

- Removed 11 identical root `/page/2/`–`/page/12/` homepage copies from the final artifact and sitemap while preserving canonical `/blog/page/N/` archives.
- Added discoverable links from the project index to all five previously orphaned project detail pages and from the writing index to category/tag indexes.
- Updated or removed verified stale internal project, tag, article, image, chapter, recommendation, and media references. Internal broken-link instances fell from 64 to zero without inventing replacement content.
- Extended the generated-site validator so duplicate root pagination, missing project links, stale meta keywords, invalid card selection, and missing image dimensions fail the build.

## Metadata and result presentation

- Generated unique titles and descriptions for blog pagination, category/tag archives, and collection indexes.
- Removed generic `SSG, Static Site Generator` meta keywords from all 184 baseline pages.
- Changed Twitter cards without an image from `summary_large_image` to `summary`; preserved real image cards where present.
- Kept canonical, Open Graph, RSS, sitemap, robots, and language signals aligned.

## Structured data and entity clarity

- Replaced generic `WebSite` markup on listings and incorrect `BlogPosting` markup on project records with page-purpose types: `WebSite`, `Person`, `CollectionPage`, `AboutPage`, `ContactPage`, `BlogPosting`, `SoftwareSourceCode`, and visible `BreadcrumbList` where available.
- Represented Robert DeVore as a `Person` author/publisher with factual GitHub/X identity links, and added project repository URLs only when visible on the page.
- Kept claims limited to visible content; no ratings, reviews, awards, FAQs, or organizational claims were invented.

## Media and performance

- Added intrinsic width/height to 440 linked generated image occurrences (459 page-image occurrences were missing dimensions in the baseline inventory), plus lazy loading and asynchronous decoding outside the hero.
- Removed eight missing, empty, or corrupt historical image references while preserving surrounding article meaning.
- Made the complete stylesheet render-blocking to prevent the critical/full CSS layout swap found by Lighthouse.
- Excluded primary hero headings from automatic scramble animation so the largest viewport heading no longer disappears/reflows during initial rendering.
- Bumped the site release to 1.0.6 and regenerated the CSS artifacts so changed CSS/JavaScript URLs invalidate existing browser/CDN caches.
- Removed six dead current-project GitHub links rather than sending users or crawlers to confirmed 404s.

## Content integrity

- Preserved all 138 authored post URLs and all intended pages/projects.
- Reworded only narrow passages needed to remove missing chapter/screenshot references or accurately label a 2015 hosting promotion as historical and possibly expired.
- Left ambiguous third-party historical citations in place for human review rather than silently substituting unrelated sources.

## Audit tooling and dependencies

- Added a reproducible whole-site audit crawler/dataset generator (`scripts/seo_audit.py`).
- Declared the pinned Pillow dependency used for corrupt-image verification and intrinsic dimensions.
- Added permanent baseline/after inventories, link/schema/media/performance datasets, search and AI benchmarks, crawler evidence, research sources, scoring methodology, unresolved work, and comparison guidance under this dated directory.
