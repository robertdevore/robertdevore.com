# Proposed golden path for an agent building a Kujo website

## Required repository contract

Every website repository should contain an `AGENTS.md` that identifies:

- canonical source, generated, and vendor paths;
- exact build/test/preview commands and expected exit behavior;
- workspace/lockfile and runtime requirements;
- content schema and route/redirect ownership;
- allowed write boundaries and deployment prohibition/approval boundary;
- visual/a11y/link release commands and artifact locations;
- command receipt, plan, and handoff locations.

## Agent sequence

1. Run `kujo site doctor --json` (**proposed**) and stop if required versions, clean worktree policy, or write boundaries cannot be established.
2. Read root instructions, lock/workspace manifest, architecture summary, content schema, route manifest, and prior handoff/context pack.
3. Create a concise plan and change ledger mapping each requirement to an owner repository, source path, expected test, and release effect.
4. Prefer existing SSG templates and SiteKit schemas/components. Record a proposed upstream change instead of silently copying a generic component or adding a platform workaround.
5. For migration, emit a route migration manifest and asset ledger before mutating content. Require human approval for destructive redirects, content deletion, publishing, external fetches, or cross-repository source changes.
6. Build in a disposable output path; keep a build receipt with command, runtime/version, config, source revision, duration, exit code, output hash, and warnings.
7. Run structural, routes, link-policy, accessibility, SEO/schema, visual, and performance checks; persist receipts. An agent must distinguish a warning waiver from a new warning.
8. Produce a PatchBrief-style change ledger and final handoff naming tests, artifacts, upstream candidates, risks, and unresolved decisions.

## Recommended supporting tools and contracts

| Tool | Use only when | Required input → output contract |
| --- | --- | --- |
| Doctor (proposed) | Every session | Workspace manifest → machine-readable prerequisite/compatibility report. |
| Context pack (Muzzle/PackWrite/Scent candidate) | Multi-repo work | Selected instructions/architecture/route/schema files → bounded, versioned context manifest. No raw transcript required. |
| RunLedger | Commands affect verification/release confidence | Command/version/cwd/input hashes → exit code, duration, output/artifact hashes. |
| ChangeBucket | Cross-repo or large diffs | Base/head → categorized changed files and blast radius. |
| Lens or equivalent | Visual/browser QA is required | Route/viewport/baseline manifest → screenshots, violations, pass/fail JSON. |
| ShipCheck or equivalent | Release gate | Required receipts/manifests → one no-deploy release verdict. |
| PatchBrief | Handoff/review | Git diff + test receipts → owner-aware concise summary. |
| CaseFile | A significant failure recurs | Sanitized command/error/environment evidence → reproducible incident bundle. |

No supporting tool should be required merely because it exists. This project provides no evidence that these tools were used; the recommendation closes specific traceability gaps found in the postmortem.

## Stop conditions and human approvals

Stop and request direction when a requirement would change public routes, discard historic content, fetch untrusted remote data, alter a dependency repository, or deploy/publish. Do not stop for normal source inspection, local disposable builds, or reversible validation. A failed build must not be represented as valid output; preserve its receipt and keep prior output clearly marked stale.
