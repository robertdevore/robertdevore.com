---
title: "Introducing HPOS Compatibility Scanner for WooCommerce® (free)"
description: "I’m excited to announce the release of HPOS Compatibility Scanner , a free WordPress® plugin designed to help developers identify and fix compatibility issues with WooCommerce’s High-Performance Order Storage (HPOS).…"
custom_url: "introducing-hpos-compatibility-scanner-for-woocommerce-free"
author: "Robert DeVore"
date: "2024-12-19"
canonical: "https://robertdevore.com/introducing-hpos-compatibility-scanner-for-woocommerce-free/"
template: "signal-b"
nav_hide: true
excerpt: "I’m excited to announce the release of HPOS Compatibility Scanner , a free WordPress® plugin designed to help developers identify and fix compatibility issues with WooCommerce’s High-Performance Order Storage (HPOS).…"
categories: ["WordPress Archive"]
tags: ["WordPress", "WooCommerce"]
---

I’m excited to announce the release of [**HPOS Compatibility Scanner**](https://github.com/robertdevore/hpos-compatibility-scanner), a free WordPress® plugin designed to help developers identify and fix compatibility issues with WooCommerce’s High-Performance Order Storage (HPOS).

This plugin aims to fill a gap that has been glaringly obvious since HPOS became the new standard.

![HPOS Compatibility Scanner for WooCommerce® - scan results ](/assets/legacy-images/hpos_compatibility_scanner_for_woocommerce_scan_results_1.webp)

## Why This Plugin?

When WooCommerce introduced HPOS over a year ago, it promised faster performance and a modernized architecture.

But for developers, it also brought a wave of changes that required reworking how we handle orders in our plugins.

Despite this, many developers (myself included) haven’t fully updated our plugins.

Why?

Because WooCommerce’s built-in notification system simply says that a plugin is “incompatible” and should be deactivated.

That’s it. No details, no actionable steps.

![That's not going to help, bro. GIF - First we Feast](/assets/legacy-images/thats_not_going_to_help_bro.webp)

For a feature as impactful as HPOS, this lack of clarity is frustrating – and it’s left many in the WooCommerce® community scrambling to diagnose compatibility issues.

## What Does HPOS Compatibility Scanner Do?

[HPOS Compatibility Scanner](https://github.com/robertdevore/hpos-compatibility-scanner) changes that.

This plugin doesn’t just tell you your plugin is incompatible – it shows you why. It scans the codebase of any selected plugin, flagging the use of outdated or incompatible APIs and direct database calls that could break under HPOS.

It’s an actionable, developer focused solution designed to:

  * Identify specific issues in your code.
  * Provide detailed scan results in an easy-to-read table.
  * Export results as a CSV for further analysis.

![HPOS Compatibility Scanner - scan results](/assets/legacy-images/hpos_compatibility_scanner_for_woocommerce_scan_results_2_948x1024.webp)Example scan results

## Why Should WooCommerce® Have Built This?

Let’s be honest; this is a tool WooCommerce® should have provided from the start.

Transitioning an entire ecosystem to a new architecture is no small feat, and developers deserve better tools to manage this shift.

[HPOS Compatibility Scanner](https://github.com/robertdevore/hpos-compatibility-scanner) exists because the WooCommerce® community needed it, and I’m proud to contribute a solution.

## How to Use HPOS Compatibility Scanner

The plugin integrates seamlessly with the WordPress® admin interface. Here’s how to get started:

  1. Navigate to `HPOS Scanner` in your admin dashboard.
  2. Select a plugin to scan from the dropdown menu.
  3. Click **Scan Plugin** to get detailed results on compatibility issues.



You can even export the results as a CSV for collaborative debugging with your team.

## What’s Next?

This is just the beginning.

Future updates will include real-time notifications, expanded API coverage, and advanced filtering options for the scan results.

I’m always looking for ways to improve the tool, so feedback from the community is highly appreciated 🙏

![Snoop Dogg - Smiling GIF](/assets/legacy-images/snoop_smiling.webp)

## Get Involved

I built this plugin to solve a pain point that I’ve felt personally, and I’m sure I’m not alone.

If you’re a developer struggling with the HPOS transition, give this tool a try. It’s free, open-source, and available now on [GitHub](https://github.com/robertdevore/hpos-compatibility-scanner).

Let me know how it works for you and what features you’d like to see in the future (if any) 🤘

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
