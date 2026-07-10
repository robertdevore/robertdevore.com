# RobertDeVore.com build postmortem

**Date:** 2026-07-10  
**Scope:** `robertdevore.com`, Kujo SSG, SiteKit, and the Kujo runtime path used to build the site.  
**Method:** source, history, generated output, published project records, and fresh local validation. This is a postmortem of the evidence available in these checkouts; it is not a claim that unrecorded work did not happen.

## Executive assessment

The project proves that a determined maintainer or agent can build, migrate, validate, and visually differentiate a substantial 138-post publishing site with Kujo SSG and SiteKit. The result is source-first, static, accessible by construction in several important ways, and has reproducible local output on this machine.

It does **not** prove that the ecosystem is ready for a broad public launch. Kujo SSG has unresolved security hardening work documented by its own roadmap, no development watch mode, a macOS/local-checkout-dependent integration method, and inadequate cross-repository release provenance. SiteKit is a credible source-driven component system, but it is explicitly private/source-only, so its consumer upgrade and distribution story is not yet a product-grade package boundary. The target site has strong site-specific validation, but it relies on local Python dependencies and accepts 73 historic broken-link warnings without a machine-readable waiver.

**Public-launch conclusion:** not ready.  
**Limited-beta conclusion:** ready for maintainers and technically capable early adopters, provided they receive a pinned workspace, an environment check, and an explicit acknowledgement of the security and reproducibility limits below.

## Evidence standard and limits

Findings use these labels:

- **Evidence:** Directly observed, Reproduced, Inferred from implementation, Reported but not reproducible, or Unknown.
- **Confidence:** High, Medium, or Low.

Directly observed/reproduced evidence includes:

- Target history: six commits on 2026-07-10, from `d703fc1` through `a57dc9b`; the primary rebuild replaced tracked generated output with sources and ignored `output/`.
- Content inventory: 138 posts, 12 pages, six project items, five category archives, and six tag archives.
- Fresh target build: `./scripts/build.sh` completed in 7.865 wall seconds and reported 138 posts/12 pages.
- Fresh target validation: `python3 scripts/validate_site.py output` checked 195 primary routes and passed with 73 historical-link warnings; the SSG validator checked 388 HTML files and passed.
- Fresh SiteKit gate: build, lint, component validation, and snapshot all passed for 85 components.
- Fresh SSG checks: CLI contract test and generated-output contract test both passed; the starter build generated 4 posts/3 pages in 1.74 seconds and passed generated-output validation.
- SSG commits `8641a71` and `d17ed50` added root-level post routes and custom-collection `llms.txt` output, with generated-output assertions. The target's vendored `build.kujo` is byte-identical to the SSG checkout.

The following were **not** available: an agent transcript, task plan, command receipt stream, RunLedger record, CaseFile, Lens run, ShipCheck run, CI log, clean-machine run, deployment evidence, performance trace, or accessibility-tool report. Absence is a traceability finding, not evidence that those activities did not occur. The screenshots in `reports/visual/` are evidence that visual captures were retained, but they do not replace a recorded browser or accessibility test run.

## Chronological journey reconstruction

