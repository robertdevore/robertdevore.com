---
title: "Kujo"
description: "The programming language and ecosystem at the center of Robert DeVore's current systems work."
author: "Robert DeVore"
date: "2026-07-10"
template: "project"
tags: ["Language", "Runtime", "Open source"]
excerpt: "A programming language and ecosystem built for clear, local, inspectable software workflows."
---
Kujo is a Rust-built, VM-first programming language for AI-native software, local-first automation, agentic workflows, and application scripting. It is designed for work where deterministic behavior, native capabilities, and practical ergonomics need to coexist.

## Why Kujo exists

Automation languages often force a choice between small scripts and dependable systems. Kujo keeps the scripting loop direct while making files, processes, network access, databases, async work, crypto, AI operations, and security capabilities explicit.

## What it provides

- A VM-first runtime with an interpreter available as a deliberate fallback and debugging path.
- Deterministic package manifests, lockfiles, nested module layouts, and frozen installs.
- Native AI request hashing, record/replay cassettes, streaming callbacks, multimodal messages, token budgeting, vector math, and JSON Schema validation.
- Trusted and untrusted execution modes with capability-specific filesystem, process, network, and AI egress controls.
- Machine-readable CLI contracts, diagnostics, documentation generation, tests, and release gates.
- A growing ecosystem of SDKs, workflow tools, publishing systems, QA tools, and local-first applications.

## Start from source

```text
cargo build
./target/debug/kujo run examples/hello.kujo
```

## Current boundary

Kujo is usable from source and staged as a pre-tag 1.0.0 release candidate. The repository deliberately separates implemented runtime capability from final tag, artifact publication, and environment-specific production proof.

[Explore the Kujo repository on GitHub ↗](https://github.com/kujolang/kujo)
