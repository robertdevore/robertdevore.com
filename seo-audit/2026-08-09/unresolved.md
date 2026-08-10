# Unresolved findings

Audit date: 2026-08-09.

## P1 — `www` hostname returns HTTP 521

`https://robertdevore.com/` returns 200 and `http://robertdevore.com/` redirects to it. `http://www.robertdevore.com/` redirects to `https://www.robertdevore.com/`, which returned Cloudflare 521 on repeated checks. This can strand old links and split hostname signals. Correct the Cloudflare/DNS/origin configuration, then make both HTTP variants and HTTPS `www` issue one-hop permanent redirects to `https://robertdevore.com/`. This cannot be repaired safely from the site repository.

## P2 — historical third-party link debt

The after crawl observed 153 failing external-link instances representing 106 unique destinations, concentrated in older posts. Network and third-party behavior can be transient; each row is evidence to verify, not permission to mass-replace citations. Prioritize pages with the most failures in `broken-links.csv`, verify intended context in a browser or archive, then update, annotate, or remove the link. Current project-index dead links were already removed.

## P2 — outcome data is unavailable

Google Search Console (including Generative AI performance), Bing Webmaster Tools, analytics/server logs, CrUX/RUM, and independent AI-answer platform access were unavailable. Organic clicks/impressions/CTR/position, index coverage, crawl stats, conversions, referrals, AI citations, and field CWV/INP remain **NOT AVAILABLE — DATA ACCESS REQUIRED**. See `data-availability.md`.

## P2 — production deployment and recrawl are pending

The final artifact is validated locally, but the production probes and search samples describe the site before these commits are deployed and reprocessed. Deployment is expected from the normal push-to-`main` workflow; verify the workflow and production routes after it completes.

## P3 — eight destinations are four clicks deep

`/blog/page/6/`–`/blog/page/9/` and the older articles `/invest-in-yourself/`, `/making-up-for-lost-time/`, `/organized-chaos/`, and `/twitter-marketing/` are four clicks from the homepage in the generated link graph. Pagination depth is expected; the four articles should receive contextual links only if current topic hubs or new articles genuinely support them.

## Policy choices, not defects

- `robots.txt` currently allows GPTBot as well as search crawlers. GPTBot is a model-training control, not a ChatGPT Search requirement. Keep or change it according to the owner's training policy, not for SEO gain.
- `llms.txt` remains available and valid, but current Google documentation says Google ignores it. Retention is for experimental interoperability only.
- The 172 static legacy aliases use client-side meta refresh because the generated artifact cannot emit host-level status codes. Prefer host-level 301/308 rules if GitHub Pages/Cloudflare operations later provide a maintainable redirect map.
