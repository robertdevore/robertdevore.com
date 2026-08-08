---
title: "Introducing Media Copyright Scanner"
description: "I’m excited to introduce my latest plugin 👀 Media Copyright Scanner . This free tool is crafted to assist website owners, content managers, and developers in identifying potentially copyrighted images within their…"
custom_url: "introducing-media-copyright-scanner"
author: "Robert DeVore"
date: "2024-12-02"
canonical: "https://robertdevore.com/introducing-media-copyright-scanner/"
template: "signal-c"
nav_hide: true
excerpt: "I’m excited to introduce my latest plugin 👀 Media Copyright Scanner . This free tool is crafted to assist website owners, content managers, and developers in identifying potentially copyrighted images within their…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

I’m excited to introduce my latest plugin 👀 **[Media Copyright Scanner](https://github.com/robertdevore/media-copyright-scanner/)**.

This free tool is crafted to assist website owners, content managers, and developers in identifying potentially copyrighted images within their WordPress® Media Libraries.

Many stock image providers actively monitor the unauthorized use of their assets, making it crucial for website owners to ensure all images are properly licensed.

The [Media Copyright Scanner](https://github.com/robertdevore/media-copyright-scanner/) plugin serves as a proactive solution to help you audit your Media Library and maintain compliance. 

![Media Copyright Scanner - Scan Results](/assets/legacy-images/media_copyright_scanner_plugin_screenshot.webp)

Here’s how it can benefit you:

## Comprehensive Scanning

  * **Thorough Analysis** : Scans filenames, titles, alt text, and descriptions of your media files.
  * **Detects Common Patterns** : Identifies images from well-known stock image providers such as Getty Images, Shutterstock, iStockPhoto, and many more (50+)



## User-Friendly Interface

  * **Seamless Integration** : Accessible via the WordPress admin area under the Media menu.
  * **Easy to Use** : Start scans with a single click and monitor progress through a visual progress bar.



## Actionable Results

  * **Detailed Reporting** : Provides a list of media items that may require your attention, including details like Media ID, Filename, Title Text, Alt Text, Description, and Identified Source.
  * **Flag Safe Images** : Allows you to mark images you know are compliant as safe, excluding them from future scans.
  * **CSV Export** : Export the scan results for record-keeping or further analysis.



## Customizable and Extensible

  * **Custom Patterns** : Add or modify scanning patterns using filters to suit your specific needs.
  * **Adjustable Batch Processing** : Modify the batch size to optimize performance based on your Media Library size.

![Snoop nodding in agreement GIF](/assets/legacy-images/snoop_nodding.webp)

## Why This Plugin Matters

### Mitigate Legal Risks

By regularly scanning your Media Library, you can identify and address potential copyright infringements before they become legal issues.

### Support Ethical Practices

Ensure that you’re respecting the intellectual property rights of photographers and creators, promoting a culture of fairness and legality.

### Save Time and Resources

Automate the tedious process of manually checking each media file, freeing up time to focus on creating great content.

## Getting Started

### Installation

  1. **Download the Plugin** : Visit the [GitHub repository](https://github.com/robertdevore/media-copyright-scanner/) to download the plugin.
  2. **Install and Activate** : Upload the plugin to your WordPress site and activate it through the `Plugins` menu.



### Using the Plugin

  1. **Access the Scanner** : Navigate to `Media` > `Copyright Scanner`.
  2. **Initiate Scan** : Click the `Start Scan` button.
  3. **Review Results** : Examine the list of potentially copyrighted images.
  4. **Take Action** : 
     * **Flag Safe Images** : Select images you are certain are compliant and click `Save Flags`.
     * **Address Issues** : For images that may be in violation, consider replacing them or obtaining proper licenses.



## Extending Functionality

### Custom Patterns

If your website uses images from specific sources not included by default, you can easily add custom patterns:

``` add_filter( 'mcs_patterns', function( $patterns ) { $patterns['Your Custom Source'] = [ '/your-custom-pattern/i' ]; return $patterns; } ); ``` 

### Adjusting Batch Size

Optimize scanning performance for large Media Libraries:

``` add_filter( 'mcs_scan_media_batch_size', function() { return 50; // Adjust based on your server capabilities } ); ``` 

## Looking Ahead

This initial release is just the beginning.

I’m ready, wiling and able to expand the plugin’s capabilities based on user feedback and evolving needs 🤘

Download the **Media Copyright Scanner** plugin [from GitHub](https://github.com/robertdevore/media-copyright-scanner) and take control of your website’s media content – then tell me what you think 💯

Thank you for your continued support, and I look forward to hearing how this tool helps you 🙏

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
