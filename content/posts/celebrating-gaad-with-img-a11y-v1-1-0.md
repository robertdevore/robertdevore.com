---
title: "Celebrating GAAD with IMG A11Y v1.1.0"
description: "Today is Global Accessibility Awareness Day (GAAD) , and I’m celebrating the only way I know how: shipping code that actually helps. I pledged time with Equalize Digital to focus my time on the IMG A11Y plugin, and…"
custom_url: "celebrating-gaad-with-img-a11y-v1-1-0"
author: "Robert DeVore"
date: "2025-05-15"
canonical: "https://robertdevore.com/celebrating-gaad-with-img-a11y-v1-1-0/"
template: "signal-b"
nav_hide: true
excerpt: "Today is Global Accessibility Awareness Day (GAAD) , and I’m celebrating the only way I know how: shipping code that actually helps. I pledged time with Equalize Digital to focus my time on the IMG A11Y plugin, and…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

Today is [Global Accessibility Awareness Day (GAAD)](https://accessibility.day/), and I’m celebrating the only way I know how: shipping code that actually helps.

I pledged time with [Equalize Digital](https://equalizedigital.com/gaad2025/) to focus my time on the [IMG A11Y](/projects/img-a11y/) plugin, and that’s exactly what I did.

But first, before we talk about the code, let’s talk about GAAD.

### What is GAAD?

GAAD is a worldwide effort to get people talking, thinking, and doing more about digital accessibility – for the over one **billion people** living with disabilities.

It’s not a marketing campaign. It’s not a charity stunt. It’s a call to action. One that should resonate especially loud in the WordPress community.

As of this writing, WordPress powers around **43% of the internet**.

That means every accessibility bug, every missing `alt` tag, every un-navigable menu has ripple effects across millions of users.

If you care about the open web, you should care about accessibility.

Full stop.

### IMG A11Y v1.1.0 – Small Changes, Big Impact

To honor GAAD, I’m releasing version **1.1.0** of [IMG A11Y](/projects/img-a11y), my plugin dedicated to improving image accessibility in WordPress.

#### 🚫 Removed A11Y Options for Non-Image Media

In earlier versions, IMG A11Y would show accessibility options for media types like PDFs and other non-image files.

That caused confusion – because those settings don’t apply.

In 1.1.0, they’re gone. Thank you [@dknauss](https://github.com/robertdevore/img-a11y/issues/3) for raising the issue 🤘

#### 🔍 Elementor Support Added

Gutenberg? Checked.

Classic editor? Checked.

But Elementor? That was missing.

As of 1.1.0, IMG A11Y now **scans Elementor builder content** for images missing `alt` attributes – and blocks the post from being published until you fix them.

Same enforcement, new editor. No excuses.

### Why This Matters

Missing `alt` tags might not break a layout, but they **break the experience** for screen reader users.

They leave blind and visually impaired visitors guessing what a photo is. Or worse, they leave them out entirely.

That’s not okay. Not in 2025. Not when we have the tools to do better.

Accessibility isn’t just a checkbox. It’s a mindset.

It’s about designing for the edges so that **everyone** can use what we build.

And it starts with the basics – like making sure your images are described properly.

### Why I’m Doing This

I’m not trying to win awards. I’m trying to write software that doesn’t leave people behind.

IMG A11Y was built because WordPress still makes it too easy to ship inaccessible content.

Alt text is optional. Decorative images aren’t marked. Media modals don’t nudge users toward best practices.

This plugin helps fill that gap.

And today, GAAD is a reminder to take that responsibility seriously.

### How You Can Help

  * Install and use IMG A11Y. It’s free.
  * Add alt tags to your media library.
  * Mark decorative images correctly.
  * Teach your team why it matters.
  * Spend an hour improving your site’s accessibility.
  * Take the GAAD Pledge and be part of the movement.



Let’s build a better web – not just for some, but for everyone.

**Download IMG A11Y v1.1.0** :

View the [IMG A11Y project page](/projects/img-a11y/) and download it from there. If you’ve already installed the plugin, you’ll receive the update notification in your dashboard.

_Released with purpose. Built for inclusion._

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
