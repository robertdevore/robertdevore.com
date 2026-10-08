# Courses page SEO + AI-search / Howl audit

**PASS WITH RECOMMENDATIONS · 2026-10-08**

Scope: https://robertdevore.com/courses/, its five course destinations, sitewide inbound discovery links, and shared hosting/discovery behavior. This is a page-scoped audit, not a claim that every historical article was audited.

The published catalog already had crawlable HTML, unique metadata, one H1, a matching canonical, sitemap inclusion, direct navigation links, and working destinations. The immutable baseline showed one factual schema error: the catalog was labeled BlogPosting. Its social image also had a generic CONNECT label and a truncated subtitle.

Commit **925401c** changes the page type to CollectionPage and derives an ItemList of five Course entries from the visible cards. Release validation now checks every structured name, URL, description and position against the rendered catalog. Howl regenerated a 1200×630 social preview with a COURSES label and complete subtitle. Course copy, destinations, layout and crawler policy are unchanged.

Full CI build, site validation, homepage validation, HTML validation and deployment succeeded in [run 37783562143](https://github.com/robertdevore/robertdevore.com/actions/runs/37783562143). Independent live checks verified the new schema and exact published PNG hash. Local integration validation covered 170 primary HTML routes with zero warnings. The baseline hash seal and visible main-content hash remain unchanged.

| Measure | Before | After |
| --- | --- | --- |
| Scoped canonical / indexable pages | 1 / 1 | 1 / 1 |
| P0 / P1 root causes | 0 / 0 | 0 / 0 |
| Wrong page-type root causes (P2) | 1 | 0 |
| Missing/duplicate metadata, missing canonical, H1 count problems | 0 | 0 |
| Broken internal links / proven broken course destinations | 0 / 0 | 0 / 0 |
| Orphans / depth above three clicks | 0 / 0 | 0 / 0 |
| Missing image alt/dimensions / broken observed media | 0 / 0 | 0 / 0 |
| JSON-LD parse errors | 0 | 0 |
| Structured visible course entries | 0 | 5 |
| Truncated course social subtitle | Yes | No |

All five course destinations returned HTTP 200. Canonical HTTP/www variants redirected permanently in one hop; a nonexistent nested path returned 404. Seven crawler-user-agent probes returned 200 and robots allowed access. These are workstation probes, not proof of real crawler-IP access or indexing. The non-slash alias is served with the preferred slash canonical.

Search Console, Bing account data, rankings, traffic, conversions, backlinks, field CWV and controlled AI-answer citations are **NOT AVAILABLE — DATA ACCESS REQUIRED**. No improvement in rankings, traffic or citations is claimed. No internal SEO/AI readiness score was assigned; available evidence does not justify a comparable platform-wide score. Lighthouse measurements are separate lab diagnostics, recorded in performance.csv and raw receipts.

Remaining recommendations: use the dated 7/28/60/90-day plan in recommendations.md to measure indexing, searches, citations and user experience. Validate suspected production performance costs with field data and repeated comparable runs before changing Cloudflare/analytics/security settings. See unresolved.md for limits; no new external settings were changed.

Evidence: baseline.csv / after.csv; baseline-summary.json / after-summary.json; before/sha256.json; before/live/requests.json / after-live/requests.json; issues.csv; howl-verification.json; receipts/production-verification.json. Build/toolchain provenance and repeat commands are in methodology.md.
