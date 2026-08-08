---
title: "WP Dispensary v2.0 is being released on 4/20"
description: "It is now less than 2 weeks until I release version 2.0** of WP Dispensary . And if you're not looking at a calendar, yes, the release date is 4/20 ? After working on this release, I took a step back and realized that…"
custom_url: "wp-dispensary-v2"
author: "Robert DeVore"
date: "2018-04-09"
canonical: "https://robertdevore.com/wp-dispensary-v2/"
template: "signal-c"
nav_hide: true
excerpt: "It is now less than 2 weeks until I release version 2.0** of WP Dispensary . And if you're not looking at a calendar, yes, the release date is 4/20 ? After working on this release, I took a step back and realized that…"
categories: ["WordPress Archive"]
tags: ["WordPress", "WooCommerce"]
---

It is now less than 2 weeks until I release **version 2.0** of[**WP Dispensary**](https://www.wordpress.org/plugins/wp-dispensary). And if you're not looking at a calendar, yes, the release date is 4/20 ? After working on this release, I took a step back and realized that it's been a hell of a journey to get here. From it's humble beginnings when it was [first released](https://www.wpdispensary.com/welcome-to-wp-dispensary/) in November 2015, to last September when [I left freelancing](/going-all-in-with-wp-dispensary/) and started working on it full time, I'm still just as proud at every milestone [WP Dispensary](https://www.wpdispensary.com) hits. The release of **version 2.0** will be no different. Before pushing this update out to the world, I wanted to take time to outline some of the changes and new features you can expect.

## Rebuilt Settings Page

This is arguably the biggest change coming in version 2.0 of [WP Dispensary](/two-years-building-wp-dispensary/). Back when I first released WPD, I honestly didn't put much thought into the **Settings** page. At the time, there wasn't many settings at all, and I wanted to get the MVP out into the world. This update brings in a brand new **Settings** page, built with the [WP OOP Settings API](https://github.com/AhmadAwais/WP-OOP-Settings-API) from [Ahmad Awaias](https://www.ahmadawais.com). [![](/assets/legacy-images/wpd_v2_settings_page_300x243.webp)](/wp-content/uploads/2018/04/wpd-v2-settings-page.png)click to expand

### Increased control over how to display data

Included in **version 2.0** are extra control over the way you display your menu item data on the front end of your website. For instance, in versions prior to**v2.0** the**Pricing** and**Details** tables that show up on single menu item pages had titles you couldn't alter. Now, there's a couple of options to choose from for each, as well as a way to type in your on custom titles. You are also able to _show/hide_ each table and as of [version 2.0](https://www.wpdispensary.com/demo/product/chemdawg/) you'll be able to choose _above/below_ placement options for both the **Pricing** and **Details** tables.

### Easier for add-on's to add their own settings

With the **Settings** being built with the**WPOSA** , it is giving me the ability to add additional tabs for the other add-on's from[WP Dispensary](https://www.wpdispensary.com). For instance, the [Connect for WooCommerce](https://www.wpdispensary.com/product/wooconnect-for-woocommerce/) add-on has it's settings page added as a sub-menu item of the WooCommerce tab in the WordPress dashboard. After the release of WPD **v2.0** , I'll be able to update the **Connect for WooCommerce** add-on to move it's setting options into a tab of the WP Dispensary **Settings**. This means it's easier to find these options for the user, and that's always my goal - an easy to use product for all users, developers and dispensary owners alike.

## Organized Edit Screens

Another big update as far as the UI is concerned is the cleaned up **Edit** screens for each menu type. Previously, all**taxonomies** and**metaboxes** for each menu type would display on the **Edit** screen, creating a bit of chaos and intimidation for users. **Version 2.0** cleans house! [![](/assets/legacy-images/wpd_v2_edit_screen_300x238.webp)](/wp-content/uploads/2018/04/wpd-v2-edit-screen.png)click to expand

### Default hidden data boxes

Each menu type has it's own set of **metaboxes** and**taxonomies** , but not all of them are needed by every user. Now, instead of having certain**taxonomies** like**Aroma** ,**Effects** , and **Symptoms** display on the page by default, they are now hidden under the **Screen Options** area. This makes the **Edit** screen for WP Dispensary's menu types a lot nicer to look at.

## Code Optimization & Speed Increases

This release will also feature a lot of code optimization and increases to the overall speed of the plugin. For instance, in the current version of the plugin, there's about 100 lines of code which displays the **currency code** that users select in the**Settings**. Every file that needs to display the **currency code** would also needs that ~100 lines of code added to it. This became a headache, both in terms of code maintenance as well as visually when looking at the code. It felt good to remove those lines of code from each file and replace them with a custom function. This also means that add-on's like [Connect for WooCommerce](https://www.wpdispensary.com/product/wooconnect-for-woocommerce) and [Heavyweights](https://www.wpdispensary.com/product/dispensary-heavyweights/), which display **currency codes** , will be able to remove those extra lines of code. Code may be poetry, but clean code is magical! ![](/assets/legacy-images/magic_2.webp)

## Calling for beta testers

I've been testing the code on various installs locally, but I'd love to have some outside eyes take a look at it and see if there's any bugs or ways to enhance the plugin further that I'm missing. Want to help beta test? Get in touch!

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
