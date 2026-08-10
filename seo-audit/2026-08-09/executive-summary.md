# Executive summary

## Overall status

**PASS WITH RECOMMENDATIONS** — Audit date: **2026-08-09**.

The complete generated site was baselined before edits, 184 canonical sitemap pages were audited, current search/AI guidance was researched, safe fixes were implemented, and the final 173-page canonical artifact was rebuilt and re-audited. The page count fell by 11 intentionally because `/page/2/`–`/page/12/` were duplicate homepage copies, not unique content. All 138 authored post URLs remain.

Internal SEO health improved from **67/100 to 92/100**. Internal AI Search Readiness improved from **66/100 to 82/100**. These are documented trend heuristics, not Google or AI-platform scores. P0 critical findings remained **0 → 0**; P1 affected-page findings moved **19 → 1** at audit completion and **1 → 0** after the 2026-08-10 hostname fix. See `post-audit-fixes.md`.

## Where the site was

The baseline had complete titles, descriptions, canonicals, H1s, sitemap membership, permissive crawler access, and parseable JSON-LD. It also had 11 indexable duplicate pagination pages, 26 duplicate-title pages, 29 duplicate-description pages, 18 orphans, 64 broken internal-link instances to 28 destinations, 459 missing image-dimension occurrences, eight missing/corrupt linked images, generic meta keywords on all 184 pages, inappropriate schema types, and layout instability from async CSS replacement plus automatic hero-title scrambling.

The public search sample found the homepage first for an exact branded query, but its cached description reflected the previous production experience. The audited domain was not observed for the sampled Kujo, agent tooling, workflow-orchestration, WordPress security, image accessibility, or Python tutorial queries. This is a limited dated sample, not a universal ranking report.

## What changed

- Removed the 11 duplicate root pagination routes from output and sitemap while preserving canonical blog pagination.
- Eliminated all observed internal broken links and all 18 orphans through factual link updates/removals and new project/taxonomy navigation.
- Made archive/collection metadata unique, removed legacy keywords, and corrected image-less Twitter cards.
- Rebuilt structured data around factual page types and Robert DeVore as a `Person`; all 173 canonical pages have parseable page-appropriate JSON-LD.
- Added intrinsic dimensions and non-hero loading hints, removed eight broken/corrupt media references, and removed six dead current-project repository links.
- Stabilized rendering by loading the full stylesheet before paint and excluding the primary hero heading from automatic scramble animation.
- Added build failures for the newly enforced metadata, route, project-link, card, and media contracts.
- Preserved a reproducible crawler and permanent CSV/JSON/Markdown audit record for future comparisons.

## Where the generated site is now

The final crawl found zero missing/duplicate titles or descriptions, zero missing canonicals, zero broken internal links, zero orphans, zero missing H1s/multiple H1s, zero missing alt attributes, zero missing image dimensions, zero broken images, zero JSON-LD parse/type errors, and zero accidental noindex pages. Eight older/pagination destinations remain four clicks deep.

Representative Lighthouse lab runs improved from **70 → 90** performance with **CLS 0.507 → 0.004** on the homepage and **61 → 82** with **CLS 0.259 → 0.003** on the media-rich article. Lighthouse SEO remained 100 for both templates. These single local lab runs do not replace production CrUX/RUM; field LCP, INP, and CLS remain unavailable.

## What can and cannot be measured

Production apex, robots, sitemap, and `llms.txt` returned 200. Googlebot, Bingbot, OAI-SearchBot, GPTBot, PerplexityBot, and Perplexity-User all received 200 under the current `Allow: /` policy. `https://www.robertdevore.com/` returned Cloudflare 521 during the audit; the stale DNS origin and redirect path were corrected and verified on 2026-08-10.

Google Search Console, its Generative AI performance report, Bing Webmaster Tools, analytics/server logs, CrUX/RUM, and independent AI-answer platform sessions were **NOT AVAILABLE — DATA ACCESS REQUIRED**. Therefore clicks, impressions, CTR, positions, index coverage, conversions, referrals, AI citations, citation order, and field Core Web Vitals were not invented or inferred. The 15-question AI benchmark is preserved for controlled future runs.

## Highest-value next actions

1. Inspect sitemap/canonicals and key project routes in Search Console and Bing Webmaster Tools.
2. Grant read access to search/analytics/log/CWV data and repeat the documented 7-, 28-, 60-, and 90-day comparisons.
3. Manually review the 153 observed failing external-link instances across 106 historical destinations; do not mass-substitute citations.
4. Publish first-hand, maintained Kujo/entity/adoption and workflow implementation guides where real evidence exists, then repeat the search and AI benchmarks.

Detailed evidence and every row-level finding are in this directory; implementation specifics are in `changes.md`, comparison metrics in `before-after.md`, blockers in `unresolved.md`, and the measurement/content roadmap in `recommendations.md`.
