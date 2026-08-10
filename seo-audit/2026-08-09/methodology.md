# Methodology

Audit date: 2026-08-09. Scope: the complete RobertDeVore.com source repository, its generated static artifact, publicly reachable production endpoints, a dated search-result sample, and a repeatable AI-search question set.

## Evidence sequence

1. Read repository policy, build/deployment contracts, dependency pins, content/templates, generated-output hardening, validators, robots, sitemap, feeds, `llms.txt`, and current first-party search/AI-crawler documentation.
2. Ran the required dependency sync dry-run. It correctly refused to write because the external Kujo SSG/SiteKit checkouts did not match the manifest pins; no vendored artifact was changed. Built the pinned Kujo revision in a temporary detached worktree and used that runtime without adding a machine path to the repository.
3. Built the untouched site, preserved the complete baseline output outside the repository, and crawled every canonical sitemap HTML route before editing.
4. Mapped generated URLs to source/frontmatter where possible and extracted status, indexability, canonical, title, description, headings, visible text, dates, author, schema, links, images, local assets, estimated payload, click depth, sitemap membership, and content hash.
5. Probed production canonical URLs and unique third-party destinations with a descriptive audit user agent. HTTP failures are observations, not proof that a third-party resource is permanently gone; 401/403/405/429 were treated as blocked or indeterminate rather than broken.
6. Sampled representative branded, product, and non-branded queries. The web-search provider does not expose engine, location, personalization, or complete result depth, so the results are dated observations only—not universal rankings.
7. Established 15 natural-language AI-search questions. No independent ChatGPT Search, Google AI, Bing Copilot, or Perplexity answer session/connector was available; all visibility values remain `NOT AVAILABLE — DATA ACCESS REQUIRED` instead of being inferred.
8. Implemented only repository-safe, factual fixes, rebuilt, crawled again, validated generated HTML/assets/routes, and ran Lighthouse 12.8.2 on a representative homepage and media-rich article using local static servers. Lighthouse is lab data; real-user CrUX/Core Web Vitals and INP were unavailable.

The reproducible crawler is `scripts/seo_audit.py`. Core commands:

```bash
python3 scripts/seo_audit.py --output BASELINE_OUTPUT --audit-dir seo-audit/2026-08-09 --phase baseline --production --external
python3 scripts/seo_audit.py --output output --audit-dir seo-audit/2026-08-09 --phase after --production --external
```

## Severity

- P0 / critical: site-wide deindexing, unsafe production behavior, or a defect that prevents meaningful crawling.
- P1 / high: material discovery/indexation/architecture failure affecting a canonical page or hostname.
- P2 / medium: meaningful quality, trust, link, performance, or maintainability debt.
- P3 / low: cleanup or incremental clarity improvement with limited direct impact.

## Internal SEO health score

This is a trend heuristic, not a Google score. The 100 points are: crawlability/indexability 20; metadata/SERP representation 15; information architecture/internal linking 15; content quality/currentness 15; structured data 10; performance/Core Web Vitals evidence 10; media 5; authority/trust 5; AI-search readiness 5. Each category is awarded only for evidence in this audit; missing platform data cannot earn outcome points.

| Category | Weight | Baseline | After | Evidence basis |
| --- | ---: | ---: | ---: | --- |
| Crawlability/indexability | 20 | 16 | 19 | Canonicals/sitemap existed; duplicate indexable pagination, orphan pages, broken links, and `www` failure reduced to the external `www` issue. That final hostname issue was resolved post-audit on 2026-08-10. |
| Metadata/SERP representation | 15 | 9 | 15 | Duplicate archive metadata, legacy keywords, and invalid large-card selection resolved. |
| Architecture/internal linking | 15 | 8 | 14 | 18 orphans and 28 broken internal targets reduced to zero; eight pages remain four clicks deep. |
| Content quality/currentness | 15 | 12 | 12 | Strong first-hand archive; historical third-party link/currentness debt remains. |
| Structured data | 10 | 5 | 10 | Generic/wrong page types replaced with factual page-specific graphs. |
| Performance/CWV evidence | 10 | 7 | 8 | Layout stability improved in lab runs; field CWV/INP is unavailable. |
| Media | 5 | 2 | 5 | 459 missing intrinsic dimensions and eight broken/corrupt linked images reduced to zero. |
| Authority/trust | 5 | 4 | 4 | Authorship and source links are present; external corroboration and stale history still need governance. |
| AI-search readiness | 5 | 4 | 5 | Crawlers were already allowed; entity/schema/internal relationships improved. |
| **Total** | **100** | **67** | **92** | Internal comparison only. |

## AI Search Readiness score

This is also an internal heuristic—not an official score from Google, OpenAI, Microsoft, Perplexity, or any other platform. Components: search-crawler access 15; indexability 10; clarity/entity definition 10; source attribution/authorship 10; original/citable information 15; semantic/structured data 10; internal topic relationships 10; freshness 5; technical/media readiness 5; measured AI benchmark visibility 10.

| Component | Weight | Baseline | After |
| --- | ---: | ---: | ---: |
| Search-crawler access | 15 | 15 | 15 |
| Indexability | 10 | 9 | 10 |
| Information/entity clarity | 10 | 7 | 9 |
| Attribution/authorship | 10 | 7 | 9 |
| Original/citable information | 15 | 12 | 12 |
| Semantic/structured data | 10 | 5 | 10 |
| Internal topic relationships | 10 | 5 | 9 |
| Freshness evidence | 5 | 3 | 3 |
| Technical/media readiness | 5 | 3 | 5 |
| Measured AI visibility | 10 | 0 | 0 |
| **Total** | **100** | **66** | **82** |

The measured-visibility component stays at zero because no independent AI answer/citation data was available. A technically ready site is not presumed to be cited.

## Interpretation limits

- Production probes occurred before these repository changes were deployed. Immediate “after” results describe the generated artifact, not post-deployment indexing or ranking outcomes.
- A valid JSON-LD parse and factual visible-content match does not guarantee a rich result.
- `llms.txt` is retained as experimental interoperability, not credited as a Google ranking mechanism.
- No rankings, traffic, indexing, referrals, or AI citations were fabricated from technical improvements.
