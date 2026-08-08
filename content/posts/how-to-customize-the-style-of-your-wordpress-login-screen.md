---
title: "How to customize the style of your WordPress login screen"
description: "This post is going to show you how to add a few small code snippets to change the appearance of the WordPress login screen. We’ll walk through the process of changing the default WordPress logo to your own using the…"
custom_url: "how-to-customize-the-style-of-your-wordpress-login-screen"
author: "Robert DeVore"
date: "2019-06-27"
canonical: "https://robertdevore.com/how-to-customize-the-style-of-your-wordpress-login-screen/"
template: "signal-c"
nav_hide: true
excerpt: "This post is going to show you how to add a few small code snippets to change the appearance of the WordPress login screen. We’ll walk through the process of changing the default WordPress logo to your own using the…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

This post is going to show you how to add a few small code snippets to change the appearance of the WordPress login screen.

We’ll walk through the process of changing the default WordPress logo to your own using the `login_headertext` filter that was added in WordPress 5.2

And I’m going to break down how to change various other styles, giving you the ability to style your login screens to match your website branding.

I was recently working on the registration flow of WP Dispensary’s [eCommerce add-on](https://www.wpdispensary.com/product/ecommerce) and realized there’s a few places that the default WordPress login page are lacking from a branding perspective.

![](/assets/legacy-images/wp_login_default_screen.webp)

So I decided I had to change that.

Since the [CannaBiz](/cannabiz/) theme I built for [WP Dispensary](https://www.wpdispensary.com/) already has areas in the Customizer for the logo upload and multiple color styles, I knew it wouldn’t be too hard to update the login page style to match the front-end design.

Previous to WordPress version 5.2, the most common way to change the logo on the login screen was with CSS style updates to display yours properly.

These codes can be found in the Codex which shows you [how to customize the login form](https://codex.wordpress.org/Customizing_the_Login_Form).

With WordPress v5.2 we can now use the newly added `logo_headertext` filter in the `wp-login.php` file to display your logo image.

Here’s an example of what you can do with the updated login screen style for WordPress.

![](/assets/legacy-images/cannabiz_login_screen_wp_dispensary.webp)

## Using the new filter added in WP v5.2

You can find the `logo_headertext` filter in the **wp-login.php** file in your website’s root directory.

We’ll be looking for this bit of code below.

[snippet slug=wp-login-php-filter lang=php]

You can also view the full **wp-login.php** file on Github at the following [link](https://github.com/WordPress/WordPress/blob/master/wp-login.php). 

## Adding your logo with a custom filter

Now that we found the filter, let’s add some code to change out the WordPress logo and replace it with an image of our own.

These changes will go in your theme **functions.php** file (or a custom plugin).

[snippet slug=acme_login_logo_image lang=php]

Next, we’re going to want to remove the default CSS styles that WordPress applies to the logo image so ours new logo fits properly within the space and re-sizes automatically depending on logo size.

[snippet slug=acme_login_logo_image_styles lang=php]

## Extending the code to work with the customizer

Once you have the logo added, your login screen will feel like it’s starting to take shape, but what about the background color, button colors, and link colors?

That’s where your Customizer codes come into place!

![](/assets/legacy-images/duh_michelle_tanner.webp)

In the [CannaBiz theme](https://www.wpdispensary.com/product/cannabiz), I have options for button background and text colors, text link colors, plus the logo image upload. 

I’ll be using these settings to style the login page of my website, which you can see in the updated codes below.

### Adding a logo image from the customizer

Below is the updated filter code which replaces the first piece of code we added earlier in the article.

[snippet slug=acme_login_logo_image_2 lang=php]

As you can see in the above code, we’re using [get_theme_mod](https://codex.wordpress.org/Function_Reference/get_theme_mod) and checking to see if the logo file is present.

This way, if no logo is uploaded, none of the code changes will occur, and nothing will be altered on the front-end view.

Next, we’ll be updating the CSS for the text and button links.

### Adding text & button link styles from the customizer

I wanted to utilize the text link colors and button colors I added in the CannaBiz theme so the login page matches the website design even more.

The code below adds in text link colors and will be added along with the CSS we added in the second code example in this article.

You can change the `get_theme_mod` instances to match your color options names.

[snippet slug=acme_login_logo_image_css_links lang=css]

The next step is to update the button on the page to match the colors and style of the buttons added in my theme.

The CSS codes below make the button full width and adds the background color and text colors I have in the theme customizer.

[snippet slug=acme_login_logo_image_css_button_links lang=css]

### Changing the login screen background color

The last step to making the login screen really feel like a part of your website brand is to change the background color to match your website.

The code below uses the background color option added to the theme customizer.

[snippet slug=acme_login_logo_image_css_background lang=css]

## See the code in action

Check out the WP Dispensary demo server’s [login screen](https://www.wpdispensary.com/demo/wp-login.php) to see the above code’s being used via the CannaBiz theme’s styles.

Hopefully this article helped you get a better looking login screen for your website, without the need to use _another_ plugin.

![](/assets/legacy-images/bob_ross_glad_you_could_join_me_today.webp)

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
