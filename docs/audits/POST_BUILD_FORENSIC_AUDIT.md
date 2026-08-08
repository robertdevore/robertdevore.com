# Kujo SSG + SiteKit post-build forensic audit

**Audit date:** 2026-07-17  
**Evidence boundary:** repository history through `6c5dd57`, current working tree, generated `output/`, pinned-workspace diagnostics, the SSG/SiteKit checkouts named by `workspace-dependencies.json`, and the earlier postmortem/remediation receipts. This is an evidence-led review; it does not claim visibility into an unavailable agent transcript, source-site snapshot, CI run, deployment, or elapsed-time log.

## 1. Executive summary

The migration succeeded as a source-first conversion of a previously committed static export into 167 authored Markdown files, 16 templates, SiteKit-based CSS, and a Kujo SSG build. It preserved 138 root-level post routes, added 12 pages, 6 projects, and materialized five category and six tag archives. Two real product gaps discovered during the work were fixed upstream in Kujo SSG: root-level post permalinks (`8641a71`) and custom collections in `llms.txt` (`d17ed50`). SiteKit itself was not changed.

The forensic result is more critical than the finished site: the initial migration relied on a fragile importer, materialized taxonomies, copied framework artifacts, a manual visual review, and an unrecorded discovery phase. A remediation pass made the workspace portable in source form, added a dependency lock, requirements, a doctor, and a Lens receipt workflow. However, the *current* checkout has advanced past the lock: `doctor` and `sync --check` now fail, and a direct build with the newer runtime/SSG combination stopped after partial output. That is a confirmed next-site blocker until the workspace lock is intentionally refreshed or the pinned revisions are restored.

**Assessment:** do not begin the next migration yet. Perform the small hardening pass in the readiness checklist, beginning with a reproducible clean build and an updated QA receipt. The SSG is capable for this site; its remaining recurring gaps are taxonomy archives, watch mode, migration-oriented route/redirect tooling, and a stronger consumer release boundary. SiteKit’s primary recurring gap is consumption/versioning, not visual expressiveness.

### Confidence vocabulary

- **Confirmed** — directly observed in source, commit, command, or receipt.
- **Strongly inferred** — supported by multiple artifacts but no command transcript.
- **Possible** — plausible, but not proven by available evidence.
- **Unknown** — the required evidence was absent.

## 2. Overall assessment and reconstruction

### Original architecture and conversion path

| Area | Reconstruction | Confidence / evidence |
| --- | --- | --- |
| Original site | A generated static export was committed: route directories with `index.html`, `sitemap.xml`, `llms.txt`, legacy CSS/JS, and roughly 1 GB of media variants; no source build configuration was found. | Confirmed: parent `7b562b9`, `docs/architecture.md`, `d703fc1` deletion list. |
| Discovery | `scripts/migrate_legacy.py` reads `llms.txt` for post/page inventory and `sitemap.xml` for dates, then reads route HTML. | Confirmed: importer source. The exact original crawl/sitemap interpretation session is unknown. |
| Classification | Posts came from the `## Posts` section; pages from `## Pages` plus a hard-coded `LEGACY_PAGES` set. Taxonomy was inferred from title/body keywords. | Confirmed: importer. This was manual policy encoded as heuristics, not source metadata recovery. |
| Transfer | BeautifulSoup removes scripts/styles/classes, rewrites URLs, converts selected HTML to Markdown with `html2text`, writes normalized frontmatter, appends three related links, and copies referenced assets by basename. | Confirmed: importer. Replay was not preserved because legacy input and an import receipt/checksum are absent. |
| Routing | `custom_url` preserves original root slugs; `posts_at_root` keeps posts at `/<slug>/` while the listing is `/blog/`. Legacy pages retain their routes. | Confirmed: migrated frontmatter, `build.kujo`, SSG commit `8641a71`. No redirects were required. |
| Layouts/components | Site templates select `signal-a/b/c`, archive, project, legacy, and page layouts. SiteKit supplies token/theme/component CSS; this site composes its own chrome, hero art, cards, navigation, and contact flow. | Confirmed: 16 templates and CSS imports. |
| Assets | Legacy media was retained at `assets/legacy-images`; new signal art uses desktop/mobile WebP with PNG fallback. Inter fonts were added after the first rebuild. | Confirmed: `bca635c`, assets, architecture record. |
| SEO/auxiliary | Per-item canonical/title/description, JSON-LD, RSS, sitemap, robots, and `llms.txt` are generated and site-validated. | Confirmed: frontmatter, generator, validator. |
| Validation | Structural target validation, SSG contracts, and a later Lens/axe receipt workflow were created. An earlier Lens receipt found home-page contrast and image-link-name failures; no later passing receipt is present. | Confirmed: `docs/verification.md`, QA-001 handoff. |

