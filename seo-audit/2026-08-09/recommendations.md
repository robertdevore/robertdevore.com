# Recommendations and measurement plan

## Immediate after deployment

1. Confirm the GitHub Pages workflow passes and sample production homepage, blog pagination, taxonomy indexes, all six project records, sitemap, robots, feed, `llms.txt`, and representative historical posts.
2. **Completed 2026-08-10:** corrected the `www` Cloudflare/DNS path and verified one-hop permanent redirects for all hostname/protocol variants, including nested paths and query strings.
3. Submit or inspect the sitemap in Google Search Console and Bing Webmaster Tools. Inspect the removed `/page/N/` URLs and key project URLs; request recrawl only where platform guidance supports it.
4. Connect Search Console, Bing Webmaster Tools, and privacy-appropriate analytics/log access to the next audit. Preserve the pre/post deployment date as an annotation.

## 7-day checks

- Deployment/crawl errors, sitemap fetch status, robots access, canonical selection on a small key-page sample, and whether removed duplicate pagination begins dropping from reported coverage.
- Production Lighthouse/CrUX availability and any new 4xx/5xx, especially `www`.
- OAI-SearchBot/PerplexityBot/Googlebot/Bingbot access in CDN or server logs where available.

## 28-, 60-, and 90-day comparisons

- Google Search Console: clicks, impressions, CTR, average position, query/page pairs, indexed pages, excluded-duplicate reasons, crawl stats, and Generative AI performance by page/query/country/device where the platform exposes it.
- Bing Webmaster Tools: impressions/clicks/query/page, index/crawl errors, and sitemap state.
- Analytics/logs: organic landing sessions, engaged sessions, conversions/contact actions, new vs returning, `utm_source=chatgpt.com`, perplexity.ai, copilot.microsoft.com/bing.com, gemini.google.com, and other clearly attributable AI referrals. Do not infer unseen referrals from direct traffic.
- Repeat every row in `search-rankings.csv` with the same provider/locale/device and record the full observed result/citation evidence.
- Repeat every question in `ai-search-benchmark.csv` in controlled signed-out or documented accounts; capture brand mention, site citation, exact cited URL, position, competitor sources, and factual accuracy.
- Production Core Web Vitals: p75 LCP, INP, and CLS by template/URL group; compare Lighthouse only as a diagnostic, not as field performance.

Use comparable windows, annotate major releases/search updates, and account for seasonality. Technical readiness changed immediately; ranking, traffic, and citation impact must be earned and measured over time.

## Content roadmap (editorial approval required)

1. Publish a first-hand Kujo overview that consistently defines the language, disambiguates it from Koja, links installation/docs/source, states maturity and limitations, and has a verifiable maintained date.
2. Create one evidence-rich guide for bounded/testable AI agents and one for resumable workflow orchestration, using runnable examples, artifacts, failure modes, and comparisons grounded in actual Kujo behavior.
3. Add factual comparison pages only where Robert has used or evaluated the alternatives; avoid generic “best tool” pages.
4. Review the highest-failure historical posts in `broken-links.csv` and add explicit current-status notes for products/projects that changed ownership, maintenance, or availability.
5. Decide whether WordPress security audits remain an active service. If yes, create a current intent-specific page with scope, process, deliverables, limitations, authorship, and verifiable proof. If no, keep historical articles informational and avoid commercial ambiguity.

## Optional technical work

- Add host-level 301/308 redirects for static aliases if Cloudflare can own a generated redirect map.
- Consider IndexNow only if deployment frequency or Bing discovery latency justifies a verified key and CI integration; the current sitemap is sufficient for the present static cadence.
- Add a controlled production Lighthouse or browser receipt after deployment, plus alerting for `www`, sitemap, robots, and key canonical routes.
