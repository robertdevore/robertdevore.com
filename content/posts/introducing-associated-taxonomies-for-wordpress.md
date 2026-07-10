---
title: "Introducing Associated Taxonomies for WordPress®"
description: "I’m thrilled to announce the release of Associated Taxonomies , a free WordPress® plugin designed to streamline taxonomy management by enabling you to associate terms within the same taxonomy. This plugin was built with…"
custom_url: "introducing-associated-taxonomies-for-wordpress"
author: "Robert DeVore"
date: "2024-12-09"
canonical: "https://robertdevore.com/introducing-associated-taxonomies-for-wordpress/"
template: "signal-a"
nav_hide: true
excerpt: "I’m thrilled to announce the release of Associated Taxonomies , a free WordPress® plugin designed to streamline taxonomy management by enabling you to associate terms within the same taxonomy. This plugin was built with…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

[WordPress Archive](/category/wordpress-archive/) · [WordPress](/tag/wordpress/)

I’m thrilled to announce the release of **[Associated Taxonomies](https://github.com/robertdevore/associated-taxonomies/)** , a free WordPress® plugin designed to streamline taxonomy management by enabling you to associate terms within the same taxonomy.

This plugin was built with simplicity, flexibility, and usability in mind, making it easier for administrators to create meaningful relationships between terms.

![Snoop Nodding GIF](/assets/legacy-images/snoop_nodding_1.webp)

## Why I Built Associated Taxonomies

I’ve run into the issue of 2 sub-categories with the same name forcing one to add a number to the slug, which is less than ideal 🤦‍♂️

I also often encountered situations where associating terms within the same taxonomy would have added significant value to taxonomy-based content management.

Unfortunately, WordPress® doesn’t natively support this functionality.

Recognizing this gap, I set out to develop a solution that was not only functional but also easy to use for both developers and site administrators.

![Associated Taxonomies Settings](/assets/legacy-images/associated_taxonomies_settings_field.webp)

## Key Features

Here’s what makes **Associated Taxonomies** stand out:

  * **Associate Terms with Ease** : Add, edit, and manage associated terms directly from the taxonomy term management pages.
  * **Dynamic Integration** : Automatically hooks into all public taxonomies, so there’s no need for manual setup.
  * **Shortcode Support** : Display associated terms or posts with parent and child term relationships using simple shortcodes.
  * **Custom Admin UI** : Select2-powered multi-select dropdowns ensure an intuitive and smooth user experience.
  * **Frontend Styling** : Includes styling to display associated terms cleanly and beautifully on your site.



## How It Works

### Associating Terms

With Associated Taxonomies, associating terms is seamless:

  1. Navigate to the taxonomy management page in the WordPress admin.
  2. Use the “Associated Terms” dropdown to select terms while creating or editing a taxonomy term.
  3. Save the term, and the associations are stored in the term meta.

![Associated Taxonomies shortcode display](/assets/legacy-images/associated_taxonomies_shortcode_display_1024x412.webp)

### Displaying Associated Terms

You can display associated terms on your site using the `[related_terms]` shortcode:

> [related_terms id=”123″ taxonomy=”category”]

Replace `123` with the term ID and `category` with the taxonomy name.

### Displaying Posts by Related Terms

Want to show posts related to specific parent and child terms? Use the `[posts_by_related_terms]` shortcode:

> [posts_by_related_terms parent=”12″ child=”34,56″ taxonomy=”category”]

This flexibility allows you to create dynamic and meaningful content relationships.

## Get Started

Installing and using Associated Taxonomies is simple:

  1. [Download the plugin](https://github.com/robertdevore/associated-taxonomies/) from GitHub.
  2. Upload the plugin to your WordPress site and activate it.
  3. Start associating and managing terms like never before!

![Snoop Nodding GIF](/assets/legacy-images/snoop_nodding_2_1.webp)

## A Note to the Community

Associated Taxonomies was developed with the WordPress® community in mind.

Whether you’re managing a small blog or a large-scale content site, this plugin can help you unlock new possibilities for taxonomy management.

I’d love to hear your feedback, suggestions, or ideas for future updates.

Feel free to reach out on [GitHub](https://github.com/robertdevore/associated-taxonomies/) or through my [contact form](/).

Thank you for supporting independent developers and open-source projects 🤘

## Related writing

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)

## Continue reading

**Newer:** [Introducing Site Vitals for WordPress®](/introducing-site-vitals-for-wordpress/)

**Older:** [Introducing Maintenance Mode for WordPress®](/introducing-maintenance-mode-for-wordpress/)
