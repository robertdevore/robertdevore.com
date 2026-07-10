# Verification record

## Passing checks

- `npm run build && npm run lint && npm run snapshot` in SiteKit — 85 components validated; snapshot generated.
- `KUJO_BIN=... bash scripts/run_ci_checks.sh` in Kujo SSG — CLI contracts, generated contracts, build, HTML validation, and custom-collection `llms.txt` coverage passed.
- `./scripts/build.sh` — 138 posts, 12 pages, custom collections, and auxiliary outputs generated in about 10 seconds.
- `bash .../ssg/scripts/validate-generated-output.sh output` — 388 HTML files checked; passed.
- `python3 scripts/validate_site.py output` — 195 primary routes checked; titles, descriptions, canonicals, one-H1 structure, unique IDs, alt attributes, JSON-LD, assets, required routes, article taxonomy/related-reading contracts, project landing pages, contact form, footer, and `llms.txt` collection coverage validated; passed with 73 historical-link warnings.
- Browser QA at 1440px and 375–390px — homepage, representative article, category archive, project landing page, about, and contact rendered with one H1, a main landmark, and no horizontal overflow. It also verified the sticky translucent header, centered/outlined home hero, separator removal, three-card related reading, two-column archive alignment, heading-rule removal, responsive contact form, white footer, and mobile stacking.

## Representative coverage

Verified routes include homepage, writing and pagination, root-level article, long/code-heavy articles, projects listing/item, about, contact, category/tag archives, legacy service route, 404, feed, sitemap, robots, and llms.txt. The generated `llms.txt` now includes the Projects collection index and all six project URLs. Source CSS includes 64rem, 48rem, reduced-motion, forced-colors, and print paths. The mobile navigation is native HTML and remains functional without JavaScript.

## Known limitations and human review

- 73 links inside historical articles point to old project, tag, chapter, recommendation, `/wp-content/`, or image routes that were already absent from the current public inventory. They are preserved and reported, not fabricated.
- Ten retained legacy/service pages contain claims that need Robert's review before they should be treated as current.
- Historical media is intentionally preserved and dominates repository size. A later editorial pass can retire or recompress individual assets without changing routes.
- The supplied article concept was used as direction, not copied pixel-for-pixel.