### Timeline and turning points

| Date / commit | Event and significance |
| --- | --- |
| Before 2026-07-10 | Static output was the tracked site. The available history does not reveal the original generator, discovery commands, or migration prompt. **Unknown.** |
| 2026-07-10 `d703fc1` | Source-first rebuild: legacy output removed, Kujo SSG source/config/templates/content/importer/SiteKit distribution added. |
| 2026-07-10 `bca635c` | First confirmed rework: missing Inter artifacts and an incorrect copied SiteKit font path were corrected; target validation was strengthened. |
| 2026-07-10 `1b283e6`–`a57dc9b` | Archive/navigation/content refinement; project landings and machine-readable project output added. These are deliberate content/product iterations, not proven framework failures. |
| 2026-07-10 SSG `8641a71`, `d17ed50` | Reusable SSG fixes driven by this site: root post URLs and custom collection output in `llms.txt`, each with contract coverage. |
| 2026-07-10 remediation | Dependency provenance, Python requirements, portable sync/doctor, and a deterministic visual QA workflow were added. QA-001 exposed real home accessibility defects rather than masking them. |
| 2026-07-14–15 | Theme/content refinements: typography/interactions, restructuring, scramble title vendor JS, and home/projects changes. |
| 2026-07-17 audit | The declared workspace lock no longer matches the live sibling repos. `doctor`/`sync --check` fail; a direct newer-runtime build produced only partial output. |

## 3. Kujo SSG audit

### What worked

- Project configuration, frontmatter, custom collections, pagination, templates, root routes, feeds, sitemap, robots, canonical/OG/JSON-LD, asset copying, and generated aliases worked for the target. **Confirmed** by sources, contract history, and the existing generated output.
- CLI/config contract coverage exists upstream, including malformed configuration and root-post behavior. **Confirmed** by SSG test history and prior postmortem evidence.
- Output is inspectable and has a targeted validator; it did not silently accept missing font assets after `bca635c`. **Confirmed.**

### Reusable SSG findings

| ID | Finding | Classification | Evidence and disposition |
| --- | --- | --- |
| SSG-001 | Root-level posts with a separate `/blog/` listing were initially unsupported. | Missing feature, **fixed upstream**. | `8641a71` changes README/config/build/contracts; target uses `posts_at_root`. Suitable generally. |
| SSG-002 | Custom collections were excluded from `llms.txt`. | Missing feature, **fixed upstream**. | `d17ed50` adds deterministic collection index/item output and tests; target projects depend on it. |
| SSG-003 | Category/tag archives are manually materialized. No first-class taxonomy term generation, normalization/collision policy, pagination, or migration path exists. | Missing feature; open. | `content/category`, `content/tag`, importer `archives()`. High recurrence for publishing migrations. |
| SSG-004 | `--watch` is advertised as reserved/not implemented. | Missing feature / documentation clarity issue; open. | Current `build.kujo --help`; ordinary editing requires rebuild + separate server. |
| SSG-005 | No reusable migration route inventory, route-collision, redirect-map, or legacy-link-waiver capability was used. | Migration-tooling opportunity; open. | Importer and site validator implement narrow versions. |
| SSG-006 | Current pinned workspace cannot be reproduced from the active sibling checkouts. | Release/integration testing gap; open, blocker. | 2026-07-17 `workspace.py doctor --json` and `sync --check` report runtime/SSG/SiteKit revision/hash drift. This is not evidence that the SSG parser is broken. |
| SSG-007 | Direct build against the newer available runtime began rendering but did not complete, leaving 535 files and `.kujo-*.tmp` rather than the current 873-file output. | Compatibility/reproducibility issue; **possible root cause**, blocker. | Reproduced 2026-07-17; no final error text or compatible pinned checkout was available, so exact cause is Unknown. Do not diagnose as an SSG bug without a pinned-revision rerun. |
| SSG-008 | SSG has no demonstrated responsive-image derivative/fingerprinting pipeline in this migration. | Missing feature or capability not exercised; Unknown. | Hero derivatives were supplied manually; legacy assets were copied. |
| SSG-009 | Draft/scheduled/future-content, redirect collisions, deleted-content cleanup, incremental builds, and deterministic rebuild hashes were not exercised. | Testing gap; Unknown. | No receipt/fixture for these cases in target evidence. |

