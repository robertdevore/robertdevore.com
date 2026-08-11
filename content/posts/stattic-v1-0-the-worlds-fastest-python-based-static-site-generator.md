---
title: "Stattic v1.0: The World’s Fastest Python-based Static Site Generator"
description: "Over the last few months, I’ve gone all-in on Python. Not just because it's powerful - but because it’s accessible. I've been building tools , writing tutorials , dropping full cipher projects , and even releasing a…"
custom_url: "stattic-v1-0-the-worlds-fastest-python-based-static-site-generator"
author: "Robert DeVore"
date: "2025-06-20"
canonical: "https://robertdevore.com/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/"
template: "signal-b"
nav_hide: true
excerpt: "Over the last few months, I’ve gone all-in on Python. Not just because it's powerful - but because it’s accessible. I've been building tools , writing tutorials , dropping full cipher projects , and even releasing a…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
featured_image: "/assets/social/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator-social.png"
---

Over the last few months, I’ve gone all-in on Python. Not just because it's powerful - but because it’s accessible. I've been [building tools](/5-python-scripts-for-osint-and-pentesting/), [writing tutorials](/complete-beginners-guide-building-a-python-url-checker-for-google-sheets/), dropping full [cipher projects](/i-built-a-python-stego-cipher-tool-and-you-can-have-it/), and even releasing a full [Python course](https://python.robertdevore.com) specifically designed to help PHP and WordPress® developers make the leap. Because I’m not just trying to hand people a tool. I want to teach you how to wield it, too. That’s what [Stattic](https://stattic.site) is about: giving devs control again - with no lock-in, no unnecessary functionality, and no noise. Just fast, secure, clean builds every time. And now? Stattic v1.0 is here! It's the **fastest Python static site generator in the world** - and the **second fastest SSG overall** , right behind Hugo. Brag? Hell yeah. I’m proud of it. 😎

_This claim is based on[dat](https://ssg-build-performance-tests.netlify.app/)[a](https://ssg-build-performance-tests.netlify.app/) from [CSS Tricks](https://css-tricks.com/comparing-static-site-generator-build-times/) in 2020. I will be looking to conduct additional tests to solidify the current numbers._

_You can see Stattic’s build time from March 2025[here](https://x.com/deviorobert/status/1900010961857024183)._

Stattic started as a single Python script. Just Markdown in and HTML out. 

I needed something fast, SEO-friendly, and simple enough to understand in one sitting. That was `v0.1`. Hacky and scrappy – but it worked.

Today, it’s `v1.0`.

And [Stattic](https://stattic.site) isn’t just a script anymore – it’s a real package. Installable, well documented, secure and professional.

## What’s New in Stattic v1.0.0

This is the biggest update yet – here’s the short version:

### 🔧 Core Overhaul

  * **Fully modular Python package** – instead of one massive script
  * **PyPI ready** – install with `pip install stattic`
  * **New CLI** – run `stattic --init yml` , and you’re good to go
  * **Project scaffolding** – comes with base templates, assets, and starter content



### 🔐 Security Upgrades

  * **SSRF protection** and **URL validation** – no more accidental open proxies
  * **Input and path sanitization** – safer file handling by default
  * **Directory traversal protections** – blocks `../` exploits and keeps builds safely locked to your project folder



### ⚡ Speed & Performance

  * **Large build regression squashed** – it’s fast … hella fast
  * **File processing streamlined** – reduced memory use and better flow



### 🎨 UX & Templates

  * **New mobile menu** – Alpine.js-powered hamburger menu
  * **Cleaner base theme structure** – easier to customize
  * **Better responsive defaults** – looks solid on mobile out of the box



### ⚙️ Config & CLI

  * **New config support** – `stattic.yml` or `stattic.json`
  * **Centralized settings** – one source of truth
  * **Improved CLI parsing** – less guesswork, more control



### 🧹 Code Cleanup

  * **Total refactor** – better separation of concerns, cleaner modules
  * **Stronger error handling and logging**
  * **Prepped for future extensibility**



## Breaking Changes (Read This)

If you’re upgrading from `v0.3.0` or earlier, heads up:

  * The **project structure is different**
  * Instead of `python stattic.py`, use `stattic` as your CLI
  * **Config files** now use YAML or JSON (`stattic.yml` / `stattic.json`)
  * Templates are now inside the package under `stattic_pkg/templates/`



Migration is easy, but it’s not automatic. You’ll want to:

``` pip install stattic stattic --init yml ``` 

Then move over your content and templates.

## So what’s next? 🤔

This release isn’t about features – it’s about product maturity.

[Stattic](https://stattic.site) is no longer just a script I hacked together out of frustration. 

It’s a real alternative for devs who want full control over their site with none of the baggage of legacy platforms.

If you’re building blogs, portfolios, documentation, or product pages – and you’re tired of fighting your tools – give Stattic a spin.

This is `v1.0`, and it’s just getting started.

→ [Install Stattic](https://pypi.org/project/stattic)

→ [View the source](https://github.com/getstattic/stattic)

→ [View the demo](https://demo.stattic.site)

→ [View the docs](https://docs.stattic.site/)

I am looking for feedback and contributors, so if you want to help Stattic grow, please reach out 🤘

## Related Reading

- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
- [I Just Launched a Python Course for PHP Developers](/i-just-launched-a-python-course-for-php-developers/)