| Phase | Expected / actual path | Evidence, outcome, and lesson |
| --- | --- | --- |
| 1. Orientation | Discover a repository that previously tracked output, then establish authored sources. | `docs/architecture.md` records 138 posts, 12 listed pages, 28 pagination pages, and roughly 1 GB of media variants with no source build configuration. `d703fc1` performed the conversion. **Directly observed; High.** The source-first decision was correct and should be a documented migration product, not an ad-hoc feat commit. |
| 2. Instruction and ecosystem discovery | Identify SSG and SiteKit contracts before editing. | SSG has `AGENTS.md`, README, templates, and contract scripts; SiteKit has `AGENTS.md`, `DESIGN.md`, schemas, recipes, and standards. The target repository has no committed `AGENTS.md`; its README is the primary entrypoint. **Directly observed; High.** Cross-repo instructions exist but are not surfaced by the consuming site. |
| 3. Architecture and content model | Model pages, root-level posts, projects, and taxonomy archives. | `content/` is organized by type and the target uses per-template overrides. `docs/architecture.md` records materialized category/tag collections because native taxonomy archives are absent. **Directly observed; High.** This is a successful use of custom collections, plus a workaround for a general SSG capability gap. |
| 4. Route preservation | Preserve public post URLs while moving the blog index to `/blog/`. | SSG commit `8641a71` added `posts_at_root`; its contract test asserts root post output while retaining `/blog/`. **Directly observed; High.** A real-site requirement drove a reusable upstream feature and test. |
| 5. Component and theme composition | Use SiteKit distribution assets and compose a distinct editorial theme. | Target `assets/css/sitekit/` vendors compiled output; `assets/css/site.css` and templates add editorial composition. `docs/architecture.md` maps skip link, navigation, cards, metadata, pagination, and alerts to SiteKit. **Directly observed; High.** Distinct design was possible without changing SiteKit. |
| 6. Migration | Parse old site inventory/HTML into Markdown and retain routes. | `scripts/migrate_legacy.py`, `docs/content-migration.csv`, and the 138 migrated post files are present. **Directly observed; High.** There is no recorded repeat run or source checksum, so the import is auditable but not fully replayable. |
| 7. Asset integration | Retain legacy media and add optimized hero art. | `assets/legacy-images` is 195 MB; full checkout is 1.1 GB. Three hero art variants have desktop/mobile WebP plus PNG sources. **Directly observed; High.** Preserving historic assets protected content fidelity but leaves a scale and repository-cost problem. |
| 8. Build/debug loop | Build target, provision font assets, validate output. | `bca635c` adds missing Inter assets and CSS path corrections after the initial build. `scripts/build.sh` then produces a clean output. **Directly observed; High.** This is a successful recovery, but exposes manual dependency sync and unpinned assets. |
| 9. Project and machine-readable output | Add project repository pages and include projects in `llms.txt`. | `14cfc35` adds six project pages; target commit `a57dc9b` vendors SSG change `d17ed50`, updates validators, and tests output. **Directly observed; High.** Strong end-to-end feedback loop, but the upstream SSG checkout is ahead of its remote by one commit. |
| 10. Visual, accessibility, and release review | Verify representative desktop/mobile pages and generated metadata. | Screenshots exist under `reports/visual/`; `docs/verification.md` describes browser checks. Fresh structural validation passed. **Reported plus directly observed artifacts; Medium.** The visual process lacks a command, viewport manifest, and pass/fail receipt. |

No timing, failed-attempt count, or context-switch count can be honestly reconstructed beyond the build times above. The documented history shows one asset-provisioning correction and several deliberate refinements; it does not establish retry totals.

## What worked exceptionally well

### Source-first migration and route preservation

The migration replaced generated output with authored Markdown, templates, assets, and configuration. `output/` is ignored, and the target build regenerates 388 HTML files. The crucial production route requirement—posts at `/<slug>/` while retaining `/blog/`—was generalized upstream in `8641a71` rather than simulated with a site-specific router. This is the strongest evidence of useful ecosystem extensibility.

- **Classification:** Q — No defect / positive capability
- **Evidence:** Directly observed and reproduced
- **Confidence:** High
- **Regression protection:** retain the root-route generated contract and add a cross-repo fixture using this site shape.

### Transparent, deterministic static pipeline at this scale

The target clean build completed in 7.865 seconds on the current machine and passed both target and SSG structural validation. The generated `llms.txt`, feed, sitemap, robots, 404, canonicals, JSON-LD, root routes, and project collection were all checked by `scripts/validate_site.py`. The output is inspectable instead of hidden behind a hosted platform.

- **Classification:** Q — No defect / positive capability
- **Evidence:** Reproduced
- **Confidence:** High for this machine and corpus; Low for other machines or larger sites
- **Public positioning:** “auditable local static builds” is defensible; “fast at any scale” is not, given SSG's own performance report.

