---
title: "Just Released: Stattic v.0.3.0"
description: "Another release. Another step forward. Stattic v0.3.0 isn’t a flashy overhaul – it’s a focused upgrade that makes the core tighter, the output cleaner, and the tooling smarter. Here’s what’s new (and why it matters): 📦…"
custom_url: "stattic-v0-3-0-release-llms-txt-faster-gifs-leaner-core-and-smarter-routing"
author: "Robert DeVore"
date: "2025-05-19"
canonical: "https://robertdevore.com/stattic-v0-3-0-release-llms-txt-faster-gifs-leaner-core-and-smarter-routing/"
template: "signal-a"
nav_hide: true
excerpt: "Another release. Another step forward. Stattic v0.3.0 isn’t a flashy overhaul – it’s a focused upgrade that makes the core tighter, the output cleaner, and the tooling smarter. Here’s what’s new (and why it matters): 📦…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

[WordPress Archive](/category/wordpress-archive/) · [WordPress](/tag/wordpress/)

Another release. Another step forward.

**[Stattic](https://stattic.site) v0.3.0** isn’t a flashy overhaul – it’s a focused upgrade that makes the core tighter, the output cleaner, and the tooling smarter.

Here’s what’s new (and why it matters):

### 📦 `llms.txt` Generator

Large Language Models are scraping the web, and now Stattic gives you a way to tell them what you want indexed – or not. 

The new `llms.txt` generator works just like `robots.txt` but is designed specifically for AI crawlers like OpenAI’s GPTBot.

One flag, one file, full control.

### 🧹 9 Methods Deleted

Stattic isn’t bloating over time. It’s getting leaner.

We ripped out 9 internal methods from the core class that were dead weight. Less code, fewer bugs, faster reads.

### ⚡ GIF Optimization (Without the Lag)

Animated GIFs are now handled with `gif2webp` for drastically improved conversion speed. No `gif2webp` installed? We fall back to Pillow. No headaches either way.

It’s fast. It works. Move on.

### 📑 Sort by Front Matter `order`

You can now manually control the order of your posts using the `order` field in the front matter:

``` order: 1 ``` 

Want to build a course? A walkthrough? A mini-series? This gives you the power to dictate flow, not just rely on dates.

### 🏠 Smarter Index + Blog Routing

  * If you define a custom home page, Stattic won’t overwrite it.
  * If you _don’t_ include a blog template, `/blog/` now redirects to the home page.



This solves the weird edge cases and makes things Just Work™ with less config.

### 🔗 Misc Fixes & Cleanup

  * Broken contact link on the demo page? Fixed.
  * `render_template()` now always includes `site_url` and lets you override `relative_path` cleanly.
  * Codebase cleaned up across the board.
  * Docs updated with `gif2webp` in the requirements and a few minor fixes in the README.



## v0.3.0 TL;DR

  * ✅ AI-aware `llms.txt` support
  * ✅ Faster GIF to WebP conversion
  * ✅ Front matter-based post ordering
  * ✅ Fewer methods, smaller core
  * ✅ Smarter default routing
  * ✅ Clean code, clearer docs



**Stattic keeps doing what WordPress won’t: getting out of your way.**

No dashboards. No database. Just clean, fast, SEO-friendly sites with version-controlled content and full creative control.

And this is just v0.3.0. We’re only getting started 💪💯

👉 [See full changelog on GitHub](https://github.com/getstattic/stattic/releases)

## Related writing

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)

## Continue reading

**Newer:** [What Makes Content Beautifully Useful?](/what-makes-content-beautifully-useful/)

**Older:** [Plan. Prompt. Publish. A Practical Guide to Creating Beautifully Useful Content with AI](/plan-prompt-publish-a-practical-guide-to-creating-beautifully-useful-content-with-ai/)
