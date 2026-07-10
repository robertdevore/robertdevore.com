---
title: "Dispatch"
description: "Reliable AI workflow orchestration with resumable runs, approvals, policies, and trace artifacts."
author: "Robert DeVore"
date: "2026-07-10"
template: "project"
tags: ["Agents", "Orchestration", "Workflows"]
excerpt: "Reliable workflow orchestration with resume support, approvals, policies, and exportable evidence."
---
Dispatch is a Kujo workflow-orchestration engine for reliable AI systems. It routes structured work through repeatable templates and leaves behind reviewable run state, traces, reports, and handoff bundles.

## Why Dispatch exists

Single-step chat calls are not enough when work must be repeated, paused, reviewed, approved, retried, and resumed. Dispatch treats orchestration state and evidence as part of the product instead of incidental logs.

## What it provides

- Declarative workflow steps, typed metadata, agent roles, dependencies, and schema validation.
- Persisted run state with pause, resume, retry, timeout, cancellation, and optional-step semantics.
- Human approval decisions, tool-policy profiles, plugins, lifecycle hooks, and webhook sinks.
- Run catalogs, diagnostics, retention cleanup, export/import, and health repair.
- Structured Markdown/JSON reports, trace artifacts, handoff events, and signed bundle seams.
- Safe local fixture execution by default with optional Kujo AI SDK integration behind a bridge.

## Run a fixture workflow

```text
kujo run dispatch.kujo demo "Review this decision" --yes --non-interactive
```

## Current boundary

The verified path is local and fixture-backed. Live provider behavior is optional and requires the adjacent AI SDK plus explicit environment-specific validation.

[Explore Dispatch on GitHub ↗](https://github.com/kujolang/dispatch)