### SiteKit's tokens and semantic defaults supported differentiation

SiteKit's source model has 85 schema-backed components; its generated CSS, tokens, `kujo-light` theme, `skip-link`, navigation, card, code-block, metadata-panel, and form patterns were enough for the target to maintain a recognizably different editorial design. The target uses native `<details>` for mobile navigation and progressive enhancement rather than a component-library JavaScript runtime. SiteKit’s own gate passed after regeneration.

- **Classification:** Q — No defect / positive capability
- **Evidence:** Directly observed and reproduced
- **Confidence:** High
- **Caveat:** the target consumes copied distribution artifacts, not a versioned package, so this is evidence of composition quality, not of package ergonomics.

### Target-specific validation is unusually substantive

`scripts/validate_site.py` checks title/description/canonical coverage, one-H1 structure, duplicate IDs, image `alt` attributes, JSON-LD parseability, CSS asset references, required routes, related-reading contracts, project landing content, contact-form labels, footer social links, and project entries in `llms.txt`. It turned site requirements into executable policy rather than a prose checklist.

- **Classification:** Q — No defect / positive capability
- **Evidence:** Directly observed and reproduced
- **Confidence:** High
- **Protect:** promote its smallest generic checks into SSG integration contracts; leave brand/content assertions in the site.

## Major findings

### F-01 — The cross-repository integration is machine-layout-dependent

`scripts/build.sh` defaults `KUJO_BIN` to `/Users/robertdevore/2026/Kujolang/kujo-repos/kujo/target/release/kujo`. `scripts/sync_dependencies.sh` defaults SSG and SiteKit roots to sibling absolute paths and uses BSD-only `sed -i ''`. The target vendors `build.kujo` and compiled SiteKit CSS/fonts by copying them; there is no manifest recording source repository commit, asset hashes, or compatible version range. The SSG checkout itself is `main...origin/main [ahead 1]` at `d17ed50`.

- **Classification:** I — Packaging/dependency problem; contributing N — Environment problem
- **Evidence:** Directly observed
- **Confidence:** High
- **Impact:** a fresh developer cannot infer the required checkout layout, Kujo binary build, source revisions, or platform-specific `sed` behavior. A consumer can silently obtain a different upstream result after sync.
- **Severity / priority:** S1 / P0 for broad launch; S2 / P1 for limited beta
- **Recommendation:** create a lockable workspace manifest with repository URLs, commit SHAs, artifact hashes, and compatibility versions; make `sync` cross-platform; make `build` resolve a project-local tool or fail with an actionable doctor report; add a clean-directory integration test.

### F-02 — SSG has documented security-hardening gaps

`ssg/docs/enhancements-roadmap.md` identifies three P0 items still open: featured-image path traversal outside allowed roots, remote image/font fetches without a destination policy in trusted mode, and fragile frontmatter splitting around `---`. The target has `download_remote_images: false`, so it did not exercise remote fetching, but that does not resolve a platform issue. The site also imports historic Markdown and assets, making robust path boundaries especially relevant.

- **Classification:** C — SSG missing capability / hardening; contributing P — Test gap
- **Evidence:** Directly observed in SSG roadmap; not independently exploited
- **Confidence:** High for documented status; Medium for practical exploitability in a trusted-author workflow
- **Severity / priority:** S1 / P0 before public release where untrusted or third-party content can be built
- **Recommendation:** canonical-root enforcement for local featured images; opt-in private-network deny policy for remote fetches; delimiter-aware frontmatter parser; negative regression fixtures. Do not market untrusted-content builds before this work passes.

### F-03 — Development experience omits a working watch mode

The public SSG README and `--help` expose `--watch` as reserved/not implemented; `build.kujo` prints a warning and performs one build. The target’s own README tells users to run a separate Python HTTP server after an explicit build, with no rebuild loop or live reload. This is not a failure for the completed site but is a repeated normal workflow for website builders.

