---
title: "Leafly Reviews"
description: "You know those moments in your life where you step back and look around, knowing that things are about to change? Yeah, I'm having one of those moments right now. I've wrote a lot of code in my lifetime and customized…"
custom_url: "leafly-reviews-wordpress-plugin"
author: "Robert DeVore"
date: "2015-10-15"
canonical: "https://robertdevore.com/leafly-reviews-wordpress-plugin/"
template: "signal-a"
nav_hide: true
excerpt: "You know those moments in your life where you step back and look around, knowing that things are about to change? Yeah, I'm having one of those moments right now. I've wrote a lot of code in my lifetime and customized…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

[WordPress Archive](/category/wordpress-archive/) · [WordPress](/tag/wordpress/)

You know those moments in your life where you step back and look around, knowing that things are about to change? Yeah, I'm having one of those moments right now. I've wrote a lot of code in my lifetime and customized other WordPress plugins in the past, but today marks a special moment in history, for me at least, because I am officially releasing my first WordPress plugin.

## Leafly Reviews WordPress plugin

As a dispensary owner, or developer who works with marijuana dispensaries, you've undoubtedly heard of the Leafly website before. Odds are very high that a dispensary worth anything has a profile on Leafly and is getting reviews from patients. Until today, there was not an easy way to showcase those reviews on your own website. That's all about to change. **Introducing Leafly Reviews for WordPress!** This free WordPress plugin gives you a way to easily display your dispensary reviews from Leafly on your own website through the use of a widget or shortcode.

### Download

I'd suggest reading the entire post, but if you just can't wait to get your hands on the plugin, you can click here to be taken to the bottom of the post with the download links.

### Adding your APP ID and KEY

Once you install this plugin, you'll notice a new options page in your WordPress dashboard under the Settings section, titled "Leafly Reviews". On this page, you'll be able to add in your APP ID and KEY, which is needed for the plugin to work. Not sure where to get your APP ID and KEY? You get them from the [Leafly Developer](http://developer.leafly.com/) area, which lets you sign up for an account and create an app. When you create the app, you'll be given a KEY and ID to use, which is what you'll need to copy over to this plugin's settings page. **Caching built in** Leafly gives their API users a limit of 25 hits per day for their**seed** account, or 60 hits per minute for their** bloom** account. To help your dispensary utilize this plugin without needing to upgrade to bloom, and taking too many hits to your account, I've built in a cache that refreshes once per hour. There's nothing that you need to do on your end in order to get this to work, it's baked right in to the plugin - pardon the pun 🙂

### Widget Options

![leafly-reviews-wordpress-plugin-widget](/assets/legacy-images/leafly_reviews_wordpress_plugin_widget.webp)After you install the Leafly Reviews WordPress plugin, you'll be able to add a custom widget to your website's sidebar (or anywhere else that widgets are enabled in your theme). The widget is colored green, so you'll be able to easily spot it on your widgets page. Drag it into place where ever you'd like it to show, and fill in the options, which you can see to the left. Here, you can add in your dispensaries URL slug and the amount of reviews you'd like to show (limit: 100). You can also select if you want to show the reviewer's avatar, the star rating, individual ratings for meds, service and atmosphere, if the user reviewer would recommend your dispensary and shop there again, and also show the reviewers comments.

### Shortcode Options

A secondary option built into the plugin to display your reviews from Leafly is the shortcode. Sometimes, it might be a better option to show reviews on a page of your website (for instance, the home page), so the shortcode will give you all of the flexibility you need. Here is the basic shortcode: `[leaflyreviews slug="denver-relief"]` You will need to add in your slug, just like the widget options. The shortcode will default to showing 5 reviews, and all of the options given in the widget (avatar, star rating, detailed rating, recommendation, shop again and comments. If you'd like to remove some of these options from showing, you can add the option to the shortcode with the value of _no_ , like this: `[leaflyreviews slug="denver-relief" limit="5" avatar="no" stars="no" ratings="no" recommend="no" shopagain="no" comments="no"]`

## Credits & Thank-you's

Without the open source projects below, this plugin would have never came together the way that it has. I'd like to say thank you to everyone who was indirectly a part of this WordPress plugin's release.

  * [Leafly Developer Center](http://developer.leafly.com)
  * [WordPress Plugin Boilerplate](http://wppb.me/)
  * [PHP SimpleCache](http://github.com/gilbitron/PHP-SimpleCache)
  * [Font Awesome](http://www.fontawesome.io)



## Download

**Leafly closed it 's API, so as of 2.29.16, this plugin no longer works.** I will be keeping an eye out if an API ever opens back up and I can update this plugin. Still want to check the plugin out anyways? You can download the Leafly Reviews WordPress plugin via the[official WordPress plugin repository](http://wordpress.org/plugins/leafly-reviews/). You can also download it directly from your WordPress dashboard by going to `Plugins - Add New` and searching for **Leafly Reviews**.

## The road ahead

Thank you for taking the time to read this entire release post. Right now, the plugin is going to sit while it gets tested out by various dispensaries in order to find any bugs that need fixed. I've also got plans in the future to add an option for the user to select the amount of time that passes before the cache refreshes itself, as well as a couple of other enhancements. Want to contribute to the plugin? Head over to the [Github repository](http://github.com/deviodigital/leafly-reviews-wordpress-plugin) and submit any issues you find or pull requests. Your contributions are both welcomed and appreciated.

## Related writing

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)

## Continue reading

**Newer:** [WP Dispensary](/wp-dispensary/)

**Older:** [Focus](/focus/)