### SSG details by requested area

Configuration is now discoverable through `kujo-ssg.yml`, README, and the site doctor, but the lock drift proves that configuration alone is insufficient: tool/runtime compatibility must be atomically resolvable. Content supports the needed scalar/array frontmatter; its importer writes repetitive per-file canonical, author, template, and `nav_hide` values. The source does not prove nested-object/date validation quality. Template composition was sufficient, although template selection is a string frontmatter convention and no rendered-template error from the migration was retained. Collections worked for projects but were repurposed as a taxonomy compatibility layer.

Asset copying is adequate for local assets, but the initial font correction proves the consumer boundary was fragile. The normal `scripts/build.sh` clears `output/`, reducing stale-output risk when it can run; direct compatibility testing did not complete. SEO coverage is strong at the target level, but most guarantees come from a custom validator rather than a declared generic SSG schema. Build performance is only historically measured: 7.865 seconds for 138 posts/12 pages on this machine in the earlier record. No current comparable completed build is available because of lock drift.

## 4. SiteKit audit

### What worked

SiteKit tokens, the Kujo Light theme, reset/base/components/utilities, skip link, navigation, cards, metadata, buttons, code/table treatment, and form styles were enough to create a distinct editorial system without SiteKit source changes. The target uses 95 unique custom CSS selectors in `assets/css/site.css`; that is expected theme composition, not evidence of a component failure. **Confirmed** by assets/templates and the prior SiteKit gate (85 components passed).

### Findings

| ID | Finding | Classification | Evidence and disposition |
| --- | --- | --- |
| SITEKIT-001 | The initial copied distribution omitted Inter assets and needed a font URL rewrite. | Consumer packaging/default gap, **locally fixed**. | `bca635c`; later workspace manifest encodes `rewrite_sitekit_font_paths`. A generic consumer smoke test is needed. |
| SITEKIT-002 | Consumption is vendored CSS/fonts plus a site-specific transform, rather than a released consumer package/bundle with compatibility metadata. | Documentation/release-boundary gap; open. | `workspace-dependencies.json`, SiteKit `ca3e1d4`; latest SiteKit has later consumer-dashboard work but is not the pinned source. |
| SITEKIT-003 | Initial QA-001 found home-page contrast and image-link accessible-name violations. | Accessibility issue, status uncertain after later CSS/template changes. | QA handoff records failure; no later passing receipt. This belongs primarily to target theme composition, with SiteKit’s consumer examples a secondary opportunity. |
| SITEKIT-004 | Hero art, title strokes, archive/project grids, and responsive crop positions are custom CSS rather than configurable SiteKit variants. | Site-specific requirement, not a framework defect. | `assets/css/site.css`; no need to upstream brand-specific signal-art components. |
| SITEKIT-005 | SiteKit does not prove component use through a typed/template adapter in this SSG. | Example/documentation gap; open. | This site applies classes/composition directly. A Kujo SSG consumer example would reduce ambiguity. |

CSS is predictable enough to inspect (the existing output contains 28,764 bytes of `site.css` and 111,641 bytes of unminified SiteKit component CSS). The source order is intentionally layered: SiteKit precedes the site theme, so overrides are stable only as long as SiteKit’s layer/selector contract remains stable. The site has progressive enhancement and reduced-motion styles, but keyboard/focus/contrast claims must be re-receipted after later changes. No evidence shows unnecessary framework JavaScript; the only added third-party code is the vendored scramble decoder, a site choice.

## 5. Site-specific findings and hidden workarounds