- **Classification:** C — SSG missing capability
- **Evidence:** Directly observed
- **Confidence:** High
- **Severity / priority:** S2 / P1
- **Recommendation:** implement content/template/asset/config watching with debounced rebuilds, stable non-zero failure behavior, and documented browser refresh or live-reload semantics. Until then, remove `--watch` from the “feature” mental model and provide a copyable shell loop as an interim procedure.

### F-04 — Native taxonomy archives are absent; the site materializes them as collections

The target’s category and tag archives are Markdown items under `content/category` and `content/tag`, regenerated by `scripts/migrate_legacy.py`, because SSG does not provide native taxonomy archive generation. That works for the known historic corpus but creates duplicated derived content and a migration-time maintenance obligation. It does not automatically demonstrate taxonomy term normalization, empty archives, collision handling, pagination, metadata, or future post updates.

- **Classification:** C — SSG missing capability
- **Evidence:** Directly observed
- **Confidence:** High
- **Severity / priority:** S2 / P1
- **Recommendation:** add first-class taxonomy index/term archive generation from post frontmatter, with stable slug normalization, empty-term policy, pagination, metadata context, collision checks, and a migration path from materialized collections. Keep materialized archives available as an intentional override.

### F-05 — SiteKit is source-driven but lacks a consumer release contract

SiteKit’s README explicitly labels it `private: true` and says consumers copy or vendor reviewed source surfaces. That is consistent with its current internal phase, but it conflicts with easy multi-site adoption. The target copies generated CSS/fonts and patches `base.css` after copying. There is no package version, lockfile, provenance metadata, compatibility policy, or automated consumer fixture that verifies `sync_dependencies.sh` against a particular SiteKit version.

- **Classification:** I — Integration problem; contributing I — Packaging/dependency problem
- **Evidence:** Directly observed
- **Confidence:** High
- **Severity / priority:** S2 / P1
- **Recommendation:** before broad release, choose and document one supported consumption model: published package, versioned tarball, vendored release bundle with manifest, or a workspace tool. Supply a lockfile/manifest and an upgrade command that reports changed tokens/components. Do not call the current copy process “installation.”

### F-06 — Visual/accessibility quality is asserted but not receipt-backed

There are eight visual PNGs and prose in `docs/verification.md` reporting desktop/mobile checks. The target structural validator is strong, but it does not test keyboard navigation, focus visibility, forced colors, reduced motion, computed contrast, heading order, or visual regressions. SiteKit's README also says browser/accessibility testing remains a separate pre-launch requirement. No Lens receipt, browser script, or accessibility scanner report is present.

- **Classification:** P — Test or quality-system gap; contributing J — Agent workflow problem
- **Evidence:** Directly observed missing receipts; visual review reported but not independently reproduced
- **Confidence:** High for missing automation; Medium for the claimed browser QA outcome
- **Severity / priority:** S2 / P1
- **Recommendation:** add a deterministic visual/accessibility command with a route and viewport manifest, persist its JSON/report/screenshot receipt outside generated output, and run it in CI. Start with home, long post, archive, project, contact, 404, and mobile nav.

### F-07 — Historic broken links are visible but the acceptance policy is weak

The target validation passes with 73 warnings, reporting only the first 20 in output. `docs/verification.md` explains that historical links were preserved rather than fabricated. That editorial decision is reasonable, but the warnings are not keyed to a versioned exemption manifest, no full report is committed, and a new broken link is indistinguishable from a tolerated historic one in the final pass message.

- **Classification:** M — Content problem; contributing P — Test/quality-system gap
- **Evidence:** Reproduced
- **Confidence:** High
- **Severity / priority:** S3 / P1
- **Recommendation:** emit a full JSON/CSV broken-link report, classify each entry (`intentional historical`, `external`, `needs redirect`, `new regression`), fail only on unapproved/new entries, and review the manifest periodically. This is not a reason to invent redirects.

