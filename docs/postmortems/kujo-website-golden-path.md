# Proposed golden path: build a website with Kujo

This is a proposed workflow, not a claim that every command exists today. “Proposed” marks missing ecosystem features.

| Step | Command/tool | Input → output | Verification / failure condition | Handoff artifact |
| --- | --- | --- | --- | --- |
| 1. Initialize workspace | **Proposed:** `kujo site init --workspace` | Site name, SSG/SiteKit versions → repo, lock manifest, starter site | Fails if runtime/dependency versions unresolved | `kujo-site.lock` |
| 2. Environment doctor | **Proposed:** `kujo site doctor --json` | Workspace → runtime, Node, Python, capability, writable-output report | Non-zero on missing/pinned mismatch | `doctor.json` |
| 3. Create/choose theme | SSG template directory + SiteKit bundle | Theme name/tokens → `templates/`, token override | Build sample route; validate token/source manifest | `theme-manifest.json` |
| 4. Set content schema | `kujo run build.kujo -- --init yml` today; schema inspector proposed | Site config/frontmatter requirements → checked config | Invalid schema/unknown field reports file/line | `content-schema.json` |
| 5. Import content | **Proposed:** `kujo site migrate` | Sitemap/HTML/assets → Markdown, route map, asset ledger | Route count/checksum and rejected-content report | `migration-manifest.json` |
| 6. Preserve routes | **Proposed:** `kujo site routes check` | Existing/public routes + redirects → collision/redirect report | Fail collisions, missing required routes, redirect loops | `routes.json` |
| 7. Process assets | **Proposed:** `kujo site assets build` | Local images/fonts → validated/derived assets | Fail path escapes, missing dimensions, unsupported asset refs | `asset-manifest.json` |
| 8. Develop | **Proposed:** `kujo site dev` | Content/templates/assets changes → debounced rebuild and preview | Display prior valid build vs current build failure distinctly | `dev-receipt.json` |
| 9. Build | `kujo run ./build.kujo -- --site-url …` | Sources → isolated output directory | Non-zero on any generation failure; no source overwrite | `build-receipt.json` |
| 10. Structural validation | `ssg/scripts/validate-generated-output.sh output` plus target checks | Output → HTML/auxiliary contract results | Fail malformed/missing generated artifacts | `structure-report.json` |
| 11. Accessibility | **Proposed:** `kujo site a11y` | Route/viewport manifest → violations and DOM evidence | Fail configured severity threshold | `a11y-report.json` |
| 12. SEO/schema | **Proposed:** `kujo site seo check` | Output → metadata/schema/feed/sitemap checks | Fail invalid JSON-LD/canonicals/route mismatch | `seo-report.json` |
| 13. Visual QA | **Proposed:** `kujo site visual check` | Route/viewport/baselines → screenshots/diff | Fail approved-diff threshold | `visual-report.json` |
| 14. Link policy | **Proposed:** `kujo site links check` | Output + waiver manifest → new/known broken-link report | Fail new links, never hide approved historic links | `links-report.json` |
| 15. Performance | **Proposed:** `kujo site perf` | Key routes/build fixture → budgets | Fail explicit budgets only | `performance-report.json` |
| 16. Release | **Proposed:** `kujo site release check` | All receipts → signed/linked gate summary | No deploy; non-zero when any required receipt absent | `release-receipt.json` |

## Clean-room checklist

1. Clone the target repository and obtain its workspace lock; do not depend on a parent directory name.
2. Install the declared Kujo runtime version, Node/npm version, and Python validation environment.
3. Resolve SiteKit and SSG from the recorded commits/bundles, verify hashes, and record any local patch.
4. Run doctor, then build in a fresh temporary output directory.
5. Run structure, routes, link-waiver, SEO/schema, a11y, visual, and performance gates.
6. Compare output route manifest to the migration manifest; then publish only the validated output directory.

Until the proposed commands exist, use the current target build and validator with explicit `KUJO_BIN`, then record every command/result externally. Do not treat copied assets or a locally built sibling runtime as a portable installation.
