# Shared analytics and search configuration

Verified 2026-10-22. This records the live Cloudflare configuration; changing the source file here does not publish it to Zaraz.

## Identity and collection

- Existing GA4 property: Robert DeVore, `311013393`; stream `3447802764`; measurement ID `G-PV52K8R0R8`. Canonical stream URL is now `https://robertdevore.com`.
- Existing Search Console **Domain** property `robertdevore.com` covers the apex and all subdomains. Its existing link to this GA4 stream was verified, not recreated.
- Zaraz GA4 tool `hygV` requires analytics purpose `vIAC`. Consent management and the initial choice dialog are enabled. Automatic pageviews are enabled; SPA and automatic data-layer conversion are disabled.
- GA4 originating IP forwarding and advertising audiences are disabled. Query removal, IP trimming, user-agent cleaning, external referrer removal and denied Google Consent Mode defaults are enabled. Removing query/referrer data limits attribution detail intentionally.
- Cloudflare Web Analytics site `fa7fb605a02e4a7787646ff8ae788884` uses manual installation. Its public beacon token is `d9d7359b43a441e6a71dd4d4cb6f45a5`.
- Zaraz custom HTML tool `NZDm` runs `consent-controls.html` on Pageview without a consent gate so visitors can always reopen their choices. The helper itself gates the beacon on `vIAC`, prevents duplicate loads, and reloads after withdrawal to stop the loaded beacon.
- No new paid plan, session replay, advertising product or separate GA property was introduced.

## Host coverage and boundaries

`evidence/final-host-checks.json` records 18 reachable public hosts with Zaraz injection and no automatic Cloudflare beacon. Browser checks demonstrated rejection without a beacon, acceptance with one beacon, a working Privacy settings control, and withdrawal without a beacon on reload. GA realtime showed main-site and course-site pageviews; Cloudflare reporting showed multiple hostnames under the existing site.

CheatCodes now uses Cloudflare proxying for its existing GitHub Pages CNAME. Its target was not changed.

Configuration rule `8835caae0d37407bbd54bae267b83350` disables Zaraz and RUM on bench, admin/staging/origin host prefixes, and private/API paths. Bench remains behind Cloudflare Access. Mail and verification DNS names are not websites. WWF redirects to the main site.

Response-header rule `8840a5e6aa3c46218917192dc83efd1b` preserves existing CSP directives while allowing the Cloudflare beacon script and connection origins on HTML from TypeScript, Kujo, Rebuild and Edge Academy. Rule `79f9a6f6f43a434787ba0f2138d01fcc` supplies Edge Academy's explicit script directive when absent. Neither enables unsafe-inline or removes the other protections. Browser-cached pages from before the configuration change may need a fresh navigation; verify a fresh URL as well as revisits.

## Search submissions

All 15 current sitemap files (main plus 14 subdomains) showed **Success** in Google Search Console, totaling 736 listed URLs at verification. These are discovered URLs, not a promise of indexing. The two historical 2015/2016 WordPress sitemap-index submissions were retained; their stale errors do not describe the current sitemap.

Bing ownership was verified with a DNS-only CNAME `27d6cbe94d24628fd6a43e029c53ccc4` to `verify.bing.com`. The same 15 sitemap files were submitted and all showed **Success**, with 736 discovered URLs. See `evidence/bing-sitemap-results.json`. Discovery is not a guarantee of indexing.

The legacy MoneyMan, Mother's Day and Wolfpack pages have no sitemap at the conventional location. They receive the shared analytics configuration but were not newly promoted for search indexing. IntelliPress returned Cloudflare 522 on retry, and Savage/Vuln do not resolve through their old targets; restore or retire those hostnames separately before claiming universal live-site coverage.

## Future sites and verification

A new public subdomain must be proxied, serve normal HTML, permit the shared scripts/connections under its CSP, and expose the privacy control. Check accept/reject behavior and its hostname in reporting. Submit its actual sitemap separately to the existing domain properties. Consent rejection, blockers and disabled JavaScript mean analytics never represents every request; Cloudflare edge/security request counts are a separate measure.

Do not count email-link clicks as delivered enquiries. The main site's contact page uses email and has no successful-form event to instrument. Additional application events need explicit, non-sensitive success signals from their application code.