### F-08 — SSG documentation and roadmap state are internally stale/confusing

`ssg/docs/parity-audit.md` contains findings that were later fixed in current `build.kujo` and tests: taxonomy rendering, display date formatting, RSS dates, absolute social images, JSON-LD, and favicon output. Its action list remains written as if these are open. `ROADMAP.md` also has unchecked baseline/CLI/init items while the text says validated. The documents retain valuable history, but they are not labelled as superseded or reconciled.

- **Classification:** D — SSG documentation problem
- **Evidence:** Directly observed by comparing current contract assertions to the audit/roadmap
- **Confidence:** High
- **Severity / priority:** S3 / P1 because new users and agents will follow stale gaps
- **Recommendation:** add a “superseded by commit/version” status to historic audits; create one current capability matrix generated or verified from contracts; make roadmap checkbox state match its status table. Do not delete historical evidence.

### F-09 — Target release checks depend on undeclared Python packages

`scripts/validate_site.py` imports `bs4`, but the target has no `requirements.txt`, lockfile, `pyproject.toml`, or bootstrap command. The validation succeeded on this machine only because BeautifulSoup was available. The README lists the validator without declaring this prerequisite.

- **Classification:** I — Packaging/dependency problem
- **Evidence:** Directly observed and reproduced on an already-provisioned environment
- **Confidence:** High
- **Severity / priority:** S3 / P1
- **Recommendation:** declare and pin the Python validation environment, or reimplement the required checks using dependencies already provided by a documented tool. Add a fresh-venv CI check.

### F-10 — SSG scale claims need qualified benchmarks and scale safeguards

The target’s 138-post build is quick, but it is not a scale test. SSG’s `docs/performance-findings.md` reports a serial finalize floor and that the reference generator is about 13.5× faster at 10k pages; its roadmap lists native frontmatter parsing, finalize parallelism, and file walking as runtime work. The target emits 388 HTML files but does not stress thousands of posts, sitemap limits, many derivative images, or CI cold starts.

- **Classification:** C — SSG missing capability; contributing P — Test gap
- **Evidence:** Directly observed source documentation; target performance reproduced
- **Confidence:** High for reported benchmark limitations; Low for this site’s projected degradation
- **Severity / priority:** S3 / P2 for current target; S2 / P1 if broad launch promises large-site performance
- **Recommendation:** publish fixed-hardware, clean-run benchmark fixtures at 100/1k/10k content items; implement sitemap sharding before 50k URLs; report serial-finalize share and memory use.

## Workaround inventory

| ID | Workaround | Native expectation / actual behavior | Risk and long-term disposition |
| --- | --- | --- | --- |
| W-01 | Materialized taxonomy archives in `content/category` and `content/tag` | Native taxonomy archive generation was unavailable; custom collections produce routes. | Derived Markdown can drift from post frontmatter. Replace with native archives plus migration support; retain override files only when editorially intentional. **C, S2/P1.** |
| W-02 | `scripts/sync_dependencies.sh` copies SSG and SiteKit artifacts | Consumers should resolve compatible dependencies declaratively; actual process requires sibling checkouts and a BSD `sed` rewrite. | Machine/version drift. Replace with a lockable release bundle/workspace command. **I, S1/P0.** |
| W-03 | Target vendors `build.kujo` | Site should use a pinned SSG release; target copies the single source file. | Undocumented upstream delta and difficult upgrades. Replace with explicit package/release provenance. **I, S2/P1.** |
| W-04 | `scripts/build.sh` embeds an absolute Kujo binary path | Project-local or discoverable runtime selection expected. | Other machines fail immediately. Use local tool resolution and doctor output. **N/I, S1/P0.** |
| W-05 | Python/BeautifulSoup site validator outside SSG | Generic generated-site validation expected upstream; target adds rich local assertions. | Undeclared dependency and duplicated quality logic. Keep site assertions; promote generic checks to SSG. **I/P, S3/P1.** |
| W-06 | Native `<details>` plus `assets/js/site.js` enhancements | SSG only renders static markup, so interactive behavior is composed locally. | This is intentional extension code, not a platform defect; maintain no-JS behavior. **Q, S4/P3.** |
| W-07 | Preserve broken historical URLs as warnings | Migration should not fabricate destinations. | Warning debt can hide regressions. Keep content fidelity, add waiver manifest and policy. **M/P, S3/P1.** |

