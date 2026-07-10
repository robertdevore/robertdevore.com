---
title: "How to Stop Your Plugins & Themes from Being Used on WordPress.com Hosting"
description: "In recent months, the WordPress® community has faced increasing challenges stemming from nuclear decisions made by Automattic’s CEO, Matthew Charles Mullenweg. During WordCamp US 2024, Mullenweg launched what he…"
custom_url: "how-to-stop-your-plugins-themes-from-being-used-on-wordpress-com-hosting"
author: "Robert DeVore"
date: "2024-12-22"
canonical: "https://robertdevore.com/how-to-stop-your-plugins-themes-from-being-used-on-wordpress-com-hosting/"
template: "signal-c"
nav_hide: true
excerpt: "In recent months, the WordPress® community has faced increasing challenges stemming from nuclear decisions made by Automattic’s CEO, Matthew Charles Mullenweg. During WordCamp US 2024, Mullenweg launched what he…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

[WordPress Archive](/category/wordpress-archive/) · [WordPress](/tag/wordpress/)

In recent months, the WordPress® community has faced increasing challenges stemming from nuclear decisions made by Automattic’s CEO, Matthew Charles Mullenweg.

During WordCamp US 2024, Mullenweg launched what he referred to as a “nuclear” war against WP Engine – a dick move that showed everyone what type of person was really in control of WordPress®.

This public display of hostility toward a core part of the WordPress® ecosystem has left many of us questioning the future of the open-source project.

WordPress® has always been about freedom: freedom to innovate, freedom to share, and freedom to choose. 

However, recent restrictions imposed on developers and hosting providers associated with WP Engine have undermined these principles. 

So let’s do something about it 😎

![Restricted plugin access for WordPress.com users](/assets/legacy-images/stop_plugin_usage_on_wordpress_com.webp)

As a direct statement against these actions, you can add a simple script to your plugins to stop them from being used on WordPress.com hosted websites – a platform that has increasingly prioritized control and cash over collaboration and community.

Let’s break down the code you can use in your plugins and themes to take a stand against the BDFL formerly known as Matthew Charles Mullenweg.

## The Code

The utility code prevents your plugins and themes from being activated or used on WordPress.com-hosted sites.

It’s designed to detect the WordPress.com environment, deactivate your plugin or theme automatically, and display appropriate notices to users.

You can install it with composer [via Packagist](https://packagist.org/packages/robertdevore/wpcom-check).

![WPCom Check composer install script](/assets/legacy-images/carbon_4.webp)

You can also find the code in it’s [GitHub repository](https://github.com/robertdevore/wpcom-check) to review in detail.

## How the Code Works

### Centralized Helper Class

The `WPComPluginHandler` class encapsulates all the key functionality:

  * **Environment Detection:** The `pluginCheck` method checks for the `IS_WPCOM` constant to determine if the site is hosted on WordPress.com.
  * **Plugin Deactivation:** If the site is hosted on WordPress.com, it ensures the plugin is deactivated and a deactivation notice is saved in the database.
  * **Scoped Execution:** The deactivation logic runs only in the admin context, ensuring frontend performance is unaffected.



### Automatic Deactivation

The `autoDeactivate` method is hooked into the `plugins_loaded` action, which runs after all plugins are loaded. If WordPress.com is detected, it deactivates the plugin automatically without further user interaction.

### User Feedback

  * **Admin Notice:** When the plugin is deactivated, an admin notice is displayed to inform users about the reason for deactivation and provides a link to learn more.
  * **Activation Block:** The `activationCheck` method hooks into the plugin activation process and blocks activation on WordPress.com sites. Users are shown a detailed error message explaining the restriction and a link to additional information.



### Improved Code Structure

  * **Namespace Usage:** All code is namespaced under `RobertDevore\WPComCheck` to prevent conflicts with other plugins or themes.
  * **Reusable Design:** By centralizing logic in a class, the functionality is modular, easy to maintain, and reusable across multiple plugins.



### How to Use the Class

Developers can integrate this functionality into their plugins with minimal effort. The only requirements are:

  1. Instantiating the `WPComPluginHandler` class in their plugin file.
  2. Providing the plugin slug and a link for users to learn more about the deactivation reason.

![Vince McMahon - Rejected WWE Gif](/assets/legacy-images/wwe_mcmahon_rejected.webp)

## Why Use This Code?

### Take a Stand for the Community

This script isn’t just about restricting your plugin.

It’s a statement against the centralization and overreach demonstrated by WordPress.com and Automattic’s (lack of) leadership. 

WordPress® developers deserve a level playing field – free from monopolistic B.S. that stifles innovation and community growth.

### Easy to Implement and Reuse

With the `wp_com_plugin_check` helper function, this script is designed to be reusable. 

You can drop it into any plugin with minimal modifications, simply updating the plugin slug, function prefixes and link to your custom “Learn More” page.

### Practical Benefits

  * Protect your plugin’s integrity by ensuring it isn’t used on a platform that undermines open-source values.
  * Clearly communicate your stance to users with professional and actionable feedback.

![Snoop Dogg - All money ain't good money - GIF](/assets/legacy-images/snoop_all_money_aint_good_money.webp)

BRB, I got [a LOT of plugins](/wordpress-and-woocommerce-plugins/) to update 😎

## Related writing

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)

## Continue reading

**Newer:** [Introducing Delete Inactive Users](/introducing-delete-inactive-users/)

**Older:** [Host Your WordPress Plugins on GitHub and Automate Plugin Packaging](/host-your-wordpress-plugins-on-github-and-automate-plugin-packaging/)
