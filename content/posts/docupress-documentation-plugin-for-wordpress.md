---
title: "DocuPress: documentation simplified."
description: "DocuPress is a documentation plugin for WordPress that lets you, you guessed it , add documentation directly from your website's WordPress dashboard. This is the 6th free plugin I've released in the WordPress plugin…"
custom_url: "docupress-documentation-plugin-for-wordpress"
author: "Robert DeVore"
date: "2017-05-12"
canonical: "https://robertdevore.com/docupress-documentation-plugin-for-wordpress/"
template: "signal-c"
nav_hide: true
excerpt: "DocuPress is a documentation plugin for WordPress that lets you, you guessed it , add documentation directly from your website's WordPress dashboard. This is the 6th free plugin I've released in the WordPress plugin…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

[**DocuPress**](https://www.wordpress.org/plugins/docupress) is a documentation plugin for WordPress that lets you, _you guessed it_ , add documentation directly from your website's WordPress dashboard. This is the 6th free plugin I've released in the WordPress [plugin repository](https://www.wordpress.org/plugins/) and one that I definitely know I'm going to be using myself … _a lot_.

## Why build a documentation plugin?

This has become a bit of a run-on story with me, but DocuPress was built for a self-serving reason; [WP Dispensary](/wp-dispensary/) needed better [documentation](https://www.wpdispensary.com/documentation) than it had, and nothing I found fit my needs, so I built it. In reality, there's a few documentation plugins out there already and I'm sure I could have found something that worked well enough, but where's the fun in that? ? I had the original idea for DocuPress in December of 2015! ? and didn't do anything else with it until about 4 months ago, when I created the initial core files for the plugin (which was just a boilerplate build from [wppb.me](http://www.wppb.me)). A couple of weeks ago, I knew I had to do something about the WPD documentation, so I dove in and started writing code. Again, I didn't do much, but it _did_ make it to my list of things to do, which was a step in the right direction. Then, a couple of nights ago I had a couple of spare hours along with the urge to get it done, so I sat down and wrote code. The rest, as they say, is history ✌

## What does DocuPress actually do?

![DocuPress in the WordPress admin menu](/assets/legacy-images/docupress_admin_menu.webp)DocuPress is built as a [custom post type](https://codex.wordpress.org/Post_Types) for WordPress, along with a custom taxonomy for the collections, which act like categories. After install and activation, you'll see the Documentation tab in your dashboard. This is where you can add new articles, which function similar to blog posts. You can also add the article to a specific collection, add a featured image and publish it. ![DocuPress Widget Options](/assets/legacy-images/docupress_widget_options.webp)There's also a custom widget added which you can use to display all recent articles from your documentation. It also comes with the ability to change which collection it will display articles from, so you can easily have multiple widgets for multiple collections of articles. You're also able to randomize the articles that are displayed, and also add a "view all" link to the bottom of the widget (only displays if you choose a specific Collection, not if "All" is selected).

### In the pipeline

I'm working on adding some shortcodes to make it easy to create your own documentation page, as well as the ability for DocuPress to create a documentation page upon activation. Approaching this right will take some time to think through and plan out properly, but it's definitely in the works. I've got a couple of other ideas as well, but want to keep those close to the chest right now while I take feedback from users ?

## DocuPress Demo

As I mentioned earlier, I built DocuPress to handle the documentation for WP Dispensary, and that's where you can currently view the plugin in action. The demo is using the [Beaver Builder](https://wordpress.org/plugins/beaver-builder-lite-version/) plugin to add the DocuPress widgets side-by-side in a grid format. [View DocuPress Demo](https://www.wpdispensary.com/documentation)

## Where can I download DocuPress?

You can download DocuPress directly from your dashboard, by going to `Plugins - Add New` and searching for **DocuPress**. ![DocuPress - documentation plugin for WordPress](/assets/legacy-images/DocuPress_add_plugin_in_WordPress.webp)

You can also check out DocuPress in the [WordPress repository](https://www.wordpress.org/plugins/docupress) and [Github](https://www.github.com/robertdevore/DocuPress).

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