## Tool inventory

| Tool/system | Actual use and evidence | Verdict |
| --- | --- | --- |
| Kujo runtime CLI | Builds target and SSG via a local release binary; contract path exercised. | **Essential.** It rendered the site and enforced CLI failure contracts. |
| Kujo SSG | Vendored `build.kujo`, templates/content/frontmatter, auxiliary output, generated validation. | **Essential.** Adequate for this migration, with launch gaps above. |
| SiteKit | Vendored compiled CSS/font distribution; 85-component source gate run. | **Strongly beneficial.** It supplied consistent tokens/accessibility primitives, but its consumer distribution is immature. |
| Target `migrate_legacy.py` | Present; imports old inventory/HTML to Markdown and materializes archives. | **Essential for this migration.** No replay receipt or input snapshot was found. |
| Target `validate_site.py` | Fresh run passed 195 primary-route checks with 73 warnings. | **Strongly beneficial.** Site-specific and dependency-undeclared. |
| SSG generated-output validator/contracts | Fresh SSG output and contract test passed. | **Strongly beneficial.** It validates important shape but not target real-world migration cases. |
| Screenshots in `reports/visual` | Eight retained PNG artifacts; no command/report found. | **Useful, not sufficiently tested.** |
| Lens, RunLedger, ChangeBucket, PackWrite, Muzzle, ShipCheck, CaseFile, Howl, Concord, Watchdog, RAG/context system | Repositories may exist in the broader checkout, but no target configuration, receipt, or invocation evidence was found. | **Not actually used.** Do not claim their value for this build. |

## Kujo language/runtime and CLI review

The language/runtime was used indirectly through `kujo run ./build.kujo`; the target did not author a separate Kujo program beyond the vendored SSG. Its directly exercised behavior is therefore the SSG CLI path, filesystem writes, config parsing, template/Markdown rendering, and native render helpers. There is insufficient evidence to rate the general language, compiler, standard library, package manager, or runtime across unrelated workloads.

Strengths: contract tests demonstrate non-zero failures for unknown flags, missing values, malformed configuration, and invalid enums. Configuration precedence among YAML/YAML/JSON plus CLI overrides is tested. The local runtime executed both the target and starter builds successfully.

Shortcomings: the target does not use a package manager or project manifest for Kujo; runtime discovery is absolute-path based; no machine-readable diagnostic mode was used; `--watch` is an explicit no-op; and no clean-room runtime installation was exercised. The SSG's current trusted-mode remote fetch behavior needs the security controls described in F-02.

## SiteKit review

### Component coverage and API quality

The 85-component inventory, schemas, examples, generated design guide, and source checks are strong discoverability foundations. Component schemas consistently declare variants, token dependencies, slots, responsive strategy, and accessibility notes. The site’s use of semantic, static patterns shows that SiteKit did not force a generic visual identity or an application runtime.

The gap is the boundary between a source library and a consumer. Copying generated assets delivers CSS but not component templates, schemas, version information, upgrade guidance, or a consumer test. The target uses SiteKit classes/composition rather than instantiating every component through a formal adapter; that is flexible but leaves API compatibility implicit. No generic SiteKit change is required for the target’s signal art, editorial rhythm, project landing composition, or contact flow; these are correctly theme-level/site-specific.

### Accessibility

SiteKit's standards and schemas establish useful contracts; target templates/documentation claim landmarks, skip links, one H1, focus states, native disclosure navigation, reduced motion, forced-colors, and print styles. Fresh structural checks confirmed several of these output invariants. Keyboard, focus, contrast, screen reader, and motion behavior still require automated/browser evidence before broad launch (F-06).