| Workaround | Why / underlying limitation | Safety and long-term disposition |
| --- | --- | --- |
| Materialized category/tag Markdown | SSG lacks native taxonomies; importer derives archives from posts. | Safe for a static snapshot, fragile for future edits because derived data drifts. Move to SSG taxonomy support; retain manual files only for editorial overrides. |
| Keyword taxonomy inference | Legacy HTML did not provide preserved structured taxonomy in the importer path. | Unsafe as a general importer classifier; review/approve a generated classification manifest before writing content. Site-specific source ambiguity, reusable tooling opportunity. |
| Hard-coded `LEGACY_PAGES` and required-route lists | Original inventory was incomplete/heterogeneous. | Maintainable only for this finite corpus. Replace with an explicit route inventory/redirect manifest generated during discovery. |
| Per-file canonical/author/template/nav_hide | SSG defaults/schema were not used for those common fields. | Safe but repetitive. Consider site defaults/collection schemas; do not require a site-specific SSG feature without a second use case. |
| `rewrite_sitekit_font_paths` transform | SiteKit distribution’s relative font location differed from this site's asset location. | Safe and hash-checked, but a consumer adapter/release bundle should own it. |
| 73 historic broken-link warnings | Fidelity policy avoids fabricating targets. | The most dangerous remaining hidden workaround: new regressions can hide among warnings. Replace with a versioned waiver manifest that fails new/unapproved links. |
| Dead “richer normalization” code after `return` in importer | Raw trusted HTML support was unavailable/avoided. | Harmless at runtime but misleading maintenance debt. Remove or promote only with tests when raw HTML is supported. |
| `related reading` appended by category/date | SSG lacks a relation/query model and original related links were not retained. | Safe but editorially generic; make it an explicit migration policy and review sampled results. |

No regex HTML post-processing, empty catches, disabled validation, or manually maintained sitemap entries were found in canonical source. The importer does use HTML parsing/URL rewriting and a basename asset copy; basename collisions are a **possible** risk not covered by evidence.

## 6. Framework changes caused by the migration

| Repository | Change | Reference | Completeness |
| --- | --- | --- | --- |
| Kujo SSG | `posts_at_root` option/config/docs/contract. | `8641a71` | Complete for the demonstrated route shape; tests/docs added; backward compatible default false. General-purpose. |
| Kujo SSG | Custom collections in `llms.txt`. | `d17ed50` | Complete for demonstrated collections; tests/docs added. General-purpose. |
| Kujo SSG | Featured-image/frontmatter hardening and capability-doc reconciliation after the first postmortem. | `83e56b7`, `a09a534` | Strongly inferred remediation linkage; target lock pins `a09a534`. Revalidate in a clean pinned workspace. |
| SiteKit | No site-driven source change located. | Target history + SiteKit history | The font-path issue was fixed at the target consumer boundary, not upstream. |
| This site | Dependency lock/doctor/sync, requirements, Lens receipt workflow, theme/content refinements. | `16fee69`, `2d6e72d`, `9545005`–`6c5dd57` | Useful local remediation; current lock needs a controlled update. |

## 7. Original migration prompt assessment

The original mega prompt was not retained, so an item-by-item assessment is **Unknown**. The evidence shows it likely specified a finished visual rebuild but did not force a phase gate for route inventory, source capture, taxonomy policy, dependency provenance, or receipt logging; this is **strongly inferred** from the missing artifacts and subsequent remediation.

A better prompt must require: (1) read-only discovery and a signed route/content/asset/SEO inventory before editing; (2) capability-gap approval before a workaround; (3) a declared source snapshot/checksum and import receipt; (4) a lockable toolchain; (5) exact visual/a11y route/viewport acceptance criteria; (6) a redirect/waiver policy; and (7) an end report distinguishing site decisions from upstream changes. The agent must stop and report—not silently work around—missing taxonomy generation, route collisions/aliases/redirect behavior, asset path transforms, raw-HTML sanitization, untracked framework modification, or a failed release receipt.

## 8. Metrics and limits

