---
title: "? hue.js"
description: "I forked a color picker for WordPress I know what you're thinking. _Isn 't there a color picker in WordPress already? _ Yeah … ? Not another color picker?!?! Why a color picker for WordPress? Technically, the hue.js…"
custom_url: "hue-js"
author: "Robert DeVore"
date: "2018-04-03"
canonical: "https://robertdevore.com/hue-js/"
template: "signal-b"
nav_hide: true
excerpt: "I forked a color picker for WordPress I know what you're thinking. _Isn 't there a color picker in WordPress already? _ Yeah … ? Not another color picker?!?! Why a color picker for WordPress? Technically, the hue.js…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

[WordPress Archive](/category/wordpress-archive/) · [WordPress](/tag/wordpress/)

## I forked a color picker for WordPress

I know what you're thinking. _Isn 't there a color picker in WordPress already?  
_ Yeah … ? ![](/assets/legacy-images/dj_khaled_another_one_2.webp)Not another color picker?!?!

## Why a color picker for WordPress?

Technically, the [hue.js](https://www.github.com/deviodigital/hue.js) color picker works independently of WordPress, so it's not a color picker for WordPress at all. But to understand "_why a color picker for WordPress "_ , we have to go a couple of steps back to where the idea originally stems from. I've been working on version 2.0 ([#WPD2](https://twitter.com/hashtag/WPD2?src=hash&lang=en)) of [WP Dispensary](https://www.wpdispensary.com/) and a couple of weeks ago I ran into an issue when figuring out the best approach for a specific portion of the release - the `Settings` page. So, I did what any grown ass man does when he runs into a problem… I jumped on Twitter ?

> Any framework/code recommendations for a plugin's settings page, with tabbed areas? Not sure if there's some sort of standard but if there is, I haven't been able to find it yet. \-- Robert DeVore (@deviorobert) [March 16, 2018](https://twitter.com/deviorobert/status/974451130578145280?ref_src=twsrc%5Etfw)

Luckily for me, there's a lot of dope developers in the WordPress community and I got recommendations to some nice solutions, but one stuck out in particular. [Ahmad Awais](https://twitter.com/MrAhmadAwais/) reached out and let me know about the [WP OOP Settings API](https://github.com/AhmadAwais/WP-OOP-Settings-API) he built and after looking it over, I knew I wanted to use this as the base code for the Settings page rebuild in [#WPD2](https://twitter.com/hashtag/WPD2?src=hash&lang=en). [![](/assets/legacy-images/wposa_300x188.webp)](https://github.com/AhmadAwais/WP-OOP-Settings-API)WP OOP Settings API It wasn't long until I was working with Ahmad on WPOSA and became the project lead for the release of version 2.0. _More info on v2.0 of WPOSA coming soon_ ? While working on the **WP OOP Settings API** I had to update the outdated color picker it was using and found [Iris](http://automattic.github.io/Iris/). Iris was initially developed for [Custom Colors](http://en.blog.wordpress.com/2012/07/11/go-ahead-add-a-splash-of-color/) on WordPress.com and eventually shipped with WordPress starting in version 3.5.

## Sticking a fork in the Iris ?

[Iris](http://automattic.github.io/Iris/) is well built, _and_ it comes prepackaged with WordPress, so there's less work required for developers who need a color picker in their projects. But it hasn't been updated on [Github](https://github.com/Automattic/Iris) in over 2 years, and there are a couple of nice PR's just waiting there to be merged. I wanted those updates in my code and figured that while updating my version of the files, I'd also fork Iris and work on making the code better, while simultaneously learning JavaScript in the process. I mean, we're all supposed to [Learn Javascript Deeply](https://javascriptforwp.com/parts/javascript/), right?

## Contributing to open source

The way I see it is this: I may be the only person who ever needs to use this specific color picker within a WordPress. context **I 'm fine with that.** I may also learn a lot of JavaScript over the next year or two and incorporate that into additional updates for[hue.js](https://github.com/deviodigital/hue.js) that I can also submit as PR's to Iris. **I 'm also fine with that.** Regardless of what happens to this code within the next 6 days, 6 months or 6 years is irrelevant. The code being available for the next person to download and enhance to their needs, whenever they may need it is what's important to me. That's the beauty of Open Source. I'm happy to play my part in it, no matter how big or small of an impact my contributions end up having. Open source code is how I ended up turning an open source project into my full time business: [WP Dispensary](https://www.wpdispensary.com). I plan to give back as much as I can, as long as I can, because without open source code, [I wouldn't be here](/about/). I am grateful for WordPress and everyone who's played their part in it being here this many years later.

## ? hue.js download

You can download [hue.js](https://github.com/deviodigital/hue.js) from the command line:

> git clone https://github.com/deviodigital/hue.js

Want to download a zip file? You can do that [here](https://github.com/deviodigital/hue.js).

## Adding hue.js to your project

Being able to use hue.js in your project is pretty simple. First, you need to download the files (see above). You then need to copy over the `hue.js` file into your project and add it, like below.

> Now, you can now initiate the hue color picker by attaching it to a specific class, for instance `color-picker`.

> $('.color-picker').hue();

That's all there is to it. Now, anywhere the class is called (for instance, on a text input field), it will initiate the color picker. ![](/assets/legacy-images/color_picker.webp)example color picker

### Bug reports & Pull requests

Just a note to let you know bug reports & pull requests are always welcome ?

## Related writing

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)

## Continue reading

**Newer:** [Set Featured Images Programmatically in WordPress](/set-featured-images-programatically-wordpress/)

**Older:** [WP Dispensary: 2 years after the launch](/two-years-building-wp-dispensary/)
