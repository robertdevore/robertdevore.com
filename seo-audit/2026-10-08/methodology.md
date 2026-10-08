# Courses page audit · 2026-10-08

Scope: one new Courses page, its five outbound course destinations, shared discovery files, inbound HTML links, social preview, and production URL variants. The rest of the site was inventoried locally for links and duplicate metadata, not re-audited editorially. No DNS, CDN, analytics, or crawler-policy changes were authorized or made.

## Baseline and delivery chain

Before any remediation, `before/` preserved the unchanged Courses HTML, discovery files, authored template/front matter, hardener, social SVG/PNG and manifest. `before/sha256.json` seals those exact bytes. `before/provenance.json` identifies successful CI build/deploy 37778838321, commit 9bd48dd, artifact 11550394611. This freshly built artifact was restored during the preceding task; it is the untouched baseline, not a claimed new local build. The existing local runtime checkout is ahead of the workspace manifest pin; no local pinned build is claimed.

Authored Markdown/templates + pinned vendored Kujo SSG/SiteKit → GitHub Actions Kujo 1.0.1 release → critical CSS/output hardener/validators → GitHub Pages artifact → custom domain through Cloudflare → browser/crawler. Live responses and Lighthouse identify Cloudflare-added analytics/challenge scripts absent from repository HTML. DNS/CDN account settings and complete logs are unavailable.

## Reproduction

Run from the repository root:

```sh
python3 seo-audit/2026-10-08/collect.py baseline  # initial run only; refuses existing receipt directory
python3 scripts/harden_generated_output.py output
python3 scripts/validate_site.py output
./scripts/validate_html.sh output
howl validate
howl show courses
howl caption courses --platform x
howl render --out /tmp/courses-howl-check --format svg
python3 scripts/render_howl_social.py
python3 seo-audit/2026-10-08/collect.py after     # after deployment; initial run only
```

Use a new dated audit directory for later comparisons; never overwrite this baseline. Full rebuilds follow `.github/workflows/deploy-pages.yml`, including its checksum-verified runtime. Local hardening is a focused integration check; CI is the full-build gate.

Lighthouse 12.8.2 ran on the live URL with Chrome headless and default mobile simulation; command: `npx --yes lighthouse@12.8.2 https://robertdevore.com/courses/ --chrome-flags=--headless --only-categories=performance,accessibility,best-practices,seo --output=json --output-path=<receipt> --quiet`. Raw receipts include environment/version/timing details. One run per phase is a diagnostic sample, not field CWV or a causal performance experiment.

## Limits

UA probes originate from this workstation, not verified crawler IPs. HTTP 200 plus robots permission is not proof of indexing or real-bot access. A search-tool query is not an authenticated rank report. `llms.txt` and WebMCP are existing discovery experiments, not Google AI ranking requirements. Scores are not assigned to avoid false precision with missing field/search data. Lighthouse scores are reported only as lab observations.