### Upstream candidates

No target visual treatment clearly belongs upstream. Candidate upstream work is infrastructure: a SiteKit distribution manifest, consumer fixture, and documented source/bundle upgrade path—not the site’s decorative CSS, art direction, or editorial layouts.

## Security and safety review

No secret, deployment, or destructive-output incident was observed. `output/` is ignored, and the target build deletes its configured relative `output` directory before rebuilding. That behavior is normal but should be guarded by an output-root safety test when `--output` is configurable.

The meaningful security concerns are F-02's documented local-path and remote-fetch issues. The migration preserves raw historical content and link targets; validation parses generated HTML but does not test template escaping or HTML sanitization. Treat raw HTML/Markdown sanitization as **unknown**, not proven safe. The target did not deploy, so accidental deployment was not exercised. Absolute paths increase the risk of editing/running against the wrong checkout, but no such incident was observed.

## Reproducibility rating: Environment-dependent

A second person can understand the architecture, but cannot reproduce the validated build from this repository alone. Required but undocumented/insufficiently documented inputs include:

- macOS-compatible `sed -i ''` for dependency sync;
- the exact sibling checkouts under `/Users/robertdevore/2026/Kujolang/kujo-repos/`;
- SSG at local `d17ed50` (not pushed upstream at review time);
- a built Kujo release binary at an absolute path;
- Node/npm for SiteKit;
- Python plus BeautifulSoup for site validation;
- any original legacy inventory/HTML required to replay migration;
- a visual QA browser/tool and acceptance recipe.

The target itself builds after these are present, so this is not “not reproducible”; it is not yet reproducible with a documented setup. The clean-room checklist and golden path are in [kujo-website-golden-path.md](kujo-website-golden-path.md).

## Performance and scale

Observed target numbers are only the 7.865-second clean build and 388 generated HTML files on this machine. Runtime assets are generally restrained for the new chrome—architecture records 22,926-byte site CSS, 4,723-byte JS, 22,496-byte Departure Mono WOFF2, and 93–128 KB desktop heroes—but the repository/output remain large due to 195 MB of legacy media. Those source numbers were not independently recomputed in this review.

Projection: hundreds of posts are already exercised; thousands of posts, image derivatives, taxonomies, and CI cold starts are not. SSG's own performance report identifies a serialized finalization floor and worse 10k-page results than its reference comparator. Before launch, benchmark a realistic 1k/10k corpus and run a fresh-machine build with cold caches.

## Launch-readiness scorecard

| Area | Score | Main evidence / limitation |
| --- | ---: | --- |
| Kujo language/runtime (used slice) | 3 | Builds and contracts pass; general language/package/runtime was not evaluated. |
| Kujo CLI | 3 | Good failure contracts; no doctor or portable project-local discovery exercised. |
| SSG core | 3 | Real site completed and tested; security hardening and real-world fixtures remain. |
| Theme architecture | 4 | Target overrides compose cleanly; no upgrade/reuse proof. |
| Frontmatter | 3 | Current tests are strong; delimiter robustness remains documented open work. |
| Routing | 4 | Root posts and custom collections are tested; collision/redirect manifest coverage absent. |
| Collections | 4 | Projects worked and `llms.txt` was added with tests. |
| Taxonomies | 2 | No native archives; materialized site workaround. |
| Asset pipeline | 2 | Local copying works; path/security and provenance gaps remain. |
| Image workflow | 2 | Historic media preserved; no responsive derivative/metadata pipeline proven. |
| SEO/schema/feed/sitemap/llms | 4 | Target and SSG contracts cover core output; large sitemap and preview validation absent. |
| Development server/watch | 1 | `--watch` is explicitly unimplemented; target uses separate static server. |
| Production build | 3 | Deterministic local run passes; clean-room/CI behavior unproven. |
| Diagnostics | 3 | CLI negative paths pass; site integration failures lack doctor/provenance guidance. |
| Documentation | 2 | Strong surfaces but stale SSG audit/roadmap and missing consumer setup. |
| Testing | 3 | Good contracts; no integrated clean-room, visual/a11y, or full link waiver gate. |
| SiteKit components/tokens/customization | 4 | 85 validated components and a distinct target design; distribution boundary weak. |
| SiteKit accessibility | 3 | Good contracts and structural evidence; browser proof absent. |
| Cross-repository integration | 1 | Absolute paths, copying, no lock/provenance. |
| Agent usability | 2 | Sources are searchable; no orientation/context/receipt workflow. |
| Human developer usability | 2 | Normal build works once configured; no working watch/install path. |
| Reproducibility | 1 | Environment-dependent. |
| Traceability | 2 | Good commits/docs/validators; no command receipts or migration replay evidence. |
| Performance | 3 | Good observed 138-post result; large-scale gap documented. |
| Security/safety | 2 | No incident observed; unresolved documented SSG hardening. |
| **Overall ecosystem launch readiness** | **2** | Strong internal beta showcase, not a broad-release product workflow. |

