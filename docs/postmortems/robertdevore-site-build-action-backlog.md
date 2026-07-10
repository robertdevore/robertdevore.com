# RobertDeVore.com build postmortem — actionable backlog

## Remediation update — 2026-07-10 campaign

The local remediation campaign closed the feasible, bounded portions of the
portable-workspace and SSG-hardening work. The target now has a pinned
`workspace-dependencies.json`, portable build/sync entrypoints, a
machine-readable doctor, declared BeautifulSoup validation dependency, and an
agent handoff contract. SSG now confines local featured-image sources to
approved roots and parses frontmatter on delimiter lines; its current capability
docs are covered by a documentation contract. The target also has a versioned
Lens route/viewport receipt workflow.

The first receipt correctly found serious home-page color-contrast and
discernible-link-name violations, so the receipt mechanism is complete but the
release gate remains blocked pending frontend remediation. Remote-fetch
destination policy, native taxonomy archives, watch mode, SiteKit's consumer
distribution model, link-waiver policy, and clean-machine CI remain open.

| Item | Campaign status | Evidence |
| --- | --- | --- |
| SITE-001 | Completed locally | `workspace-dependencies.json`, `scripts/workspace.py`, `scripts/sync_dependencies.py`; target doctor/sync/build/validator passed. |
| SITE-002 | Completed locally | `requirements.txt` pins BeautifulSoup; doctor verifies it is importable. |
| SSG-001 | Completed locally | SSG commit `83e56b7` plus generated-output containment fixture. |
| SSG-003 | Completed locally | SSG commit `83e56b7` plus delimiter/body/malformed-frontmatter fixtures. |
| SSG-007 | Completed locally | SSG commit `a09a534`, capability matrix, and documentation contract. |
| QA-001 | Implemented; release blocked | Target commit `2d6e72d`; Lens found home-page contrast and image-link-name violations. |
| SSG-002, SSG-004, SSG-005, SK-001, SK-002, SITE-003 | Open | Require broader security, product, distribution, or content-policy work. |

## Kujo SSG / runtime

### SSG-001 — Constrain local featured-image paths

- **Problem/evidence:** `docs/enhancements-roadmap.md` records that local featured-image resolution can escape allowed roots.
- **Classification:** C; **severity/priority:** S1/P0; **size:** M; **timing:** before public beta.
- **Likely surface:** `ssg/build.kujo` image-source resolution; runtime path helpers if needed.
- **Acceptance/tests:** canonicalized candidate must remain under allowed content/assets/source roots; traversal fixture is rejected with file/field diagnostic; normal relative paths still pass.
- **Docs/owner:** security section in SSG README; SSG maintainer.

### SSG-002 — Add remote-fetch destination policy

- **Problem/evidence:** trusted-mode remote image/font fetches lack a default private-network policy per SSG roadmap.
- **Classification:** C; **severity/priority:** S1/P0; **size:** M; **timing:** before public beta.
- **Solution:** explicit deny-private-net option/policy, documented trusted/untrusted behavior, host/IP revalidation after redirects.
- **Acceptance/tests:** loopback/RFC1918/link-local fixture is rejected when guard enabled; public fixture works only with explicit network capability.
- **Owner:** SSG/runtime maintainers.

### SSG-003 — Use delimiter-aware frontmatter parsing

- **Problem/evidence:** roadmap reports `split(content, "---")` fragility.
- **Classification:** C; **severity/priority:** S1/P0; **size:** S; **timing:** before public beta.
- **Acceptance/tests:** `---` in quoted frontmatter/body content round-trips; malformed delimiters name source file/line; existing fixture behavior remains.
- **Owner:** SSG maintainer.

### SSG-004 — Implement native taxonomy archives

- **Problem/evidence:** target materializes `content/category` and `content/tag` archives.
- **Classification:** C; **severity/priority:** S2/P1; **size:** L; **timing:** before stable release.
- **Solution:** derive term routes from post frontmatter with metadata, sorting, pagination, slug/collision validation, empty-term policy, and template context.
- **Acceptance/tests:** fixture covers duplicate/case-normalized terms, empty archive policy, pagination, conflicts, drafts, sitemap/llms behavior, and migration from materialized archives.
- **Docs/owner:** taxonomy guide + migration note; SSG maintainer.

### SSG-005 — Deliver a real watch/dev workflow

- **Problem/evidence:** `--watch` is documented as unimplemented.
- **Classification:** C; **severity/priority:** S2/P1; **size:** M; **timing:** before public beta.
- **Acceptance/tests:** detects content/template/asset/config changes, debounces rebuilds, preserves non-zero error state, and documents reload behavior. Integration test observes a changed output file.
- **Owner:** SSG maintainer.

### SSG-006 — Publish scale and sitemap safeguards

