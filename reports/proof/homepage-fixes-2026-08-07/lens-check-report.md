# Lens Report

Status: PASS
URL: http://127.0.0.1:4183/
Started: 2026-08-07T16:17:00Z
Finished: 2026-08-07T16:17:11Z
Duration: 11245ms
Viewports: desktop, mobile
Output Directory: /Users/robertdevore/2026/robertdevore.com/.lens/runs/homepage-fixes-check

## Summary

Status: PASS
Total findings: 2
Critical: 0
Errors: 0
Warnings: 2
Info: 0
Fail threshold: error
Exit code: 0
Checks run: 15
Checks skipped: 0
Artifacts written: 10
Spec file: /Users/robertdevore/2026/robertdevore.com/qa/lens/specs/home.json
Spec checks run: 7
Spec checks skipped: 0
Spec checks failed: 0

Lens completed successfully. No findings met the configured fail threshold of `error`. Runtime artifacts were captured.

## Critical Issues

No critical issues found.

## Errors

No errors found.

## Warnings

- **LENS-LINKS-001** — Broken link (HTTP 404): LEAP: The Code of Extreme Leadership
  Same-origin link http://127.0.0.1:4183/leap-the-code-of-extreme-leadership/ returned HTTP 404.
  Evidence: links.json entry 18

- **LENS-LINKS-002** — Broken link (HTTP 404): LEAP: The Code of Extreme Leadership
  Same-origin link http://127.0.0.1:4183/leap-the-code-of-extreme-leadership/ returned HTTP 404.
  Evidence: links.json entry 57


## Evidence

Runtime evidence collected:

- Screenshots: `screenshots/desktop.png`, `screenshots/mobile.png`
- Console log: `console.json`
- Network log: `network.json`
- DOM summaries: `dom-summary.json`
- Link check results: `links.json`

- Accessibility results: `accessibility.json`

- Spec file: `/Users/robertdevore/2026/robertdevore.com/qa/lens/specs/home.json`
## Accessibility

Accessibility checks were enabled for this run.

- Engine: axe-core 4.11.4
- Scans completed: 2
- Violations found: 0
- Results: `accessibility.json`

No accessibility violations were detected by automated scanning.
Automated checks cannot detect all accessibility issues. Manual review
and screen reader testing are still essential.

Accessibility checks use axe-core automated rules. They do not guarantee
WCAG compliance and are not a substitute for manual accessibility review.

## Suggested Repair Tasks

1. Investigate the broken same-origin link recorded in links.json entry 18.

2. Investigate the broken same-origin link recorded in links.json entry 57.


## Agent Repair Brief

Lens failed because 0 finding(s) met the configured fail threshold of `error`.

The page loaded successfully. Secondary findings (console, network, overflow, links) can be trusted.

Viewports tested: desktop, mobile.

Link check enabled: 2 link finding(s) reported.

First artifacts to inspect:

Suggested first pass:
1. Investigate the broken same-origin link recorded in links.json entry 18.
2. Investigate the broken same-origin link recorded in links.json entry 57.

Do not assume the root cause is framework-specific unless the source code or console output proves it. Each finding includes evidence references — inspect those artifacts before drawing conclusions.

## Artifacts

- `lens-report.md`
- `lens-report.json`
- `metadata.json`
- `console.json`
- `network.json`
- `dom-summary.json`
- `screenshots/desktop.png`
- `screenshots/mobile.png`
- `links.json`
- `accessibility.json`
