---
title: "Introducing Broken Image Scanner"
description: "Let’s face it: broken image links are like ghosts haunting your website – annoying, scary for your users, and not great for your SEO. That’s why I’m excited to release the Broken Image Scanner , a free WordPress® plugin…"
custom_url: "introducing-broken-image-scanner"
author: "Robert DeVore"
date: "2025-01-14"
canonical: "https://robertdevore.com/introducing-broken-image-scanner/"
template: "signal-a"
nav_hide: true
excerpt: "Let’s face it: broken image links are like ghosts haunting your website – annoying, scary for your users, and not great for your SEO. That’s why I’m excited to release the Broken Image Scanner , a free WordPress® plugin…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

[WordPress Archive](/category/wordpress-archive/) · [WordPress](/tag/wordpress/)

Let’s face it: broken image links are like ghosts haunting your website – annoying, scary for your users, and not great for your SEO. 

That’s why I’m excited to release the **[Broken Image Scanner](https://github.com/robertdevore/broken-image-scanner)** , a free WordPress® plugin designed to help you hunt down and fix those pesky broken image URLs.

In this post, I’ll walk you through how to use the plugin, why it’s useful, and (hopefully) crack a smile or two along the way.

![](/assets/legacy-images/broken_image_scanner_scan_example.webp)

## What Does the Plugin Do?

The **[Broken Image Scanner](https://github.com/robertdevore/broken-image-scanner)** scans your site for image links that don’t work anymore.

It checks posts, pages, and all public custom post types for `<img>` tags, tests if those URLs are reachable, and compiles a neat list of the ones that are broken. 

Once the scan is done, you can download the results as a CSV file and even jump straight to editing the affected posts.

Think of it like having a metal detector at the beach, except instead of finding coins, you’re finding problems to fix. 

## Why Is This Useful?

Broken images are bad news for any site. Here’s why you want to avoid them:

  * **Bad User Experience:** Nobody likes seeing those “X” marks or broken icons where an image should be. It looks unprofessional and disrupts the flow of your content.
  * **SEO Impact:** Search engines don’t like broken links of any kind. Missing images can hurt your rankings.
  * **First Impressions Matter:** Whether it’s a product photo, a blog post image, or your logo, every image on your site plays a role in how people perceive your brand.



This plugin makes it easy to find and fix these issues without having to manually comb through every post.

![Ain't nobody got time for that - GIF](/assets/legacy-images/aint_nobody_got_time_for_that.webp)

## How to Use the Plugin

  1. **Install and Activate** : 
     * Download the plugin and activate it from the WordPress® admin panel. Easy-peasy.
  2. **Run a Scan** : 
     * Head to the **Image Scanner** page in your WordPress® admin menu.
     * Click the **Start Scan** button. The plugin will start scanning your content, and you’ll see a progress bar keeping you updated.
  3. **Review the Results** : 
     * As the scan progresses, a table will populate with all the broken image URLs the plugin finds.
     * Each row includes the post title (linked to the WordPress® editor) and the broken image URL. You can jump directly into fixing things without losing your place.
  4. **Download the Results** : 
     * Once the scan is complete, the **Start Scan** button transforms into a **Download CSV** button.
     * Click it to grab a CSV file with all the broken links. The file is named after your site and timestamped, so you’ll always know when the scan happened. (No more mystery files cluttering your desktop – you’re welcome.)

![Broken Image Scanner - scan results](/assets/legacy-images/broken_image_scanner_scan_results_example_scaled.webp)

## What’s Under the Hood?

The plugin scans your content in batches to avoid overloading your server. 

It sends a `HEAD` request to each image URL to check if it’s reachable. If it gets an error (or no response at all), that URL is flagged as broken.

The progress bar keeps you updated throughout, and the results are displayed in a simple, sortable table. 

Bonus: the first column of the table is fixed at 200px wide, so your data doesn’t look like it’s doing yoga.

## Who Should Use This Plugin?

This plugin is perfect for anyone managing a WordPress® site with lots of media:

  * Bloggers with a backlog of posts (because who remembers which images were linked five years ago?).
  * E-commerce site owners who rely on product photos.
  * Agencies managing client sites and needing to clean up before handing over the reins.

![Snoop Dogg - The Voice - Thumbs up GIF](/assets/legacy-images/snoop_thumbs_up_1.webp)

## Why I Built This Plugin

I noticed that broken images are one of those problems that creep into even the best-maintained sites. 

Maybe a file gets deleted. Maybe an external image link stops working. Whatever the reason, fixing broken images has always been tedious – until now.

So, I made a tool that simplifies the process. And hey, if it saves you an hour (or five) of your time, I’ll consider this project a success.

Broken images might be inevitable, but fixing them doesn’t have to be a headache. 

With the [Broken Image Scanner](https://github.com/robertdevore/broken-image-scanner), you can quickly identify the issues and clean up your site with just a few clicks.

Thanks for checking out the plugin! If you have any feedback or suggestions, [shoot me a message](/contact/), and happy scanning 🤘

## Related writing

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)

## Continue reading

**Newer:** [Hello, Plugin Pal: Your AI Powered Plugin Generator for WordPress®](/hello-plugin-pal-your-ai-powered-plugin-generator-for-wordpress/)

**Older:** [Introducing Block AI Crawlers for WordPress®](/introducing-block-ai-crawlers-for-wordpress/)