| Metric | Value | Confidence / note |
| --- | ---: | --- |
| Posts / pages / projects / category archives / tag archives | 138 / 12 / 6 / 5 / 6 | Confirmed from `content/`. |
| Authored Markdown files | 167 | Confirmed. |
| Templates | 16 | Confirmed. |
| Redirects | 0 | Confirmed in migration record; flat `.html` aliases are generated compatibility output, not redirects counted here. |
| Content types | 5 practical types (posts, pages, projects, category, tag) | Confirmed. |
| Custom migration scripts | 1 (`migrate_legacy.py`) | Confirmed; validation/QA helpers are not importers. |
| Known rework cycles | 1 minimum (fonts/path), multiple later refinement commits | Confirmed minimum; exact retry count Unknown. |
| Framework changes | 2 direct SSG features; 0 direct SiteKit changes | Confirmed. |
| Known historic link warnings | 73 | Confirmed by prior validated receipt; must be rechecked after lock repair. |
| Unresolved TODOs in canonical source | 0 explicit migration TODOs; dead importer compatibility block remains | Confirmed search, excluding Git samples/output. |
| Historical completed build | 7.865 s; 388 HTML files | Confirmed prior receipt, machine-specific. |
| Current build status | Normal build blocked by lock drift; direct newer-runtime attempt partial | Confirmed audit run. |
| Current generated output | 873 files; 209,004 KB | Confirmed existing generated output; generated files are not source of truth. |
| Legacy media | 199,284 KB | Confirmed current disk measure. |
| Site CSS / JS (existing output) | 28,764 B / 7,168 B | Confirmed; differs from older authored measurements after refinements. |
| SiteKit CSS (unminified components) | 111,641 B | Confirmed existing output. |
| Lighthouse / HTML validator | Unavailable | No receipt/tool result. |
| Automated accessibility | QA-001 ran and failed home checks; no final pass | Confirmed. |

## 9. Prioritized issue register

The authoritative machine-readable register is [`POST_BUILD_ISSUES.json`](POST_BUILD_ISSUES.json). This table includes every required decision field; evidence is abbreviated here and fully preserved in JSON.

| ID | Finding | Scope | Type | Evidence | Status | Severity | Recurrence | Impact | Current workaround | Recommended solution | Target repo | Effort | Blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MIG-001 | Lock/live dependency drift | Migration | Testing gap | doctor + sync check, 2026-07-17 | Open | Critical | High | Normal build refuses | None | Atomic lock update/restore + clean build | Site/workspace | Small | Yes |
| MIG-002 | New-toolchain build partial | Migration | Compatibility issue | 535-file temp output, `.kujo-*.tmp` | Uncertain | High | Medium | Incomplete publish risk | Use verified pins | Reproduce pinned; capture cause; compatibility contract | SSG/runtime/site | Investigation | Yes |
| SSG-003 | No native taxonomies | SSG | Missing feature | materialized category/tag content/importer | Open | High | High | Derived content drift | Generate archive Markdown | Native terms, pagination, collisions, migration fixture | Kujo SSG | Large | No |
| SSG-004 | Watch unavailable | SSG | Missing feature | `--watch` help | Open | Medium | High | Slow/manual edit loop | Manual rebuild/server | Tested watch or documented loop | Kujo SSG | Medium | No |
| SSG-005 | No migration route tooling | Tooling | Enhancement | importer/validator are local | Open | Medium | High | Repeated bespoke policy | Hard-coded lists | Route/redirect/collision/waiver CLI | SSG/tooling | Large | No |
| SITEKIT-001 | Asset layout requires transform | SiteKit | Poor default | `bca635c`, manifest transform | Partially fixed | High | High | Broken fonts risk | Hash-checked rewrite | Stable consumer bundle + smoke test | SiteKit | Medium | Yes |
| SITEKIT-002 | No consumer release contract | SiteKit | Documentation gap | vendored artifacts/lock | Open | Medium | High | Upgrade ambiguity | Site-owned manifest | Versioned bundle, compatibility metadata | SiteKit | Medium | Yes |
| QA-001 | Latest a11y receipt failed | Site-specific | Accessibility issue | QA-001 handoff | Open | High | Medium | Unproven release accessibility | Structural/manual review | Re-run and fix/waive findings | Site | Small | Yes |
| MIG-003 | Link debt unbaselined | Migration | Testing gap | validator 73 warnings | Open | High | High | New breakage masked | Pass warnings; first 20 print | Reviewed JSON waiver, fail new | Site/tooling | Small | Yes |
| MIG-004 | Import not replayable | Migration | Workaround | importer + CSV, no snapshot receipt | Open | Medium | High | Lost audit/replay evidence | Converted content only | Snapshot hashes + import receipt | Tooling | Small | No |
| MIG-005 | Taxonomy heuristic | Migration | Workaround | `taxonomy()` keyword branches | Open | Medium | High | Misclassification | Fixed keywords/default term | Extract source terms or approve manifest | Tooling | Medium | No |
| DOC-001 | No tested consumer example | Documentation | Example gap | lock + cross-repo history | Open | Medium | High | Agents infer conventions | Site-local docs | Versioned SSG+SiteKit fixture/matrix | SSG/SiteKit | Medium | Yes |
| MIG-006 | Dead importer normalization block | Migration | Workaround | code after `return` | Open | Low | Medium | Misleading maintenance | Simple Markdown path | Remove or test/feature-flag | Site/tooling | Small | No |
| SSG-006 | Image/determinism not exercised | SSG | Testing gap | manual derivatives/no receipt | Uncertain | Medium | Medium | Future ad hoc asset/output behavior | Copy/manual variants | Image + deletion + hash fixtures | Kujo SSG | Investigation | No |

