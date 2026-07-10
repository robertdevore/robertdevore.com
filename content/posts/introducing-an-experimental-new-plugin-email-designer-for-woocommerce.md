---
title: "Introducing an experimental new plugin: Email Designer for WooCommerce®"
description: "WooCommerce emails have always been a pain point for store owners looking to create beautifully branded transactional emails without diving deep into custom PHP templates. While WooCommerce recently improved its email…"
custom_url: "introducing-an-experimental-new-plugin-email-designer-for-woocommerce"
author: "Robert DeVore"
date: "2025-02-12"
canonical: "https://robertdevore.com/introducing-an-experimental-new-plugin-email-designer-for-woocommerce/"
template: "signal-b"
nav_hide: true
excerpt: "WooCommerce emails have always been a pain point for store owners looking to create beautifully branded transactional emails without diving deep into custom PHP templates. While WooCommerce recently improved its email…"
categories: ["WordPress Archive"]
tags: ["WordPress", "WooCommerce"]
---

WooCommerce emails have always been a pain point for store owners looking to create beautifully branded transactional emails without diving deep into custom PHP templates. 

While WooCommerce [recently improved](https://developer.woocommerce.com/2025/01/22/woocommerce-9-7-pre-release-updates/) its email customizer settings, they completely dropped the ball (in my opinion) by not modernizing with Gutenberg blocks as others in the community [had hoped](https://github.com/woocommerce/woocommerce/discussions/52897).

That’s why I’m excited to introduce **[Email Designer for WooCommerce®](https://github.com/robertdevore/email-designer-for-woocommerce)** , an experimental plugin that brings **block-based email customization** to WooCommerce® for the first time. 

This is the **0.1 release** , and while it’s still a work in progress, it lays the foundation for something I believe the WooCommerce® community truly needs.

![](/assets/legacy-images/email_designer_for_woocommerce_order_processing_template.webp)Order Processing Template example

## What is Email Designer for WooCommerce?

This plugin allows you to fully customize all of WooCommerce’s default emails by **creating custom templates using the WordPress® block editor**. 

Instead of manually editing WooCommerce’s email template files, you can now design your emails with a familiar interface that’s built directly into WordPress®.

![Email Designer for WooCommerce® - Processing Order Template](/assets/legacy-images/email_designer_for_woocommerce_template_editor_scaled.webp)

### Key Features in Version 0.1:

  * Uses the **WordPress® block editor** to build email templates.
  * Supports **all WooCommerce default email types** (e.g., New Order, Customer Invoice, Completed Order, etc.).
  * Custom **shortcodes for order details** (since WooCommerce doesn’t provide native blocks for this yet).
  * A foundation for **full Gutenberg support in the future**.

![Email Designer Settings - Email Designer for WooCommerce®](/assets/legacy-images/email_designer_for_woocommerce_settings.webp)

## Current Shortcomings (A Work in Progress)

As excited as I am about this initial release, there are still **some major limitations** that I’m actively working on solving:

### 1\. **Lack of Blocks for Order Details**

From what I can find, WooCommerce® doesn’t currently provide a way to insert order details using Gutenberg blocks, even though it’s [mentioned on this page](https://developer.woocommerce.com/docs/blocks-reference/#order-summary-woocommerce-order-confirmation-summary). 

Maybe I’m just not seeing it available on my site 🤔

This means I had to create **shortcodes** for now. 

I know this isn’t the ideal solution, and I’d love to explore a more seamless block-based approach in the future.

### 2\. **Custom CSS Challenges**

The block editor provides a lot of styling flexibility, but **WooCommerce® emails don’t handle block-generated CSS well**. Specifically:

  * Using `has-primary` classes by selecting your theme’s color palette doesn’t always apply correctly in the email templates, whereas setting a custom hex color works fine.
  * Spacing properties like **margin and padding** are also tricky to get right and require custom pixel numbers to be set like the color hex’s.



### 3\. **WooCommerce’s Lack of Gutenberg Adoption**

Despite WooCommerce being a flagship project in the WordPress® ecosystem, their approach to email customization still **doesn’t leverage the core block editor**.

Many in the community have been advocating for WooCommerce to modernize its email system, as seen in this GitHub discussion:

🔗 [WooCommerce GitHub Discussion](https://github.com/woocommerce/woocommerce/discussions/52897)

For all the talk about Gutenberg being the future of WordPress®, many major plugins **still aren’t adopting it for key features like email design**. 

The WooCommerce® community deserves modern email customization tools, and I hope this project helps push things in the right direction.

![Nipsey Hussle - Never taught how to drink, I just lead to the lake GIF](/assets/legacy-images/nipsey_never_taught_how_to_drink.webp)

## Why I’m Building This

I run **[Devio Digital](https://deviodigital.com)** , where I sell WordPress® plugins, and I personally need a better way to **design WooCommerce emails** without clunky custom template overrides. 

Instead of waiting for WooCommerce® to step up, I decided to build my own solution and share it with the community.

I’m actively looking for **feedback and contributors** to help shape the future of WooCommerce® email design. 

If this is something you care about, I’d love to hear your thoughts!

## Let’s Talk

If you run a WooCommerce® store, develop plugins, or are just passionate about **better email customization** , I’d love to connect!

Let’s work together to create a modern solution that brings WooCommerce® emails into the Gutenberg era.

Drop a comment, open an issue on GitHub, or find me on [Twitter/X](https://x.com/deviorobert) to discuss the future of WooCommerce® email design. 🚀

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
