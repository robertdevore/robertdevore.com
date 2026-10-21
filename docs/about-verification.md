# About page: content and design verification

Research checked 2026-10-21. Canonical route: `https://robertdevore.com/about/`.

## Content inventory and attribution

The previous About template emphasized current Kujo work, a four-item through-line, and three navigation cards. The homepage establishes monochrome signal artwork, Departure Mono headings, red accents, numbered sections, and inspectable systems as the recurring theme. Projects and Courses already provide a source-link catalog and six independent learning resources. The redesign retains that visual language and broadens the biography.

| Claim / subject | Evidence | Editorial treatment |
| --- | --- | --- |
| More than 20 years building software | User's supplied brief; `content/posts/5-things-i-learned-building-my-first-gutenberg-blocks-plugin.md`; `content/posts/goodbye-wordpress-a-eulogy.md` | Broad experience claim; no invented start date |
| Independent, commercial, and agency work | `content/posts/im-freelancing-again.md` (2025-02-15), `content/posts/the-past-present-and-future-of-wp-dispensary.md` (2022-08-14) | Custom development, security audits, performance, maintenance; no invented employer or leadership title |
| Technical leadership | User-supplied background; `/leap-the-code-of-extreme-leadership/` and homepage engineering principles | Describes approach and responsibility, not an unverified job title or team size |
| Kujo | [Public organization](https://github.com/kujolang), [language](https://github.com/kujolang/kujo), local project documentation and site's `/projects/kujo/` | Language, runtime, tooling, and ecosystem; no adoption or performance claims |
| Strata | [Repository](https://github.com/robertdevore/strata), local README | Markdown notes application, optional AI, CLI/HTTP interfaces |
| RepoRadar | [Repository](https://github.com/robertdevore/reporadar), local README | Local Git dashboard written in Kujo; avoids the older site's generic scanner description |
| DB Version Control | [Current repository](https://github.com/WebDevStudios/db-version-control), original release article | WordPress content exported to version-controlled JSON; now maintained by WebDevStudios |
| Snips | [Repository](https://github.com/robertdevore/snips), current README | Local macOS text expansion with Electron, SQLite, and a native Swift helper; no unreleased feature claims |
| Markdown Exporter | [Repository](https://github.com/robertdevore/markdown-exporter-for-wordpress) | Content portability; no usage statistics |
| Plugin succession | `content/posts/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios.md` | Article says 20 adopted plugins; historical URL says 21, so visible copy uses the article's 20 |
| Press | [WP Tavern](https://wptavern.com/wp-dispensary-offers-a-complete-marijuana-menu-solution-for-wordpress), [Search Engine Journal](https://www.searchenginejournal.com/wordpress-developer-publishes-code-to-block-mullenwegs-web-hosting-clients/536427/) | Clearly coverage of his work, not authored bylines or endorsements |
| The Repository | December 2024 retrospective reports two mentions; exact issues not independently located | Omitted from public profile rather than implying verified publication or authorship |
| Independent courses | Existing `templates/page-courses.html`; public TypeScript, Rust, Python, CPC course sites | All six existing course destinations retained; no endorsement/certification claim |

The Kujo and Edge Academy course hosts returned HTTP 403 to automated checks. Their links and course identities are supported by the existing catalog; live accessibility could not be independently confirmed by this client. Other featured repository and press links returned HTTP 200. No additional biography claims require approval; omitted publication details would need primary evidence before inclusion.

## Security dataset

Canonical source: `assets/data/security-discoveries.json`. This is a reviewed snapshot, not a feed fetched during builds or page visits.

- [Wordfence page 1](https://www.wordfence.com/threat-intel/vulnerabilities/researchers/robert-devore) lists discoveries 1–20; [page 2](https://www.wordfence.com/threat-intel/vulnerabilities/researchers/robert-devore?page=2) lists 21–40. Every listed item has a different CVE ID.
- All 40 corresponding JSON records were retrieved from the [CVE Program repository](https://github.com/CVEProject/cvelistV5). Each was PUBLISHED and explicitly credited Robert DeVore in `containers.cna.credits`: 9 Wordfence-assigned records and 31 Patchstack-assigned records.
- The [Patchstack profile](https://patchstack.com/database/researchers/770fb791-e511-4ce8-8c93-c3f912d443df) reports 31 reports. These overlap the Wordfence set and are never added to 40.
- [CIRCL plain-name credit](https://vulnerability.circl.lu/credits/Robert%20DeVore) and [Patchstack-program credit](https://cve.circl.lu/credits/Robert%20DeVore%20%7C%20Patchstack%20Bug%20Bounty%20Program) were secondary checks. Name variants are not independent researcher totals.
- Each dataset entry retains affected product, vulnerability class, CNA severity/score/vector, CVE publication date, primary advisory, attribution text and source, Wordfence profile page, Wordfence score/date, verification date, and selection flag.
- Visible severity and dates consistently use the CNA's CVSS 3.1 assessment and CVE Program `datePublished`. Wordfence assessments and publication dates sometimes differ. For example, CVE-2023-37393 is 7.1 in the CNA record and 6.1 on Wordfence; CVE-2024-2793 is published May 31 in the CVE record and May 30 on Wordfence. The page explains this rather than mixing source conventions.
- The six selected disclosures cover unauthenticated stored XSS, reflected XSS, DOM-based stored XSS, contributor-level stored XSS, and missing authorization/content spoofing. No exploit payloads are included.

Maintenance: review both Wordfence profile pages, verify each added CVE and credit, retain source-specific score/date differences, and update the snapshot date and explanatory copy together. Run `python3 scripts/test_about.py` after building. Never sum researcher-profile totals.

## Design and implementation

- Existing signal artwork, fonts, header/footer, buttons, badges, container, and SiteKit accordion/search-input contracts are reused. Native `details/summary` supplies keyboard and no-JavaScript disclosure behavior. No shared SiteKit distribution changes were necessary.
- Wide editorial introduction, four-step undated progression, inverse research section, compact selected disclosures, row-based projects, contrasting learning section, principles, and restrained contact invitation provide varied rhythm without a repeated card dashboard.
- The 40-item index is built statically by `scripts/render_about.py`. Search, severity, reset, result count, and empty state use a small local script. Controls stay hidden when JavaScript is unavailable; records remain readable.
- The renderer validates count, uniqueness, credit, dates, CVSS/severity, and HTTPS source hosts; all external strings are HTML-escaped. The client uses `textContent` and no network requests or HTML insertion.
- Both local build and GitHub Pages workflow invoke the renderer before output hardening. No edits to generated `output/` are committed.
- Title, description, canonical, Open Graph/Twitter metadata, HOWL preview, and AboutPage/Person structured data are aligned. Project nodes identify authored source projects without inventing employment or organizational affiliations.

## Validation record

- The focused About build used the deployment runtime version (Kujo 1.0.1) and the repository's own SSG/templates. All four `scripts/test_about.py` checks passed against its rendered and hardened output.
- Playwright/Chrome checks passed at 390, 768, and 1440 pixels: no overflow or JavaScript errors; CVE search, severity filtering, clearing, empty results, and keyboard activation passed. With JavaScript disabled, all 40 records remained readable through the native disclosure.
- axe-core reported zero WCAG 2 A/AA and WCAG 2.1 AA violations at all three widths, with the complete index open. This is an automated check, supplemented by visual inspection; it is not a claim of exhaustive accessibility certification.
- Nu HTML Checker 26.8.6 passed the redesigned page. CSS bundle freshness and `git diff --check` passed.
- HOWL validated and rendered all 170 card definitions; only the changed About SVG/PNG and manifest entry were retained. Unrelated regenerated images were restored.
- Full local `scripts/build.sh` completed with the isolated manifest-pinned Kujo 1.0.0 release: 138 posts, 3 generated pages, 170 primary routes after hardening. The About route was regenerated with the deployment-version runtime after browser fixes, and its current assets were staged from authored sources.
- Final `python3 scripts/validate_site.py output`: 170 primary routes, zero warnings, passed, including internal-link and asset checks. `python3 scripts/test_about.py`: 4 passed. `python3 scripts/verify_homepage.py output`: passed. `./scripts/validate_html.sh output`: passed across the complete generated site.
- GitHub Pages [run 39550696897](https://github.com/robertdevore/robertdevore.com/actions/runs/39550696897) succeeded for implementation commit `dbbc6cf5c0819e799ea4f5d1e115b018a6cecc59`: fresh full build, all 170-route checks, four About regression tests, homepage checks, full HTML validation, upload, and deployment. The entire browser suite also passed on the live HTTPS page at all three widths, including axe and the no-JavaScript fallback. A browser fetch of the live JSON returned HTTP 200 and matched the committed dataset byte-for-byte. Raw urllib requests were blocked with HTTP 403, so live checks used the browser.

### Existing dependency-manifest drift

Before this change, the clean baseline at `f16d160` already had a vendored `build.kujo` hash differing from `workspace-dependencies.json`. History includes intentional metadata compatibility fixes (`a563720`, `d94264d`, `6bf1edb`). A dependency sync would overwrite these patches. This redesign does not change the SSG source or pin metadata. `sync_dependencies.sh --check` still reports this pre-existing mismatch, even with the pinned source checkouts. The standard build can be run with the documented `KUJO_ROOT` override to an isolated pinned checkout and its verified release binary. Current neighboring dependency checkouts are newer than the manifest and are not reset.

## Requested refinement, 21 October 2026

- Edited the page using the Orwell writing skill: clearer background, research introduction, project summaries, and contact invitation.
- Added a white hero text outline; promoted the four progression labels to headings; gave the 40-discovery figure explicit Departure Mono sizing and excluded it from text scrambling.
- Selected six disclosures, enlarged their titles, and removed the extra explanatory sentences. The verified 40-record snapshot and provenance remain intact.
- Replaced Stattic and WP Dispensary in the project showcase with DB Version Control and Snips; updated the project schema association.
- Built a distinct Featured press panel led by Search Engine Journal, followed by WP Tavern and the verified [WP Minute interview](https://thewpminute.com/open-source-saved-my-life/). Own writing is not presented as press coverage.
- Replaced the closing red divider with the shared thin neutral rule.
- Focused deployment-runtime build and four research/markup checks passed. Browser checks passed at 390, 768, and 1440 pixels, including the visible 40 in Departure Mono, six selected disclosures, press order, filters, keyboard controls, no-JavaScript records, no overflow, and zero automated accessibility violations.

## Additional press verification, 21 October 2026

- Added Within WP (Within WordPress), linking directly to its [14 February 2025 newsletter](https://withinwp.com/newsletter/faster-woo-and-new-and-improved-generateblocks-wpgraphql/). The news section names Robert DeVore and links to his AI-Powered Patterns plugin announcement. This is labeled a newsletter mention, not an interview or authored article.
- Search Engine Journal remains first; all existing coverage links remain.
- The Repository remains pending verification: its site returned a Cloudflare challenge to both HTTP and browser access, and searches did not locate a specific mention. The existing December 2024 retrospective alone does not establish a primary publication URL.
