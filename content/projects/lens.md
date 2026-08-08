---
title: "Lens"
description: "Deterministic browser and visual QA workflows for local web projects."
author: "Robert DeVore"
date: "2026-07-10"
template: "project"
tags: ["Browser QA", "Accessibility", "Visual testing"]
excerpt: "Browser flows, screenshots, accessibility checks, link checks, visual baselines, and repair briefs."
---
Lens gives agents deterministic browser evidence for the interfaces they build. It opens a real page, captures what rendered, applies bounded checks, and returns an agent-ready report without relying on a vision model to guess.

## Why Lens exists

Source code and green unit tests cannot prove that a page loads, fits its viewport, exposes the expected controls, or remains accessible. Lens turns those runtime questions into repeatable checks and durable artifacts.

## What it provides

- Page-load, console, network, blank-page, and horizontal-overflow checks.
- Opt-in link, accessibility, performance, crawl, visual-baseline, and comparison checks.
- Safety-gated interaction flows with recording, screenshots, timelines, and walkthrough artifacts.
- Structured JSON, Markdown, and self-contained HTML reports.
- Agent Repair Briefs with stable evidence and secret-safe redaction.
- Localhost-first policy; external targets require explicit authorization.

## Check a local page

```text
lens check http://localhost:3000 --accessibility --html
```

## Current boundary

Lens is beta/stabilizing. Its core report and safety contracts are tested, while the public API remains free to tighten before 1.0.

[Explore Lens on GitHub ↗](https://github.com/kujolang/lens)
