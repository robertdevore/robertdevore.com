# KUJO postmortem remediation — final review

## Campaign verdict

**Partial.** The campaign completed the bounded portability, dependency,
frontmatter, local featured-image containment, documentation, and visual/a11y
receipt work. It did not meet a release-ready verdict because the first
accessibility receipt exposed serious home-page defects and several deliberate
P0/P1 items require broader work.

## Role lanes and handoffs

| Lane | Role | Agent | Outcome |
| --- | --- | --- | --- |
| Command, planning, synthesis | General Commander / Chief of Staff / Spec Writer / Systems Architect | Codex | Campaign contract, task/evidence/decision records, review. |
| Target portability | Tooling Developer | Codex subagent | Completed SITE-001, SITE-002, and AGENT-001. |
| SSG hardening | Core Developer | Codex subagent | Completed SSG-001, SSG-003, and SSG-007. |
| Visual release receipts | Visual QA Agent | Codex subagent | Implemented QA-001 and captured release-blocking findings. |
| Security, QA, release review | Security Reviewer / QA Lead / Release Verifier | Commander synthesis | Reviewed path-boundary diff, verification receipts, and release gate. |

Every implementation lane read its assigned role contract, reported inputs,
scope, changed files, commands, evidence, handoff target, and stop condition in
its completion handoff. `assignments.yml` records the operational form.

## Implemented changes

- Target portability: `workspace-dependencies.json`, portable workspace doctor
  and dependency synchronization, declared Python validator dependency, target
  `AGENTS.md`, and dependency documentation.
- SSG: delimiter-line-only frontmatter parsing with source diagnostics, canonical
  containment for local featured images, adversarial contract fixtures, a
  capability matrix, and a stale-document contract.
- Target QA: versioned representative route/spec manifest, local loopback
  404-aware static server, Lens runner, and receipt documentation.
- Postmortem/action backlog: this campaign update and machine-readable campaign
  artifacts.

## Files and artifacts

Target commits changed the target build/sync workflow, workspace manifest,
dependency docs, QA config/scripts, verification docs, and `AGENTS.md`.
SSG commits changed `build.kujo`, generated-output/docs contracts, SSG
roadmaps/audits, README, and the capability matrix. This campaign folder adds:

- `campaign.yml`
- `assignments.yml`
- `task-ledger.yml`
- `evidence-ledger.yml`
- `decisions.yml`
- `blockers.yml`
- `verification.yml`
- `remediation.spec.yml`
- `handoff-qa-001-visual-release-receipts.md`
- `strata-handoff.md`
- `final-review.md`

## Verification

| Check | Result |
| --- | --- |
| Target workspace doctor, sync check, build, validator | Passed: 138 posts, 12 pages, 195 routes; 73 existing historical-link warnings. |
| SSG CI with release runtime | Passed: CLI, generated-output, docs contracts, starter build, generated-output validation. |
| Visual/accessibility receipt | Failed: home has serious `color-contrast` (4 elements) and `link-name` (12 image links) findings at desktop and mobile; five other representative routes passed. |
| ShipCheck gate | Failed: 3 generic repository error checks (tests, version metadata, changelog) and 8 warnings. |
| SiteKit gate | Not run because the campaign did not change SiteKit. |
| Security review | Local featured-image containment is test-backed; remote-fetch destination policy remains open. |

The QA receipt is intentionally retained only as ignored local evidence under
`.lens/runs/`; its route-level report and finding IDs are indexed in the QA
handoff and evidence ledger.

## Risks and open backlog

- **Release blockers:** remediate the Lens home-page contrast and image-link
  accessible-name findings; add project-appropriate tests/version/changelog
  release metadata or treat ShipCheck as advisory for this website repository.
- **P0 security:** SSG-002 remote-fetch private-network and redirect policy is
  still open.
- **P1 product/integration:** SSG taxonomy archives/watch mode, SiteKit
  consumer-distribution contract, target broken-link waiver manifest, and
  clean-machine CI remain open.
- The 73 historical-link warnings remain known editorial debt rather than new
  regressions.

## Commits and authority

- Target: `16fee69 feat: add portable pinned site workspace`
- Target: `b736527 chore: pin hardened SSG workspace source`
- Target: `2d6e72d Add deterministic visual QA receipt workflow`
- SSG: `83e56b7 fix: harden featured images and frontmatter parsing`
- SSG: `a09a534 docs: reconcile current SSG capability status`

No commits were pushed. No deploy, publish, tag, or release action occurred.
