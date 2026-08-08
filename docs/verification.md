# Verification record

## Passing checks

- `npm run build && npm run lint && npm run snapshot` in SiteKit — 85 components validated; snapshot generated.
- `KUJO_BIN=... bash scripts/run_ci_checks.sh` in Kujo SSG — CLI contracts, generated contracts, build, HTML validation, and custom-collection `llms.txt` coverage passed.
- `./scripts/build.sh` — 137 posts, two pages, custom collections, redirects, and auxiliary outputs generated with the pinned Kujo runtime.
- `python3 scripts/validate_site.py output` — 184 primary routes checked; titles, descriptions, canonicals, sitemap parity, RSS self-discovery, robots directives, heading order, one-H1 structure, unique IDs, alt attributes, JSON-LD, assets, article taxonomy/related-reading contracts, project landing pages, contact form, footer, and `llms.txt` collection coverage validated; passed with 77 preserved historical-link warnings.
- `npx --yes vnu-jar@26.8.6 --format json --stdout --skip-non-html output` — all 366 generated HTML documents passed the pinned Nu Html Checker with zero errors, warnings, or informational findings; `./scripts/validate_html.sh output` enforces the error-level release gate.
- `python3 scripts/run_visual_receipt.py` — QA-001 passed all nine representative routes at desktop and mobile viewports with no error-level findings.
- Browser QA at 1440px and 375–390px — homepage, representative article, category archive, project landing page, about, and contact rendered with one H1, a main landmark, and no horizontal overflow. It also verified the sticky translucent header, centered/outlined home hero, separator removal, three-card related reading, two-column archive alignment, heading-rule removal, responsive contact form, white footer, and mobile stacking.

## Representative coverage

Verified routes include homepage, writing and pagination, root-level article, long/code-heavy articles, projects listing/item, about, contact, category/tag archives, legacy service route, 404, feed, sitemap, robots, and llms.txt. The generated `llms.txt` now includes the Projects collection index and all six project URLs. Source CSS includes 64rem, 48rem, reduced-motion, forced-colors, and print paths. The mobile navigation is native HTML and remains functional without JavaScript.

## Local visual/a11y receipt (QA-001)

The versioned coverage contract is [`qa/lens/routes.json`](../qa/lens/routes.json). It covers the home page, a long post, an archive, a project, contact, and the generated 404 page at Lens desktop (1440x900) and mobile (390x844) viewports. The 404 visual check targets the generated `/404.html` document, while its receipt also proves the local missing-route fallback returns HTTP 404 and expected text. Each route has a small deterministic browser assertion spec under `qa/lens/specs/`.

Run the receipt locally after installing Lens and its Chromium bridge. `LENS_BIN` must point to the Lens executable when it is not already on `PATH`:

```bash
LENS_BIN=/path/to/lens/lens python3 scripts/run_visual_receipt.py
```

The command rebuilds the static output, serves it only on an available `127.0.0.1` port with the generated `output/404.html` fallback, then runs Lens with axe WCAG 2 A/AA checks, same-origin link checks, and the two fixed viewports. Use `--port 4173` when a fixed port is required. Artifacts stay untracked in `.lens/runs/qa-001-<UTC timestamp>/`: each route contains `lens-report.md`, `lens-report.json`, `accessibility.json`, desktop/mobile screenshots, and an HTML report; the top-level `receipt.json` records the manifest hash, routes, artifact presence, and exit codes. A zero exit code means every route passed at the configured `error` threshold. The expected intentional 404 response may appear as a warning in that route's network evidence; it is not a failing 5xx response.

## Known limitations and human review

- 73 links inside historical articles point to old project, tag, chapter, recommendation, `/wp-content/`, or image routes that were already absent from the current public inventory. They are preserved and reported, not fabricated.
- Ten retained legacy/service pages contain claims that need Robert's review before they should be treated as current.
- Historical media is intentionally preserved and dominates repository size. A later editorial pass can retire or recompress individual assets without changing routes.
- The supplied article concept was used as direction, not copied pixel-for-pixel.
