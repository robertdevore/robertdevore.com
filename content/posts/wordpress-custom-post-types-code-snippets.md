---
title: "Enhance the power of your WordPress Custom Post Types"
description: "I've been working on extending the WP Dispensary plugin and wanted to share some of the ways I've found to help boost the power of the Custom Post Types you create. Custom Post Types are a great building block for…"
custom_url: "wordpress-custom-post-types-code-snippets"
author: "Robert DeVore"
date: "2017-06-26"
canonical: "https://robertdevore.com/wordpress-custom-post-types-code-snippets/"
template: "signal-a"
nav_hide: true
excerpt: "I've been working on extending the WP Dispensary plugin and wanted to share some of the ways I've found to help boost the power of the Custom Post Types you create. Custom Post Types are a great building block for…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

I've been working on extending the [WP Dispensary](https://www.wpdispensary.com/) plugin and wanted to share some of the ways I've found to help boost the power of the **Custom Post Types** you create. Custom Post Types are a great building block for turning WordPress into more than a piece of blogging software. Going beyond the original Posts and Pages, you can now segment your content as much as you need, with relative ease. I personally feel that WordPress wouldn't be where it is today without the inclusion of Post Type's in [version 3.0](https://codex.wordpress.org/Version_3.0). This is my attempt to show how a few simple code snippets can push the boundaries of what's possible with WordPress and Custom Post Types. Plus, it's a good way for me to keep the codes together in one place to reference in the future ?

> If you're new to CPT's and/or haven't built a Custom Post Type yet, you can check out this article from [Torque](https://torquemag.io/2015/12/wordpress-custom-post-types-tutorial/) that breaks CPT's down and gives you a variety of ways to create your own.

Read it? Got your own already built? _Great!_ Let's look at what we can do now that we have our CPT built. _Note: This article assumes you have a basic understanding of developing for WordPress. Please leave a comment or reach out on[Twitter](https://www.twitter.com/deviorobert) if you need further clarification on any of the tips below._

## 1. Custom API endpoints

Since this plugin seems like a likely candidate for future app integration, I want to add in some custom API endpoints to allow for content handling in something like [AngularJS](https://angularjs.org/) or [vue.js](https://vuejs.org/). **Giving your featured image an API endpoint** You can add a function like the one below, adding a filter to`rest_prepare_$CPTNAME` which will grab the url for the Custom Post Type's post featured image. In the example below, I want to add the featured image endpoint to my Flowers CPT, so it's `rest_prepare_flowers`. [snippet slug=custom-api-endpoint-featured-images lang=php] **Adding API endpoints for custom`post_tag` taxonomies** With WPD I have a variety of custom taxonomies for the CPT's I created, so I wanted to make sure that data is available via API endpoints too. The code I use to accomplish this is below. [snippet slug=custom-api-endpoint-tag-taxonomies lang=php] **Adding API endpoints for custom`category` taxonomies** The same set up can work for your custom category taxonomies too. [snippet slug=custom-api-endpoints-category-taxonomies lang=php] **Adding custom API endpoints for your metabox data** When you create custom post types, a lot of times you find yourself adding in custom metaboxes to suppor the data you need users to control through your Custom Post Type. This data can have a custom API endpoint created by using the following code snippet. The `$productsizes` array are the metabox information I needed for pricing in the WPD plugin so your set up may vary based on your metaboxes. [snippet slug=custom-api-endpoints-metaboxes lang=php] Once you have your custom post types, taxonomies and metaboxes API endpoints added, you can now allow developers to consume your API data and have more control over how the data gets displayed. **Custom API endpoints in action** You can look at an example of each of these endpoints being added into a live API by checking out the CannaBiz demo [here](https://www.wpdispensary.com/demo/wp-json/wp/v2/flowers).

## 2. oEmbed improvements

With [WP Dispensary](https://www.wpdispensary.com) I wanted to customize the output of information through the [Embeds](https://codex.wordpress.org/Embeds) so that the custom data I display within WPD's single item view gets embedded as well. The `filter` below will filter out `the_excerpt` and replace it with the_content, making sure any content you added into the output of `the_content` get's displayed properly. [snippet slug=oembed-customization-custom-post-types lang=php] Note that on line 15 there is the `wpd-oembed-wrap` ID, which you can change to anything you'd like and then add custom CSS to the public output of your plugin. [snippet slug=enqueue-custom-stylesheet-oembed lang=php] See how I handle adding this in with WP Dispensary [here](https://github.com/deviodigital/wp-dispensary/blob/2a7984cba6308498f3229d9035265bbdc7b2180d/public/class-wp-dispensary-public.php). Below is an example of how the WP Dispensary items get displayed through oEmbed now. https://www.wpdispensary.com/demo/flowers/chemdawg/

## 3. Flush rewrite rules during your plugin's activation

One thing that I looked over when building the earlier versions of the WPD plugin was `flush_rewrite_rules`. If I'm being completely honest, at the time I didn't even know it existed, so I was telling people in a FAQ page how to manually go in and resave their `permalinks` settings. We live and learn, right? ? Thankfully, WordPress does have a page [in the codex](https://codex.wordpress.org/Function_Reference/flush_rewrite_rules) on flush rewrite rules to look through. With the code below, I am able to take the Custom Post Type `function` and add it to the [activation hook](https://github.com/deviodigital/wp-dispensary/blob/master/wp-dispensary.php#L37-L40) within the WPD plugin. I also do the same for the custom [tag](https://codex.wordpress.org/Taxonomies#Tag) and [category](https://codex.wordpress.org/Taxonomies#Category) taxonomies for each menu type. [snippet slug=flush-rewrite-rules-plugin-activation lang=php] Now any time someone activates your plugin, your custom post types and taxonomies will flush and work with your current [permalink](https://codex.wordpress.org/Settings_Permalinks_Screen) settings.

## Additional resources

Now that we've gone over a few ways to enhance your CPT's, it's time to dig even further and see what else you can do to make your plugins better. Here's some links to other content that you can check out, written by people much smarter than I am ?

  * [5 Ways to Make your WordPress Plugin Really Extensible](http://www.ibenic.com/5-ways-make-plugin-extensible/)
  * [How to Make a WordPress Settings Autocomplete Field Using Ajax](https://hollerwp.com/wordpress-settings-autocomplete-field-using-ajax/)
  * [12 Most Useful WordPress Custom Post Types Tutorials](http://www.wpbeginner.com/wp-tutorials/12-most-useful-wordpress-custom-post-types-tutorials/)

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
