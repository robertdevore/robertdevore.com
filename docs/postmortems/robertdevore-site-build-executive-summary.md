# RobertDeVore.com build postmortem — executive summary

## Conclusion

The ecosystem is ready for a constrained, maintainer-supported beta; it is not ready for broad public launch. RobertDeVore.com demonstrates that Kujo SSG and SiteKit can deliver a credible, visually distinct 138-post static publishing site with route preservation, strong generated output, and a meaningful local validation layer. It does not demonstrate that a new developer can install, reproduce, upgrade, or safely operate the stack without hidden local knowledge.

The strongest parts are the transparent source-first static pipeline, root-level post routing, custom collections, generated metadata/auxiliary output, and SiteKit’s token/semantic composition. The weakest parts are cross-repository distribution, reproducibility, SSG hardening, developer watch mode, and release evidence for visual/accessibility quality.

The single biggest risk is that the published “workflow” depends on Robert’s absolute filesystem layout and local unpushed SSG state while presenting copied assets as integration. The single biggest advantage is that real-site requirements fed back into general SSG features with contract coverage instead of accumulating a site-specific framework.

## What the project proved

- 138 posts, 12 pages, six projects, five category archives, and six tag archives can be built as authored sources. A fresh local build completed in 7.865 seconds and generated 388 HTML files.
- Root post permalinks while retaining `/blog/` became SSG feature `posts_at_root` in `8641a71`, with an output contract.
- Custom collections can be included in `llms.txt`; `d17ed50` adds deterministic project collection output with tests.
- Target validation passed 195 primary-route checks and SSG structural validation passed 388 HTML files. SiteKit’s build/lint/validate/snapshot gate passed for 85 components.
- SiteKit can support a distinct editorial design without a JavaScript component runtime or upstream component changes.

## What it did not prove

- A clean-machine install, dependency upgrade, deployment, CI, or rollback.
- Working watch/live development, native taxonomy archives, redirect/collision tooling, image derivative processing, or large-scale behavior.
- Automated keyboard, screen-reader, contrast, motion, or visual-regression verification.
- Safe handling of untrusted content or remote asset URLs.
- Value from Lens, RunLedger, ShipCheck, ChangeBucket, Muzzle, PackWrite, CaseFile, Howl, Concord, Watchdog, or RAG/context tools; no usage receipts were found.

## Critical findings

1. **P0/S1 — Environment-dependent integration.** `scripts/build.sh` and `scripts/sync_dependencies.sh` default to absolute sibling checkout paths; sync uses BSD `sed`; dependencies are copied with no lock/provenance. The SSG checkout is locally ahead of its remote by `d17ed50`.
2. **P0/S1 — Documented SSG security hardening remains open.** Path escape, remote-fetch destination policy, and fragile frontmatter delimiter handling are recorded as P0 in `ssg/docs/enhancements-roadmap.md`.
3. **P1/S2 — No real dev watch mode.** `--watch` is deliberately a no-op; the target builds then starts a separate static server.
4. **P1/S2 — Taxonomy archives are a site workaround.** `content/category` and `content/tag` materialize derived archive content because native taxonomy archives do not exist.
5. **P1/S2 — Visual/accessibility review has no repeatable receipt.** PNGs and prose exist, but no route/viewport manifest, browser automation, scanner report, or CI gate does.
6. **P1/S3 — Documentation state is misleading.** SSG parity and roadmap documents describe several features as open after their implementation/tests changed.

## Strengths to preserve

- Source-first migration and ignored generated output.
- Contract tests that cover configuration precedence and generated routes/metadata.
- Root route and custom `llms.txt` improvements were generalized upstream.
- Token-driven, semantic SiteKit source model and 85-component validation.
- Target’s route/metadata/content-specific validator.
- Deliberate preservation of historic content rather than fabricated redirects.

## Next actions

1. Ship a pinned, cross-platform workspace/manifest plus a `site doctor`; test it in clean CI.
2. Close the three documented SSG hardening items with adversarial fixtures.
3. Create a single release verifier for build, routes, links/waivers, accessibility, visual QA, SEO/schema, and receipts.
4. Add native taxonomy archives and a migration path from materialized archives.
5. Implement watch mode or publish an honest interim dev workflow.
6. Reconcile stale SSG roadmap/parity documentation and declare a SiteKit distribution/upgrade model.

See [the full postmortem](robertdevore-site-build-postmortem.md), [launch scorecard](robertdevore-site-build-launch-readiness.md), and [action backlog](robertdevore-site-build-action-backlog.md).
