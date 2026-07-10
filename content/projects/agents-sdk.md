---
title: "Kujo Agents SDK"
description: "Runtime primitives and examples for building bounded, testable agents with Kujo."
author: "Robert DeVore"
date: "2026-07-10"
template: "project"
tags: ["Agents", "SDK", "Approvals"]
excerpt: "Agent runners, tools, approvals, handoffs, tracing, memory, retrieval, and offline fixtures."
---
Kujo Agents SDK provides library-first runtime primitives for bounded, testable agent workflows. It builds on the Kujo AI SDK while keeping orchestration, security, state, and integration boundaries explicit.

## Why Agents SDK exists

An agent needs more than a model call. Reliable execution requires predictable run contracts, controlled tools, approvals, cancellation, traceable events, durable artifacts, retrieval, memory, and budgets that can be tested without live credentials.

## What it provides

- Agent, message, step, run, error, and lifecycle-event contracts.
- Runners, controlled tool registries, security policy, cancellation, and runtime clock/ID services.
- Approval gates, handoffs, tracing, artifacts, session and memory stores, and retrieval providers.
- Token, step, time, and cost budget primitives for bounded execution.
- Deterministic offline fixtures and contract tests that do not require network access or provider keys.
- Adapter boundaries that keep provider execution in the Kujo AI SDK and product-specific integrations outside core.

## Run the offline proof

```text
kujo run examples/examples_smoke_runner.kujo --interpreter
kujo test
```

## Current boundary

The core is production-oriented and contract-tested, while higher-level integration payload conventions remain experimental and target-environment persistence or compliance adapters stay intentionally external.

[Explore Kujo Agents SDK on GitHub ↗](https://github.com/kujolang/agents-sdk)
