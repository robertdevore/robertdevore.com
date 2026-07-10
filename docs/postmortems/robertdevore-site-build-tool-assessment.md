# RobertDeVore.com build tool assessment

| Tool or system | Intended purpose | Actual evidence | Trustworthiness / integration | Verdict |
| --- | --- | --- | --- | --- |
| Kujo runtime CLI | Execute the SSG program. | Target and starter SSG builds passed using local `target/release/kujo`; CLI/generated contracts passed. | Output is actionable; binary path is hardcoded in target build. | Essential |
| Kujo SSG | Source-to-static-site pipeline. | 138/12 target build, 388 output pages, root routes, collections, metadata/aux output, target/SSG validation. | Strong tested pipeline; missing watch, taxonomy archives, hardening, and portable distribution. | Essential |
| SiteKit | Tokens, components, semantic/accessibility baseline. | Target vendors generated CSS/fonts; SiteKit gate passed for 85 components. | Helpful and composable; source-only consumer model is not reproducible enough. | Strongly beneficial |
| `scripts/migrate_legacy.py` | Convert historic inventory/HTML to authored Markdown. | Present with route CSV and migrated content. | Essential migration aid, but no preserved input snapshot/replay receipt. | Essential for this migration |
| `scripts/validate_site.py` | Target release assertions. | Fresh pass: 195 primary routes, 73 historical warnings. | Highly actionable; depends on undeclared `bs4`, and warning policy is weak. | Strongly beneficial |
| SSG contract/validator scripts | CLI/generated output quality. | Fresh CLI and generated contracts passed; starter output validation passed. | Strong for intended SSG fixtures; does not replace real-site visual/a11y/clean-room tests. | Strongly beneficial |
| `reports/visual/*.png` | Visual QA evidence. | Eight PNGs retained. | Useful manual evidence, but no reproducible runner, viewport list, or result receipt. | Useful |
| Python static server | Preview generated output. | README instructs `python3 -m http.server`. | Works as a simple server; no rebuild/live reload integration. | Situational |
| Lens | Browser/visual QA. | No configuration, invocation, receipt, or report in target. | Not evaluable. | Not actually used |
| RunLedger | Command/result receipts. | No `.runledger` or receipt found. | Missing traceability role. | Not actually used |
| ShipCheck | Release gate. | No invocation/artifact found. | Not evaluable. | Not actually used |
| ChangeBucket | Change-impact analysis. | No invocation/artifact found. | Not evaluable. | Not actually used |
| Muzzle / PackWrite / Scent | Agent context management. | No target config or receipt found. | No evidence of context pack/plan discipline. | Not actually used |
| CaseFile | Failure evidence bundle. | No target bundle found. | Could have captured FL-01/FL-08 but did not. | Not actually used |
| Howl / Concord / Watchdog / RAG | Showcase, drift, telemetry, retrieval workflows. | No target evidence found. | Outside proven workflow. | Not actually used |

## Recommended workflow membership

Keep Kujo SSG, SiteKit, target validation, and generated-output validation. Add a doctor/workspace manifest before adding more tools. Once a project has a reproducible build, add a visual/a11y runner (Lens is a candidate only if its receipt contract meets the golden path), RunLedger for command receipts, and ShipCheck or an equivalent single release gate. Do not mandate tools merely because they exist.
