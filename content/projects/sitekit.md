---
title: "SiteKit"
description: "An AI-readable, human-verifiable design system and semantic component library."
author: "Robert DeVore"
date: "2026-07-10"
template: "project"
tags: ["Design systems", "Accessibility", "Components"]
excerpt: "Token-driven semantic interface primitives with machine-readable schemas and human-verifiable output."
---
SiteKit is an AI-readable, human-verifiable design system for accessible, semantic, token-driven websites and interfaces. Its source model keeps the rules a human or agent needs to inspect close to the components they shape.

## Why SiteKit exists

Generated interfaces are easier to trust when design intent is encoded as structured tokens, schemas, templates, and standards—not hidden inside a screenshot or a one-off page. SiteKit gives agents reusable constraints and gives people rendered examples they can verify.

## What it provides

- Design tokens and theme contracts for color, typography, spacing, borders, motion, and layout.
- Semantic component templates with component-specific CSS and machine-readable schemas.
- Layout recipes, content patterns, accessibility standards, and implementation guidance.
- Generated distribution CSS backed by reproducible build, lint, validation, and snapshot checks.
- A component lab for reviewing real variants, code samples, responsive behavior, and interaction states.
- Native HTML-first patterns designed around WCAG 2.2 AA expectations.

## Verify the source model

```text
npm run build
npm run lint
npm run validate
npm run snapshot
```

## Current boundary

SiteKit is an internal, source-only design-system package. Consumers vendor the reviewed surfaces they need; it does not claim an npm distribution or hosted component service.

[Explore SiteKit on GitHub ↗](https://github.com/kujolang/site-kit)
