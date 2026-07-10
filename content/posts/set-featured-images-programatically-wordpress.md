---
title: "Set Featured Images Programmatically in WordPress"
description: "Recently, I found myself needing to auto-set 300+ featured images for a customers WooCommerce store. After the initial panic phased itself out, I took a couple of deep breathes and realized I've done a few kinda-sorta…"
custom_url: "set-featured-images-programatically-wordpress"
author: "Robert DeVore"
date: "2018-04-03"
canonical: "https://robertdevore.com/set-featured-images-programatically-wordpress/"
template: "signal-a"
nav_hide: true
excerpt: "Recently, I found myself needing to auto-set 300+ featured images for a customers WooCommerce store. After the initial panic phased itself out, I took a couple of deep breathes and realized I've done a few kinda-sorta…"
categories: ["WordPress Archive"]
tags: ["WordPress", "WooCommerce"]
---

[WordPress Archive](/category/wordpress-archive/) · [WordPress](/tag/wordpress/) · [WooCommerce](/tag/woocommerce/)

Recently, I found myself needing to auto-set 300+ featured images for a customers [WooCommerce](https://www.woocommerce.com) store. After the initial panic phased itself out, I took a couple of deep breathes and realized I've done a few kinda-sorta similar things with custom functions in the past. After a few hours of hacking the code up and reformatting it to fit my specific needs, I ended up with the plugin that automatically cycles through each WooCommerce product and does it's magic on plugin activation. ![](/assets/legacy-images/magic.webp)

## Why set featured images programmatically?

If you're working on a client website and there's only a couple of featured images you need to set, then it may be best to just manually set each featured image. But let's say your client has over 200 WooCommerce products that are all set up, except for the featured images. Let's say the client added images to each product, but placed them inside the content instead of setting a featured image. What direction would you take to handle this situation? The first option would be to add a featured imaged to each product manually. ![](/assets/legacy-images/fuck_that.webp)Fuck that. Instead, the code below will cycle through all of your published WooCommerce products and get the first image that's attached to the product and make that image ID the featured image.

## The Code

The function loops through all published WooCommerce products and checks if there's any media attached to the product. If it finds attached media, it will use that specific image's media ID for the product's featured image. If there's no media, it then checks to see if an image has been placed within `the_content` of the product. If it finds an image within `the_content`, it uses that image's media ID for the featured image. If no image is found in either, nothing is done. https://gist.github.com/robertdevore/9803c06086d27be2abbd540ad925cf62

## Download the plugin from Github

I created a simple plugin that fires off this function on plugin activation. Download the beta version: `git clone https://github.com/robertdevore/woocommerce-set-featured-images` Don't want to get it from the command line? Download it from it's [Github repository](https://github.com/robertdevore/woocommerce-set-featured-images). **Although this code works for me, I cannot guarantee that it will work for you.****Please remember to back up your website before use, just in case ?**

## Related writing

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)

## Continue reading

**Newer:** [WP Dispensary v2.0 is being released on 4/20](/wp-dispensary-v2/)

**Older:** [? hue.js](/hue-js/)
