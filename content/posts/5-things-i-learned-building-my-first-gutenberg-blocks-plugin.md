---
title: "5 Things I’ve learned building my first blocks for Gutenberg"
description: "Over the last few months I've watched as Gutenberg has been developed, silently taking notes, watching for patterns and possible areas to excel in. Then I found that the domain Pillar.Press was available and it snapped…"
custom_url: "5-things-i-learned-building-my-first-gutenberg-blocks-plugin"
author: "Robert DeVore"
date: "2018-05-14"
canonical: "https://robertdevore.com/5-things-i-learned-building-my-first-gutenberg-blocks-plugin/"
template: "signal-a"
nav_hide: true
excerpt: "Over the last few months I've watched as Gutenberg has been developed, silently taking notes, watching for patterns and possible areas to excel in. Then I found that the domain Pillar.Press was available and it snapped…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

[WordPress Archive](/category/wordpress-archive/) · [WordPress](/tag/wordpress/)

Over the last few months I've watched as [Gutenberg](https://wordpress.org/gutenberg/) has been developed, silently taking notes, watching for patterns and possible areas to excel in. Then I found that the domain [Pillar.Press](http://pillar.press) was available and it snapped me into action. You see, for about 6 months I've had the name **Pillar** saved as a name idea for a headless WordPress theme I wanted to create. Last September,[Todd Motto](https://www.toddmotto.com) passed the [HTML5Blank](https://github.com/html5blank/) theme to me to take over development for. It hasn't received much in the way of updates over the past few years, but it has a strong following. I've cleaned it up a bit and launched a new [landing page](http://html5blank.com/), but it's code is so far behind WordPress standards I figure a fresh start was needed. The plan was to use the name **Pillar** as the _" refreshed"_ theme. Well, that's got a new plan, because after a random search in [Namecheap](https://namecheap.com) showed the **Pillar.Press** domain was available, the **Pillar** name is now being used for the [custom Gutenberg blocks](https://www.wordpress.org/plugins/pillar-press-content-blocks) I'm building. ![](/assets/legacy-images/banner_772x250.webp)

### Building Blocks with Pillar Press

If what they say is true, and [Gutenberg](https://wordpress.org/gutenberg/) is the future of WordPress, my hope is that [Pillar Press](http://pillar.press) becomes the cornerstone of content creation with WordPress. Since making the decision to use [**Pillar Press**](http://pillar.press) as the name for my custom Gutenberg blocks solution, I've jumped in head first with all of the knowledge I've soaked up over the last few months. As a WordPress developer who's lived in Windows for 20+ years, I've recently made the switch to Linux full time and I am extremely happy I have. I've learned a lot in these last few months, and feel that my skills as a developer have been growing at hyper-speed over the last few weeks while building [my first blocks plugin](https://www.wordpress.org/plugins/pillar-press-content-blocks). What better way to celebrate becoming a better developer than by documenting what you've learned on a recent project? _Insert Usher Confessions GIF here_

## How to use Node.js and NPM

While I've written a lot of code in my life, I've been weary of working with Node or NPM, composer, etc. Probably just the "if it ain't broke don't fix it" approach I had to my development for many years. So, this time around I've told myself that I'll do whatever is needed to learn Node and NPM. The first thing I did was check to make sure I already had Node and NPM installed. In the command line, you can do that like this: `node -v` and `npm -v`. If you need to install either of them on Linux, you can do check out the official documentation to find the method to [install via the package manager](https://nodejs.org/en/download/package-manager/). For Windows users, Treehouse has a nice write up on how you can [install Node and NPM on Windows](https://treehouse.github.io/installation-guides/windows/node-windows.html).

## How to use create-guten-block to build a Blocks plugin

If you do any serious work with WordPress and haven't heard of Ahmad Awais, you need to catch up Ahmad first put out a [Gutenberg Boilerplate](https://github.com/ahmadawais/Gutenberg-Boilerplate), then upgraded that to the [create-guten-block](https://github.com/ahmadawais/create-guten-block) solution for quickly building a Gutenberg Blocks plugin. Again, this type of development (command line) wasn't something I've been 100% comfortable with, so this pushed me outside of my comfort zones. I've learned how to run **NPM** and figuring out how the build process worked, how to add a**.gitignore** file to a project in order to keep the** node_modules** folder from being sent to [Github](https://www.github.com/pillarpress/pillar-press-content-blocks), and about a dozen other things.

## The more I use Gutenberg, the more I like it

When I first seen [Gutenberg](https://wordpress.org/gutenberg/), I hated it. I think my gut reaction was because of the fear that I'd have to learn something so far outside of my comfort zone as a developer. Over time, especially more recently as I've been developing for [Gutenberg](https://wordpress.org/plugins/gutenberg/), I've come to actually like the new content editor for WordPress. There's a learning curve, sure, but who cares? It's coming to WordPress regardless of how you and I feel about having to learn something new in order to continue building plugins and themes with WordPress. I realized that if I hated it so bad, I'd have to go learn some new CMS anyways, so why not stick with what I've developed with for over a dozen years? That way of thinking is paying off. After browsing articles, then installing and actually getting my hands dirty with [Gutenberg](https://wordpress.org/plugins/gutenberg/), I've found a hidden happiness when I tackle a new piece of code in a language I barely touched before, and quickly pick it up. The learning curve actually isn't that bad - and again, this is coming from a Windows developer who didn't do anything in a command line for almost all 20 years that I've been developing for the web.

## Things are changing FAST with Gutenberg's impending release

The first block I built was a **Spacer block** , because it seemed like the easiest one to start with since there was only one option - the height of the space between blocks. Well, in[Gutenberg v2.8](https://wordpress.org/plugins/gutenberg/) there is now a default **Spacer block** included. So, now I have the joy of removing the first block I built and the[Content Blocks plugin](https://www.github.com/pillarpress/pillar-press-content-blocks) it was a part of is left with one less block. But that's part of the fun in it all, right? The constant change means that as a developer you and I have to constantly think about our next moves and what's going to be best long-term. Another change that's happening right now is the move of several components from **wp.blocks** to **wp.editor**.

> Important [#Gutenberg](https://twitter.com/hashtag/Gutenberg?src=hash&ref_src=twsrc%5Etfw) change: we moved several `wp.blocks.*` components to `wp.editor.*` (RichText, PlainText, MediaUpload, …). This will help us move forward with some blocking points we had like accessing state from blocks, more detailed explanation: <https://t.co/cjMuB9088t> \-- Greg Ziółkowski (@gziolo) [May 7, 2018](https://twitter.com/gziolo/status/993491209422295040?ref_src=twsrc%5Etfw)

While not a huge change, it will cause problems for anyone who's built a Gutenberg compatible plugin up to this point and has their components added the old way. And again, that's the beauty of building alongside a plugin like Gutenberg, the constant change keeps you on your feet as a developer. Either that, or you fall miserably to your death in a pool of outdated skill-sets. [via GIPHY](https://giphy.com/gifs/someone-gifgun-gifsquid-dnkTPFmjAxyUg)

## Final thoughts

I'm excited to see where Gutenberg goes over the next few months as it makes it's way into WordPress core. I'm also excited to see **Pillar Press** grow into a powerful solution for WordPress users as they begin using Gutenberg. **What about you?** Have you started looking into Gutenberg yet and what you'll do to upgrade your WordPress skills to work with it? Or are you on the side of the fence that hates Gutenberg and everything it stands for?

## Related writing

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)

## Continue reading

**Newer:** [Thank You WordPress](/thank-you-wordpress/)

**Older:** [Back to Basics](/back-to-basics/)
