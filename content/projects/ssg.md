---
title: "Kujo SSG"
description: "A deterministic static-site generator with visible content, templates, metadata, feeds, and release checks."
author: "Robert DeVore"
date: "2026-07-10"
template: "project"
tags: ["Publishing", "Static sites", "Kujo"]
excerpt: "Deterministic static publishing with visible templates, taxonomies, feeds, metadata, and validation."
---
Kujo SSG is a deterministic static-publishing pipeline built around one visible entrypoint. Content, routes, templates, collections, metadata, feeds, and validation stay in the repository instead of disappearing behind framework abstractions.

## Why Kujo SSG exists

Publishing infrastructure should make the resulting site easy to audit and easy to reproduce. Kujo SSG favors inspectable files, explicit configuration, deterministic routes, and generated artifacts that can be validated before deployment.

## What it provides

- Markdown pages, posts, and custom collections with custom templates and taxonomies.
- Configurable root or blog-prefixed post routes, pagination, sorting, drafts, and redirect aliases.
- Canonical, Open Graph, Twitter Card, JSON-LD, RSS, sitemap, robots, favicon, and `llms.txt` output.
- Local and remote image processing plus cached, self-hosted font support.
- Single-process and parallel-shard builds with deterministic output contracts.
- CLI, generated-site, release-gate, metadata, route, and asset validation.

## Build a site

```text
kujo run ./build.kujo -- --site-url https://example.com
bash scripts/validate-generated-output.sh output
```

## Current boundary

SSG is a local publishing system, not a hosted deployment service. Accessibility, editorial quality, performance, and production behavior still need representative review in each consuming site.

[Explore Kujo SSG on GitHub ↗](https://github.com/kujolang/ssg)
