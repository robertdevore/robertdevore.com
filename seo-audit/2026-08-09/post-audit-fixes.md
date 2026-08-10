# Post-audit fixes

## 2026-08-10 — `www` Cloudflare 521 resolved

The audit's remaining P1 hostname failure was corrected in Cloudflare:

- Replaced the proxied `www` A record targeting the stale origin `64.225.44.92` with a proxied CNAME targeting `robertdevore.com`.
- Added active 301 Redirect Rules for both `https://www.*/*` and `http://www.*/*` to the HTTPS apex, preserving the path and query string.
- Verified the root URL, `/projects/agents-sdk/`, and `/blog/page/2/` across HTTP and HTTPS `www` variants. Each now issues one permanent redirect to the equivalent `https://robertdevore.com/` URL and finishes with HTTP 200.
- Verified query-string preservation with `?utm_source=seo-test`.

The Cloudflare 521 is no longer reproducible. The original audit measurements remain preserved as dated evidence of the pre-fix state.
Post-audit P1 affected-page findings are therefore **0**.
