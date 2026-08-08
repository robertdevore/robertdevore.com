# RobertDeVore.com / Kujo ecosystem launch-readiness scorecard

Scores use 1 = not ready, 2 = early, 3 = functional, 4 = strong, 5 = launch quality. Evidence details are in [the full postmortem](robertdevore-site-build-postmortem.md).

| Area | Score | Why |
| --- | ---: | --- |
| Kujo language/runtime (used slice) | 3 | Local build/runtime contracts pass; general language/runtime/package behavior was not tested. |
| Kujo CLI | 3 | Clear negative contracts; no project-local install or doctor workflow. |
| Kujo SSG core | 3 | Real 138-post site works; hardening and real-world integration gaps remain. |
| Theme architecture | 4 | Clear templates and successful distinct site overrides; upgrade safety unproven. |
| Frontmatter | 3 | Well-covered normal cases; documented delimiter robustness gap. |
| Routing | 4 | Root posts and custom collections are tested; collisions/redirect migration are incomplete. |
| Content collections | 4 | Projects and collection `llms.txt` work with contracts. |
| Taxonomies | 2 | No native term archives; site materializes content. |
| Asset pipeline | 2 | Local assets work; dependency/provenance/path hardening weak. |
| Image workflow | 2 | Legacy media is preserved; responsive derivative strategy is not proven. |
| SEO/schema/feed/sitemap/llms | 4 | Generated targets are validated; sitemap scale and external previews are unproven. |
| Development server/watch | 1 | `--watch` is unimplemented. |
| Production build | 3 | Clean local target build passes; clean-room/CI/deploy not proved. |
| Diagnostics | 3 | Good CLI failure contracts; setup failures lack doctor/provenance guidance. |
| Documentation | 2 | Strong source docs, but stale SSG audit/roadmap and missing consumer setup. |
| Testing | 3 | Good contracts and site checker; missing clean-room, visual/a11y and waiver gate. |
| SiteKit components | 4 | 85 source-validated components; target used semantic composition effectively. |
| SiteKit token system | 4 | Token/theme assets supported a coherent unique site. |
| SiteKit accessibility | 3 | Strong documented defaults; browser verification absent. |
| SiteKit customization | 4 | Site-specific composition stayed local; distribution/upgrade model remains weak. |
| Cross-repository integration | 1 | Absolute local paths, copied artifacts, no lock/provenance. |
| Agent usability | 2 | Searchable source and tests, but no context/receipt/handoff workflow. |
| Human developer usability | 2 | Build works after hidden setup; no real watch/install route. |
| Reproducibility | 1 | Environment-dependent. |
| Traceability | 2 | Good commits/docs/checkers; no command receipts or migration replay evidence. |
| Performance | 3 | 7.865 s target build; documented 10k limitations. |
| Security and safety | 2 | No incident observed; documented SSG hardening blockers remain. |
| **Overall ecosystem launch readiness** | **2** | Appropriate for a controlled beta with maintainer support, not broad launch. |

## P0/P1 blockers and gates

| Gate | Required before | Definition of done |
| --- | --- | --- |
| Pinned portable workspace | Public beta | One checkout/manifest, no absolute paths, cross-platform sync, clean CI proof. |
| SSG input/fetch hardening | Public beta for untrusted/third-party content | Path containment, network guard, delimiter parser, adversarial tests. |
| Visual/accessibility release receipt | Public beta | Versioned route/viewport/a11y run, screenshots/report, CI status. |
| Native taxonomy plan and documented interim | Broad launch | Either feature shipped or materialization explicitly supported with safe regeneration. |
| Watch/dev workflow | Broad launch | Working watch command or clearly documented/reproducible interim loop. |
