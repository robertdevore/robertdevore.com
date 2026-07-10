# RobertDeVore.com build postmortem — issue-ready drafts

## [SSG] Confine featured-image resolution to approved roots

- **Repository:** `kujolang/ssg`
- **Priority:** P0
- **Description:** Local `featured_image` resolution can escape content/asset/source roots using traversal paths, as documented in `docs/enhancements-roadmap.md` P0-1.
- **Evidence:** Current SSG roadmap; target migration consumes many historic assets.
- **Acceptance criteria:** canonical path containment; source file/field diagnostic; no outside-root read/copy; normal relative assets continue working.
- **Tests:** traversal fixture, symlink/canonicalization fixture, normal content/assets fixture.

## [SSG] Guard remote asset/font fetching against private-network destinations

- **Repository:** `kujolang/ssg` (with runtime support if necessary)
- **Priority:** P0
- **Description:** Trusted-mode remote fetch behavior has no default destination policy, creating an SSRF risk for untrusted frontmatter/config.
- **Evidence:** `docs/enhancements-roadmap.md` P0-2.
- **Acceptance criteria:** explicit policy/flag; loopback/RFC1918/link-local destinations rejected when enabled; redirects rechecked; documentation explains trusted/untrusted behavior.
- **Tests:** local/private/public URL fixtures and redirect fixture.

## [SSG] Parse frontmatter on delimiter lines, not arbitrary `---` substrings

- **Repository:** `kujolang/ssg`
- **Priority:** P0
- **Description:** Current roadmap records fragile frontmatter splitting when content contains `---`.
- **Evidence:** `docs/enhancements-roadmap.md` P0-3.
- **Acceptance criteria:** quoted/body `---` remains intact; malformed delimiters yield source diagnostics.
- **Tests:** three regression fixtures plus existing content suite.

## [SSG] Add first-class taxonomy archives

- **Repository:** `kujolang/ssg`
- **Priority:** P1
- **Description:** RobertDeVore.com materializes `content/category` and `content/tag` because categories/tags have no native archive generation.
- **Evidence:** `scripts/migrate_legacy.py`, target `content/category`, `content/tag`, and architecture record.
- **Acceptance criteria:** derived index/term routes, metadata/template context, pagination, slug normalization, collisions, drafts, sitemap/llms integration, documented migration.
- **Tests:** representative multi-term fixture with empty/collision/pagination cases.

## [SSG] Implement `--watch` or remove it from the supported-workflow surface

- **Repository:** `kujolang/ssg`
- **Priority:** P1
- **Description:** `--watch` is publicly listed as reserved/not implemented and performs one build only.
- **Evidence:** README, help text, and `build.kujo` warning.
- **Acceptance criteria:** documented watch roots, debounce behavior, non-zero failed rebuild status, and integration test; otherwise omit flag and publish a supported workaround.
- **Tests:** modify content/template/asset/config fixture and observe rebuilt output.

## [SiteKit] Ship a versioned consumer bundle/manifest

- **Repository:** `kujolang/site-kit`
- **Priority:** P1
- **Description:** SiteKit is private/source-only; target copies generated CSS/fonts without version/provenance or upgrade safety.
- **Evidence:** SiteKit README distribution section; target `scripts/sync_dependencies.sh`.
- **Acceptance criteria:** supported consumption mode, version/commit/hash manifest, consumer sync/install command, migration notes, integration fixture.
- **Tests:** clean consumer fixture verifies assets/tokens/font paths and detects version drift.

## [DX] Create a portable Kujo website workspace and doctor command

- **Repository:** cross-repository tooling (SSG/SiteKit)
- **Priority:** P0
- **Description:** Target defaults to absolute local paths and BSD `sed`; fresh setup cannot be inferred.
- **Evidence:** target `scripts/build.sh` and `scripts/sync_dependencies.sh`; SSG local `d17ed50` is ahead of remote.
- **Acceptance criteria:** lockable workspace, no absolute path defaults, cross-platform bootstrap/sync, machine-readable doctor, clean CI proof.
- **Tests:** arbitrary-path macOS/Linux clean-machine build.

## [Quality] Add release receipts for visual, accessibility, and link policy

- **Repository:** target reference workflow or shared release tool
- **Priority:** P1
- **Description:** Visual captures/prose exist, while 73 historic link warnings and accessibility claims lack repeatable release artifacts.
- **Evidence:** `reports/visual/`, `docs/verification.md`, `scripts/validate_site.py`.
- **Acceptance criteria:** route/viewport manifest, visual/a11y report, full link JSON with approved waivers, CI verdict.
- **Tests:** intentional visual/a11y/new-link regression causes failure; approved historic link remains visible but non-blocking.

## [Docs] Reconcile SSG roadmap and parity audit state

- **Repository:** `kujolang/ssg`
- **Priority:** P1
- **Description:** Historic audit lists capabilities as missing that current contract tests assert; roadmap checkboxes conflict with status prose.
- **Evidence:** `docs/parity-audit.md`, `ROADMAP.md`, `scripts/test-generated-contract.sh`.
- **Acceptance criteria:** superseded labels/commit references, one current capability matrix, review rule for stale action items.
- **Tests:** documentation CI checks current-feature references/links and known status markers.
