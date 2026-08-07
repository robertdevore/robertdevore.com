# RunLedger Report

Generated: 2026-08-07T16:19:21Z

## Summary

| Runs | Pass | Partial | Fail | Abandoned |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 1 | 0 | 0 |

## Cost

No cost data recorded.

## Runs

| ID | Task | Provider | Model | Status | Verdict | Changed files | Follow-ups | Cost |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: |
| 2026-08-07-codex-fix-homepage-focus-principles-writing-and-closing-statement-001 | Fix homepage focus, principles, writing, and closing statement | openai | codex | partial | Homepage fixes are implemented and targeted generated-output, structural, Lens, Spec, and proof checks passed. Full repository build verification is partial because workspace-dependencies.json does not match the live Kujo/SSG/SiteKit checkouts and the full current build did not complete within the available verification window. | 9 | 0 | - |

## Runs by task

### Fix homepage focus, principles, writing, and closing statement

- 2026-08-07-codex-fix-homepage-focus-principles-writing-and-closing-statement-001 — partial (codex)

## Follow-ups

None.

## Notes

### 2026-08-07-codex-fix-homepage-focus-principles-writing-and-closing-statement-001

- Spec strict validation passed; homepage structural verifier and repository site validator passed; Lens before and after flows and homepage check passed. Full portable build remains blocked by declared workspace revision/hash drift, so verification used a reduced temporary content/assets build for the generated review output.
- Implementation commits: d2d43c6 and dff5af2; proof bundle commit: 299a3b8.
