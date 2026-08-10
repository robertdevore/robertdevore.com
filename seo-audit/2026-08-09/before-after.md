# Before and after

Audit date: 2026-08-09. “After” means the final generated repository artifact. Search/indexing outcomes require deployment and elapsed time.

| Metric | Before | After | Change |
| --- | ---: | ---: | ---: |
| Canonical sitemap HTML pages audited | 184 | 173 | 11 duplicate homepage pagination routes removed intentionally |
| Indexable canonical pages | 184 | 173 | 11 duplicates removed; no intended content page lost |
| Missing titles | 0 | 0 | 0 |
| Duplicate-title pages | 26 | 0 | -26 |
| Missing descriptions | 0 | 0 | 0 |
| Duplicate-description pages | 29 | 0 | -29 |
| Missing canonicals | 0 | 0 | 0 |
| Broken internal link instances | 64 | 0 | -64 |
| Unique broken internal destinations | 28 | 0 | -28 |
| Observed broken external link instances | 159 | 153 | -6; 153 historical instances remain for editorial verification |
| Unique observed broken external destinations | 112 | 106 | -6 |
| Orphan pages | 18 | 0 | -18 |
| Pages more than three clicks deep | 9 | 8 | -1 |
| Missing H1 | 0 | 0 | 0 |
| Multiple H1 | 0 | 0 | 0 |
| Images missing alt attributes | 0 | 0 | 0 |
| Images missing intrinsic dimensions | 459 | 0 | -459 |
| Broken/corrupt linked images | 8 | 0 | -8 |
| Invalid JSON-LD parses | 0 | 0 | 0 |
| Canonical pages with parseable schema | 184 | 173 | 100% both; after types match page purpose |
| Legacy meta-keyword pages | 184 | 0 | -184 |
| Sitemap duplicate-route errors | 11 | 0 | -11 |
| Accidental noindex pages | 0 | 0 | 0 |
| Redirect chains among canonical pages | 0 | 0 | 0 |
| Static meta-refresh aliases | 183 | 172 | -11 duplicate root-pagination aliases removed; retained aliases remain a host limitation |
| Search/AI crawler accessibility issues | 0 | 0 | All six tested agents received 200; policy unchanged |
| P0 critical findings | 0 | 0 | 0 |
| P1 affected-page findings | 19 | 1 | 18 orphans resolved; production `www` hostname remains |
| Internal SEO health score | 67/100 | 92/100 | +25 |
| AI Search Readiness | 66/100 | 82/100 | +16; visibility remains unmeasured |

## Representative Lighthouse 12.8.2 lab runs

The complete JSON receipts are in `lighthouse/`. The final summarized measurements are in `lighthouse-summary.csv`. The test used Lighthouse mobile defaults against local static servers; lab variation and local serving conditions apply. Real-user LCP, INP, and CLS are **NOT AVAILABLE — DATA ACCESS REQUIRED**.

The major measurable change was eliminating an async full-stylesheet swap and stopping automatic scrambling of the viewport's primary hero heading. Intrinsic image dimensions also prevent content-image reservation failures. No claim is made that field Core Web Vitals improved until production CrUX or RUM data proves it.