## Launch blockers

1. **Portable, pinned integration is absent** — F-01. Before public beta, a consumer must be able to clone one declared workspace and run a documented build without Robert’s filesystem layout. **Owner:** SSG/SiteKit release engineering. **Size:** M. **Done when:** lockable manifest, cross-platform sync/install, doctor, and clean-room CI pass.
2. **SSG untrusted-input hardening remains open** — F-02. **Owner:** SSG/runtime maintainers. **Size:** M. **Done when:** root confinement, remote-destination policy, robust frontmatter delimiter parsing, and adversarial fixtures pass.
3. **No trustworthy visual/accessibility release receipt** — F-06. **Owner:** quality engineering. **Size:** M. **Done when:** deterministic route/viewport/a11y command runs in CI and stores reviewable artifacts.

The lack of native taxonomy archives and watch mode are P1 major-friction items, not launch blockers for a constrained private preview with documented workarounds.

## Recommended product changes

| Product change | Problem and evidence | MVP / priority |
| --- | --- | --- |
| `kujo site doctor` | Absolute paths and undeclared dependencies block clean setup (F-01/F-09). | Resolve runtime, config, dependency manifest, Python/tool prerequisites, writable output, and source revisions. **P0.** |
| Versioned website workspace | Vendored `build.kujo`/CSS have no provenance (F-01/F-05). | Manifest + lock with SSG/SiteKit/runtime SHAs and sync verification. **P0.** |
| Native taxonomy archives | Site materializes category/tag sources (F-04). | Term/collection generation, pagination, collision checks, migration guide. **P1.** |
| SSG watch/dev command | `--watch` is a no-op (F-03). | Poll/debounce and clear failure status; live reload can follow. **P1.** |
| Site release verifier | Visual/accessibility/link evidence is fragmented (F-06/F-07). | Route manifest, accessibility scan, link-waiver manifest, screenshots, JSON receipt. **P1.** |
| Content migration CLI | Migration script/replay inputs are site-local (journey phase 6). | Sitemap/HTML import, route manifest, asset ledger, repeatability report. **P2.** |

## What this project proved and did not prove

**Proved:** a substantial static content migration; root-route preservation; custom collection pages; generated SEO/feed/sitemap/robots/`llms.txt`; source-first output; local deterministic build at 138 posts; semantic/token-based differentiation; and meaningful structural validation.

**Did not prove:** clean-machine setup, package installation/upgrade, deployment, live development, all SiteKit components, native taxonomy archives, redirects/collision handling, responsive image processing, future-post scheduling, untrusted-content safety, large-scale performance, automated visual/accessibility compliance, or use of the wider Kujo supporting-tool ecosystem.

Detailed execution backlog, incidents, tool verdicts, scorecard, issue drafts, and recommended workflows are split into the companion documents in this directory.
