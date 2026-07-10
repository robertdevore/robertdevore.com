---
title: "Introducing automattic.css – An open source CSS Utility Framework"
description: "Today I’m releasing v0.1.0 of automattic.css – a new utility-first CSS framework inspired by the structure and philosophy of Automatic.css, but with a twist: it’s lean, builder-agnostic, and open to the community from…"
custom_url: "introducing-automattic-css-an-open-source-css-utility-framework"
author: "Robert DeVore"
date: "2025-05-22"
canonical: "https://robertdevore.com/introducing-automattic-css-an-open-source-css-utility-framework/"
template: "signal-c"
nav_hide: true
excerpt: "Today I’m releasing v0.1.0 of automattic.css – a new utility-first CSS framework inspired by the structure and philosophy of Automatic.css, but with a twist: it’s lean, builder-agnostic, and open to the community from…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

Today I’m releasing **v0.1.0 of[automattic.css](https://github.com/robertdevore/automattic-css/)** – a new utility-first CSS framework inspired by the structure and philosophy of Automatic.css, but with a twist: it’s lean, builder-agnostic, and open to the community from day one.

### Why I Built It

I’ve worked with CSS frameworks long enough to know what bloats fast. 

And [automattic.css](https://github.com/robertdevore/automattic-css/) starts intentionally light – focusing on scalable, semantic utility classes built on CSS variables and fluid spacing systems.

It’s not trying to be Tailwind. It’s not locked into WordPress builders. It’s meant to be **yours to extend**.

### Plus, a bit of backstory

Let’s just say this project didn’t start in a vacuum.

After a [lively debate](https://www.youtube.com/watch?v=e6eHP6KWyrE) on what makes a $5,000 website, I ended up blocked by [Kevin Geary](/kevin-michael-geary-a-hidden-history-of-hate-racism-and-bigotry/), the creator of another CSS framework.

Then he pulled our entire episode and pretended it never happened by changing Episode 14 to 13 🤦‍♂️

Cool 🫠

So I read his docs. Then I built my own framework.

That’s how `automattic.css` was born – not (totally) out of spite, but out of principle.

I wanted something open, flexible, and community-first.

No gatekeeping, builder lock-in or paywalls.

Sometimes the best ideas start with: _“Alright, bet.”_

## What’s in v0.1.0

Right now, automattic.css includes:

  * A full spacing scale (`.p-xxs` to `.p-xxl`, `margin`, `gap`, `section--*`)
  * Core typography utilities (`.text--xl`, `.text--700`, `.text--center`)
  * Basic color classes for backgrounds and text (`.bg--primary`, `.text--neutral`)
  * Grid utilities (`.grid--3`, `.gap-md`)
  * Z-index utilities, focus states, and display helpers
  * A small set of responsive overrides



It’s built entirely with CSS variables so you can theme and scale everything with confidence.

### What’s Missing (and Coming)

This is a **v0.1.0 on purpose**. The framework doesn’t yet include:

  * Contextual spacing utilities (`.container-gap`, `.content-gap`)
  * Smart spacing (default margin resets + consistent vertical rhythm)
  * Section spacing scale (`section--sm`, `section--xl`, etc.)
  * Full color shade system (light, dark, hover)
  * Transparency utilities (`--primary-trans-40`, etc.)
  * Button variants (`.btn--primary-dark-outline`, etc.)
  * Context-aware overrides
  * Smart line height or fluid typography by default



These are already outlined and in-progress for the next release cycles. 

Please note, I’m only one man with a limited amount of time spent on this so far, so if you don’t feel like it has enough for a v0.1.0 release, sue me 😎

[![](/assets/legacy-images/automattic_css_demo_template.webp)](https://moneyman.robertdevore.com/)

### Proving It Works: The Demo Template

To show automattic.css wasn’t thrown together without and testing, I built a [live demo](https://moneyman.robertdevore.com/) template using nothing but the framework itself – no builder, no bloated theme, no extra dependencies.

The goal? Prove that you can spin up a clean, responsive, fast-loading site with purely semantic utility classes and CSS variables.

The demo covers common layout patterns: hero sections, grids, and consistent spacing.

Everything is styled using the core classes from v0.1.0.

It’s the kind of template you can fork, gut, and make your own in five minutes.

Because frameworks shouldn’t just _talk_ about being lean and flexible.

They should _show_ it.

### Why Launch Now?

Because the goal isn’t to ship perfection – it’s to **build something useful and open**.

I want feedback from real users before locking down every class, naming convention, or design constraint. 

If you’re a dev or designer who values clean markup, semantic class names, and CSS variables over rigid systems, I’d love your thoughts.

You can use [automattic.css](https://github.com/robertdevore/automattic-css/) today. You can fork it. You can help shape what v0.2.0 becomes.

### Roadmap

Here’s what’s coming next:

  * ✅ Full contextual spacing support
  * ✅ Smart spacing system to remove default margins and enforce layout consistency
  * ✅ Fluid, responsive typography with smart line height
  * ✅ Scalable button system with token-based overrides
  * ✅ Color shades, transparencies, and theme logic



Follow the repo, submit ideas, or just drop in and let me know how you’re using it.

### Get Started

You can check out the GitHub repo [here](https://github.com/robertdevore/automattic-css)

Documentation is minimal right now, but I’m working on it as I hammer out the next updates.

CSS is organized, un-minified, and easy to customize.

Thanks for reading – and thanks in advance to anyone who uses, breaks, or improves this little framework. 

Let’s build something better, together 💪💯

_The[automattic.css](https://github.com/robertdevore/automattic-css/) CSS utility framework is in no way affiliated with Automattic Inc, Matt Mullenweg, WordPress.com, or the WordPress open source project._

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
