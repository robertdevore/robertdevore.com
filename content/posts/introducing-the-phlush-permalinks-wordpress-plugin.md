---
title: "Introducing the Phlush Permalinks WordPress Plugin"
description: "Another day, another free WordPress plugin release 🚀💪 Are you tired of manually flushing your permalinks every time you make structural changes to your WordPress site? Phlush Permalinks , a new WordPress plugin I…"
custom_url: "introducing-the-phlush-permalinks-wordpress-plugin"
author: "Robert DeVore"
date: "2024-09-05"
canonical: "https://robertdevore.com/introducing-the-phlush-permalinks-wordpress-plugin/"
template: "signal-c"
nav_hide: true
excerpt: "Another day, another free WordPress plugin release 🚀💪 Are you tired of manually flushing your permalinks every time you make structural changes to your WordPress site? Phlush Permalinks , a new WordPress plugin I…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

Another day, another free WordPress plugin release 🚀💪

![Phlush Permalinks toilet with a chain coming out of it in a nice looking bathroom](/assets/legacy-images/phlush_permalinks_featured_image.webp)

Are you tired of manually flushing your permalinks every time you make structural changes to your WordPress site? 

**Phlush Permalinks** , a new WordPress plugin I developed helps to automate this essential task, ensuring that your permalinks remain optimized without any manual intervention.

Whether you’re updating post types, changing taxonomies, or performing other site management tasks, Phlush Permalinks makes sure that your permalink structure is always up to date.

## **Why Permalinks Matter:**

WordPress permalinks are the URLs that lead to your content. 

Keeping them clean, SEO-friendly, and functional is essential for a good user experience and search engine optimization. 

Unfortunately, WordPress doesn’t automatically refresh permalinks after certain actions like changing post types or slugs. 

Without this, users may find broken links, and search engines might not be able to crawl your content properly.

![](/assets/legacy-images/friday_pops_spraying_air_freshener.webp)

## **Key Features of Phlush Permalinks:**

  1. **Automated Flushing at Custom Intervals** : The plugin integrates seamlessly with WordPress’s cron system, allowing you to set automatic flushes at intervals that suit your site’s needs.
  2. **Trigger Flushing on Key Actions** : In addition to scheduled flushing, Phlush Permalinks allows you to define specific actions that trigger a permalink flush. Whether you’re updating post types, publishing new content, or making other structural changes, the plugin makes sure that your permalinks are always up to date.
  3. **Lightweight and Easy to Use** : Phlush Permalinks is lightweight, ensuring that it doesn’t slow down your site. Its simple integration with WordPress hooks means that it works quietly in the background, without needing any complex configurations.

![](/assets/legacy-images/phlush_permalinks_settings_screenshot_1024x553.webp)

## **How It Works**

Upon activation, Phlush Permalinks schedules a cron job that flushes permalinks at a user-defined interval. 

You can also specify certain actions that will trigger an immediate flush, such as publishing new posts, changing post types, or saving certain settings.

**Why Use Phlush Permalinks?**

Manually flushing permalinks is an often-overlooked task that can lead to significant issues if neglected. 

By automating this process, Phlush Permalinks saves you time and ensures that your URLs are always optimized. 

This can improve your SEO, prevent 404 errors, and enhance the overall user experience on your site.

## **Getting Started**

To install and use the Phlush Permalinks plugin, follow these steps:

  1. Download and install the plugin from the [WordPress directory](https://wordpress.org/plugins/phlush-permalinks/).
  2. Activate the plugin from the WordPress dashboard.
  3. By default, the plugin will automatically flush your permalinks at the default interval. To customize the interval or add actions that trigger flushing, you can modify the plugin settings by going to `Settings -> Phlush Permalinks`.



[Download from WordPress](https://wordpress.org/plugins/phlush-permalinks/)

## Looking to extend the plugin and add your own actions?

Included functionality provides developers like yourself with the ability to extend or modify this set of actions through the **`phlush_permalinks_available_actions`** filter.

### Example 1: Adding Custom Actions

Let’s say you want to add a custom action that triggers a permalink flush when a custom post type `event` is saved. You can hook into the filter like this:

``` function custom_phlush_add_event_action( $actions ) { // Adding a custom action for the 'event' post type $actions['save_post_event'] = esc_attr__( 'Event Save/Edit', 'your-textdomain' ); return $actions; } add_filter( 'phlush_permalinks_available_actions', 'custom_phlush_add_event_action' ); ``` 

In this example:

  * We’re adding a new action, `save_post_event`, which corresponds to saving or editing a custom post type called “Event”. This will now trigger a permalink flush every time an event is saved or updated.



### Example 2: Removing Actions

If you want to remove an action (e.g., you don’t want permalink flushing to occur when a category is edited), you can do it like this:

``` function custom_phlush_remove_category_action( $actions ) { // Removing the 'edit_category' action to prevent permalink flush on category edit unset( $actions['edit_category'] ); return $actions; } add_filter( 'phlush_permalinks_available_actions', 'custom_phlush_remove_category_action' ); ```

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
