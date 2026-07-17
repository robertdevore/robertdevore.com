# Next migration readiness

## No-go until

- [ ] Restore or intentionally update `workspace-dependencies.json`; `doctor --json`, sync check, build, and site validation pass from a clean consumer workspace.
- [ ] Re-run QA-001 against the current site; resolve or explicitly waive its home-page contrast and image-link-name failures.
- [ ] Add a versioned broken-link waiver report; fail new/unapproved internal links.

## Recommended before implementation

- [ ] Capture source snapshot/checksums, crawl/sitemap, route inventory, page taxonomy, assets, SEO metadata, and redirect decisions before writing templates.
- [ ] Require a framework-capability review for taxonomies, routes/redirects, raw HTML, assets, and SiteKit consumption. Stop for approval on a gap.
- [ ] Publish an interim dev rebuild loop or implement/test SSG watch mode.
- [ ] Ship/document native taxonomy archives or explicitly approve materialized archives and their regeneration policy.
- [ ] Add a versioned SiteKit distribution/consumer fixture, including font path behavior.

## Required tests and automation

- [ ] Toolchain provenance + clean-room consumer build.
- [ ] Route diff, collision, alias, redirect, and canonical validation.
- [ ] Link checker with approved-exception baseline.
- [ ] Generated HTML/metadata/schema/assets validation.
- [ ] Lens/axe desktop and mobile receipt for home, long content, archive, project/service, contact, and 404.
- [ ] Output file/byte/hash and build-duration receipt.

## Prompt requirements

Ask for a discovery report and approval before implementation; name route preservation rules, canonical/redirect policy, content classification authority, design fidelity target, accessibility threshold, visual routes/viewports, toolchain versions, and the rule that an unimplemented SSG/SiteKit capability must be reported rather than locally simulated without approval.

## Second-run measurements

Capture discovery/planning/implementation/review time; interventions; framework changes; undocumented decisions; workarounds; build failures; route/link/SEO/a11y/visual issues; custom components/CSS overrides; test coverage; output size; and final receipts.

**Go recommendation:** No-go now. Go after the three gating checks above pass; taxonomy/watch work may be deferred only with an explicit next-site policy.

