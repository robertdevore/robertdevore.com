# Data availability

Audit date: 2026-08-09.

| Dataset | Status | Consequence |
| --- | --- | --- |
| Repository source and generated output | Available | Full local crawl, source mapping, implementation, and before/after comparison completed. |
| Production HTTP responses | Available by public probe | Status, redirects, selected headers, crawler user-agent access, and TTFB samples measured. |
| Search-result samples | Available through a web-search provider whose engine, location, personalization, and exact result depth are not exposed | Recorded only as dated observations; not presented as universal Google rankings. |
| Google Search Console standard performance/indexing | **NOT AVAILABLE — DATA ACCESS REQUIRED** | Queries, impressions, clicks, CTR, average position, coverage, canonical selection, and crawl statistics could not be measured. |
| Google Search Console Generative AI performance | **NOT AVAILABLE — DATA ACCESS REQUIRED** | AI-mode/overview site visibility could not be measured. |
| Bing Webmaster Tools | **NOT AVAILABLE — DATA ACCESS REQUIRED** | Bing query, crawl, indexing, and Copilot-adjacent visibility could not be measured. |
| Analytics/server logs | **NOT AVAILABLE — DATA ACCESS REQUIRED** | Organic sessions, conversions, landing-page engagement, bot crawl behavior, ChatGPT/Perplexity/Copilot referrals, and `utm_source=chatgpt.com` could not be measured. |
| Independent ChatGPT Search, Google AI, Bing Copilot, and Perplexity answer sessions | **NOT AVAILABLE — DATA ACCESS REQUIRED** | Citation frequency, cited URL, citation order, competitor citations, and answer accuracy could not be measured. A repeatable question set is preserved in `ai-search-benchmark.csv`. |
| CrUX/Core Web Vitals field data | **NOT AVAILABLE — DATA ACCESS REQUIRED** | Real-user LCP, INP, and CLS are unknown; local Lighthouse is lab evidence only. |

No unavailable value was inferred from a third-party traffic estimator or invented from repository data.
