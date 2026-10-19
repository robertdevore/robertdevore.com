# Courses page addition — 2026-10-19

Scope: targeted page edit and SEO/AI-search regression review, not a new full-site audit. Add Edge Academy to the existing catalog and preserve the other five courses. No crawler policy, infrastructure, or dependency changes.

## Evidence and approach

The untouched production HTML, source files, commit and HTTP headers are in `before/`. Edge Academy's fetched homepage grounds the description: customer engineering, networking, security, Cloudflare architecture, troubleshooting labs, flashcards and mock interviews. Preserve its independent/non-affiliation context. The destination was read directly over HTTPS because the search browser could not fetch it.

Delivery: authored Markdown/template → vendored Kujo SSG → generated HTML hardening (CollectionPage with ItemList/Course entries from visible cards) → GitHub Actions (checksum-verified Kujo 1.0.1 release) → GitHub Pages. Output is excluded from Git. HOWL manifest generation derives captions from page metadata and its tagline from the page-description mapping; committed SVG/PNG previews are regenerated separately.

## Current primary guidance (retrieved 2026-10-19)

- https://developers.google.com/search/docs/appearance/ai-features — documented recommendation: retain discoverable textual content and visible-content-aligned structured data; no special AI schema or AI files are required.
- https://developers.google.com/search/docs/crawling-indexing/links-crawlable — documented recommendation: use an anchor with a real href and meaningful contextual link text.
- https://developers.google.com/search/docs/fundamentals/using-gen-ai-content — documented recommendation: check factual accuracy in content and metadata.

Application: add a server-rendered card with a descriptive link, update the visible count and description, let the existing generator derive matching structured data, and refresh the HOWL social preview. No ranking, citation, affiliation or certification claims are added.

## Measurement limits

Search Console, analytics, rankings, AI citations, CDN logs and field Core Web Vitals: NOT AVAILABLE — DATA ACCESS REQUIRED. No visibility improvement is claimed. Sitewide scoring, external-link crawling and performance benchmarking are outside this single-page change. At 7/28/60/90 days, an owner with platform access can compare the same Courses URL's index state, impressions/clicks and Edge Academy referrals; comparisons do not establish causality.

## Toolchain and baseline verification

The documented local wrapper rejected the installed runtime checkout because it differs from the manifest pin. An isolated source build of that pin was stopped when temporary compiler output consumed scarce disk space; that temporary target was removed. No dependency pins were changed. The baseline instead completed with the checksum-verified macOS x64 Kujo 1.0.1 release used by the CI workflow on Linux. This is deployment-toolchain validation, not a successful `scripts/build.sh` run. The full baseline validator checked 170 primary routes with zero warnings; the homepage contract passed.

Before changing the Courses source, its generated raw HTML and production baseline were saved. The baseline full-site build subsequently completed; `before/generated.html` and `before/summary.json` contain the hardened five-course catalog. The existing five cards remain unchanged in the source diff. The after build is performed independently by the normal deployment workflow.

HOWL: all 170 manifest entries validate. A full raster rendering run encountered a local write error during disk pressure; unrelated regenerated PNGs were restored. A targeted one-card render using the same renderer completed successfully for Courses. The 1200×630 PNG was visually inspected; its SVG retains the branded source. Only Courses assets changed.

## Separate dependency review

GitHub reports two open high-severity CairoSVG alerts in requirements.txt. Alert #1 was already captured in SignalBox and was not duplicated. Alert #2 (quadratic SVG path parsing DoS) is recorded as capture `cap_f65594b8-4335-4784-9d47-a946f40c4af3` and signal `sig_ae952e9d-0837-4144-a7b7-19b18634188c`; both passed exact-ID and conceptual retrieval. Repository exploitability was not tested; this is a separate dependency review, not a regression introduced by the Courses change. Transient build progress and resolved rendering recovery were rejected as SignalBox captures.

## Final result: PASS (targeted page change)

Commit `0078b4184281e9a3d5654f40cbb083b87190f630` passed build, site validation, homepage checks and Nu HTML validation in deployment run https://github.com/robertdevore/robertdevore.com/actions/runs/39288829342. Deployment succeeded. Local baseline also passed those validation commands. Production Courses returns six cards, matching six structured Course entries; one H1, title and self-canonical are preserved, and description includes Edge Academy. The previous five cards remain intact. The destination, robots and sitemap are reachable through curl, sitemap contains Courses, and the live social PNG matches the committed file byte-for-byte. A Python urllib request returned 403; curl verification succeeded. No claim is made about verified search-bot access.

Reproduce the page comparison with `python3 seo-audit/2026-10-19-courses/check_courses.py <saved-html>` against before/generated.html and after/live.html. Summaries include hashes. CI job receipts and production checks are in after/. No page-change blockers remain. Separate CairoSVG dependency alerts remain for human review; no sitewide SEO-health score or search-visibility outcome is inferred.