## 10. Preparation plan

### Must fix before the next migration

1. **Restore reproducibility** — owner: website workspace + Kujo release engineering. Either resolve the sibling repos to the manifest revisions or deliberately update revisions/hashes/artifacts, then pass doctor, sync check, build, target validation, and a clean-directory consumer test. Document the upgrade procedure. Success: zero lock mismatches and deterministic output comparison.
2. **Close the QA gate** — owner: site theme. Re-run QA-001 after current changes; fix contrast/image-link-name findings or retain a justified waiver. Require axe results, screenshots, viewport manifest, and receipt. Success: zero error-threshold findings on defined routes.
3. **Baseline link debt** — owner: migration tooling/content. Emit complete JSON, approve each historical exception with route/reason, and fail new internal breakage. Success: new broken link fails while an approved historical link is visible but non-blocking.

### Should fix before the next migration

1. Add an SSG taxonomy archive design (term normalization, collisions, empty terms, pagination, override rules) plus migration fixture/docs. Test conversion from materialized archives.
2. Choose a SiteKit consumption contract (versioned distribution bundle/manifest is sufficient initially) and add a SSG consumer fixture with the font-path contract.
3. Capture discovery artifacts: source snapshot ID, sitemap/route inventory, page classifications, asset inventory, metadata matrix, redirect decisions, and importer result hashes.
4. Publish an honest interim dev loop or implement `--watch`; test changed content/template/asset/config behavior and failed rebuild visibility.

### Can be tested during the next migration

1. Generic route collision/redirect-map importer and a route-diff report.
2. Asset derivative/fingerprint policy and basename-collision detection.
3. Optional frontmatter defaults/schema validation after two diverse content models prove the common shape.

### Longer-term improvements

1. First-class taxonomies, related-content query support, responsive images, scheduled-content policy, incremental build/determinism suite.
2. A packaged SiteKit release with component/API compatibility reporting and SSG integration docs.
3. A `kujo site audit` command that joins crawler/import/route/SEO/link/a11y/visual receipts.

## 11. Second-run benchmark and receipt

Use this site as baseline, but do not compare unverifiable elapsed time. Automatically collect: command start/end/exit code, tool revisions and hashes, route/page/content/asset counts, import exceptions, route diff/redirect count, framework modifications, documented decisions, workarounds, build failures, output files/bytes/hash, link-waiver deltas, axe errors, visual-diff count, template/component/custom-selector counts, and test/receipt outcomes. Humans record content corrections and material design discrepancies using stable IDs.

Compare discovery, planning, implementation, and review durations only when a timestamped receipt exists. The second migration is successful when it has fewer undocumented decisions/workarounds and no increase in validation exceptions, rather than merely a faster build.

Use [`MIGRATION_RECEIPT_TEMPLATE.md`](MIGRATION_RECEIPT_TEMPLATE.md) as an append-only log. A minimal record is: step, UTC start/end, command, input/source IDs, result/exit code, error, diagnosis, files changed, framework limitation, workaround, permanent fix reference, validation result, and owner/next action. Store command output by artifact path/hash, not as an unbounded transcript.

## 12. Final readiness recommendation

**Recommendation: begin the next site after a small hardening pass, not now.** The current lock/build and failed/obsolete QA evidence are gating defects. Native taxonomy and watch mode are important recurring SSG work but can be consciously deferred only when the next site has a documented materialized-taxonomy policy and manual rebuild workflow. Do not make another migration the vehicle for silently repairing framework or consumer-boundary behavior.