- **Problem/evidence:** SSG report documents 10k performance limitations and no sitemap index.
- **Classification:** C/P; **severity/priority:** S3/P2; **size:** L; **timing:** before large-site claims.
- **Acceptance/tests:** reproducible 100/1k/10k benchmark script; sitemap sharding above standard limit; report wall time/memory/serial-finalize share.
- **Owner:** runtime + SSG maintainers.

### SSG-007 — Reconcile current documentation state

- **Problem/evidence:** parity audit describes features now asserted by current contracts; roadmap checkbox/status mismatch.
- **Classification:** D; **severity/priority:** S3/P1; **size:** S; **timing:** before public beta.
- **Acceptance/tests:** historic documents label superseded findings/commits; a current capability matrix links each supported feature to contract coverage; documentation check prevents stale “open” status.
- **Owner:** SSG docs maintainer.

## SiteKit / integration

### SK-001 — Define a versioned consumer distribution contract

- **Problem/evidence:** SiteKit is explicitly private/source-only; target copies generated CSS/fonts and patches paths.
- **Classification:** I; **severity/priority:** S2/P1; **size:** L; **timing:** before public beta.
- **Solution:** choose package, tarball, vendored release bundle, or workspace model; include version/commit/hashes and compatibility policy.
- **Acceptance/tests:** consumer fixture installs/syncs a pinned release, verifies generated CSS/font hashes, and produces a migration report on upgrade.
- **Owner:** SiteKit release engineering.

### SK-002 — Add a real consuming-site integration fixture

- **Problem/evidence:** SiteKit gate validates source components but not the copied distribution in an SSG site.
- **Classification:** I/P; **severity/priority:** S2/P1; **size:** M; **timing:** before public beta.
- **Acceptance/tests:** fixture builds SSG + SiteKit bundle, checks font URLs, tokens, landmarks, focus rules, and no missing copied assets.
- **Owner:** SiteKit + SSG maintainers.

## Target site / developer workflow

### SITE-001 — Replace absolute dependency paths with a workspace manifest and doctor

- **Problem/evidence:** target build/sync scripts encode `/Users/robertdevore/...` paths and BSD `sed`.
- **Classification:** I/N; **severity/priority:** S1/P0; **size:** M; **timing:** before public beta.
- **Solution:** project-local manifest/lock, environment overrides, portable file rewrite, clear missing-version diagnostics.
- **Acceptance/tests:** clone into arbitrary path on macOS/Linux clean CI, bootstrap runtime/dependencies, build and validate without edits.
- **Owner:** cross-repository release engineering.

### SITE-002 — Declare validation dependencies

- **Problem/evidence:** `validate_site.py` imports BeautifulSoup with no dependency file.
- **Classification:** I; **severity/priority:** S3/P1; **size:** XS; **timing:** before public beta.
- **Acceptance/tests:** pinned Python dependency/bootstrap command and fresh virtual-environment validator run.
- **Owner:** target site maintainer.

### SITE-003 — Introduce a broken-link waiver manifest

- **Problem/evidence:** 73 warnings are tolerated without full persistent classification.
- **Classification:** M/P; **severity/priority:** S3/P1; **size:** S; **timing:** before public beta.
- **Acceptance/tests:** checker writes full JSON, known historic entries are explicitly waived, new links fail; periodic waiver review is documented.
- **Owner:** target site/content maintainer.

## Testing, release, and agent workflow

### QA-001 — Create a receipt-backed visual/accessibility release gate

- **Problem/evidence:** retained screenshots/prose exist but no repeatable command/report.
- **Classification:** P/J; **severity/priority:** S2/P1; **size:** M; **timing:** before public beta.
- **Acceptance/tests:** route/viewport manifest covers home, long post, archive, project, contact, 404, mobile navigation; reports keyboard/focus/a11y violations; screenshots and verdict committed or attached to CI.
- **Owner:** quality engineering.

### AGENT-001 — Establish the agent website handoff contract

- **Problem/evidence:** no plan, RunLedger, context pack, command receipt, or final handoff artifact was found.
- **Classification:** J; **severity/priority:** S3/P1; **size:** M; **timing:** before public beta.
- **Acceptance/tests:** `AGENTS.md` template, context/route/change/build/test/visual receipts, stop conditions, and an example replay session.
- **Owner:** DX/agent workflow maintainer.

### REF-001 — Make this site a maintained reference fixture

- **Problem/evidence:** the target uniquely exercises root posts, custom collections, historic migration, rich metadata, and SiteKit composition.
- **Classification:** P; **severity/priority:** S3/P2; **size:** M; **timing:** after beta.
- **Acceptance/tests:** minimized fixture or protected reference branch runs cross-repo build/route/metadata/a11y checks; content media is scoped to avoid a 1.1 GB CI fixture.
- **Owner:** SSG + SiteKit maintainers.
