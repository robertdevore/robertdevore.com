---
title: "Chapters for Authors"
description: "It's amazing what you can come up with randomly over the weekend while doing a dozen other things ? Case in point - Chapters for Authors ? This is a new plugin I built from an idea I got when I read a tweet from Ines…"
custom_url: "chapters-for-authors-wordpress-plugin"
author: "Robert DeVore"
date: "2016-09-27"
canonical: "https://robertdevore.com/chapters-for-authors-wordpress-plugin/"
template: "signal-b"
nav_hide: true
excerpt: "It's amazing what you can come up with randomly over the weekend while doing a dozen other things ? Case in point - Chapters for Authors ? This is a new plugin I built from an idea I got when I read a tweet from Ines…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

It's amazing what you can come up with randomly over the weekend while doing a [dozen](https://www.wpdispensary.com/downloads/dispensary-top-sellers/) other [things](https://www.wpdispensary.com/100-free-marijuana-stock-photos/) ? Case in point - [Chapters for Authors](https://wordpress.org/plugins/chapters-for-authors/) ? This is a new plugin I built from an idea I got when I [read a tweet](https://twitter.com/themotherofcode/status/780061617698533376) from Ines van Essen, who is building a plugin for bloggers to gamify their blogging.

> I'm building a thing. It's scary, which is why I am writing about it. Also, I want to pick your brain. <https://t.co/w2Z1ErzeLs> \-- Ines 🇺🇦 (@motherofcode) [September 25, 2016](https://twitter.com/motherofcode/status/780061617698533376?ref_src=twsrc%5Etfw)

Her plugin, [Bloggerpoints](https://wpbloggerpoints.com/2016/09/say-hi-to-bloggerpoints/) will reward authors for writing consistently and hitting specific word counts. A badge of honor, so to speak, for bloggers. I thought it may be a good idea for those authors, who more than likely will also be writing for NaNoWriMo this November, to have a place in WordPress to write their book. I'll be committing myself this November to [NaNoWriMo](http://nanowrimo.org/) plus I also spend a lot of time in my WordPress dashboard, so this will be a time saving, self-serving plugin. If you plan on writing and want to easily read over and share your book with the world, this plugin is perfect for you, too.

## Installing Chapters for Authors

You can download the Chapters for Authors WordPress plugin via the [official WordPress plugin repository](https://wordpress.org/plugins/chapters-for-authors/). You can also download it directly from your WordPress dashboard by going to `Plugins - Add New` and searching for WP Dispensary. If you're the adventurous type, you can get the plugin [from Github](https://github.com/deviodigital/chapters-for-authors) 🙂 **Flushing Permalinks** After you install the plugin, make sure to re-save your permalinks to flush the settings and let the Chapters plugin link properly.

## Creating Chapters

So once you have the plugin installed, you'll want to start writing immediately. I mean, why wouldn't you? 🙂 ![Chapters for Authors dashboard screenshot](/assets/legacy-images/screenshot_1.webp)Chapters for Authors dashboard screenshot In your dashboard menu, you'll now see the "Chapters" post type. This is where you can publish the chapters from your book, categorize your chapters by book and tag characters.

### Books

![chapters-for-authors_books-taxonomy](/assets/legacy-images/chapters_for_authors_books_taxonomy.webp)When publishing new chapters, there is a Books taxonomy where you can categorize your chapters by book. Looking to write and publish a lot of books? Then this will be how you can do it. If your permalinks are set to `/%postname%/` then your Book's URL will be `www.yourwebsite.com/book/book-title`

### Characters

Tagging the Characters that appear in each chapter makes it easy to see how often characters appear throughout your book, link your readers to all of the times their favorite character appears in your book, etc. Don't have characters in your book? No problem! At the top right of the Add New Chapter page, you'll see a Screen Options button. [![click to view full size](/assets/legacy-images/chapters_for_authors_screen_options_1024x222.webp)](/assets/legacy-images/chapters_for_authors_screen_options_1024x222.webp)click to view full size Clicking and opening this up lets you un-check the Characters option, hiding it from your screen forever 🙂

### Introduction Quotes

![chapters-for-authors_introduction-quote](/assets/legacy-images/chapters_for_authors_introduction_quote.webp)The Chapters for Authors plugin also adds in a custom meta box for you to add in a quote & author name. In a lot of the books I read, there's a nice quote on the first page of each chapter, so this meta box will allow you to save your own quote. You can output the quote by using the following php code: https://gist.github.com/robertdevore/b17161c8b38ec490b4c8e3e0dacc6114

## Thank yous

First, I would like to thank Ines for building a plugin for building something and talking about it. That spark is what brought this plugin to life! When building the plugin, I utilized the [WordPress Plugin Boilerplate Generator](http://wppb.me/) to quickly make the base code for the plugin. The Chapters custom post type was built with the [Post Type Generator](https://generatewp.com/post-type/) and I re-used the code from taxonomies and meta boxes in WP Dispensary to build out the custom taxonomies and meta boxes in Chapters for Authors. If you're looking for easy taxonomy and meta box generators, [GenerateWP](https://generatewp.com/generator/) has you covered! Building a plugin like this can be done really quick when you have the right system in place.

## The road ahead

I'll be actively developing this plugin over [on Github](https://github.com/deviodigital/chapters-for-authors), so feel free to submit code or [open issues](https://github.com/deviodigital/chapters-for-authors/issues). **There is a also paid version of this plugin in the works.** I am not set on a date yet because there's a couple features I want to make sure I'm getting 100% right. It is definitely coming though and if the build speed for the free plugin is any indication, I see it happening sooner rather than later. I mean, NaNoWriMo is coming up really soon 🙂

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
