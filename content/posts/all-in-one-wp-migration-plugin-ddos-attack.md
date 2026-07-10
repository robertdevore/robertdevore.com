---
title: "WordPress plugin with 5M+ active installs can be utilized in DDoS attacks"
description: "While doing some vulnerability research for WordPress plugins myself and my clients use, I came across a plugin with 5M+ active installs that can be used in DDoS attacks by non-authenticated users. Let me preface this…"
custom_url: "all-in-one-wp-migration-plugin-ddos-attack"
author: "Robert DeVore"
date: "2023-09-30"
canonical: "https://robertdevore.com/all-in-one-wp-migration-plugin-ddos-attack/"
template: "signal-c"
nav_hide: true
excerpt: "While doing some vulnerability research for WordPress plugins myself and my clients use, I came across a plugin with 5M+ active installs that can be used in DDoS attacks by non-authenticated users. Let me preface this…"
categories: ["WordPress Archive"]
tags: ["WordPress", "WooCommerce"]
---

[WordPress Archive](/category/wordpress-archive/) · [WordPress](/tag/wordpress/) · [WooCommerce](/tag/woocommerce/)

While doing some vulnerability research for WordPress plugins myself and my clients use, I came across a plugin with 5M+ active installs that can be used in DDoS attacks by non-authenticated users.

> Let me preface this to say that the plugin itself is not vulnerable to a hack AFAIK, but has a flaw (IMO) that allows non-authenticated users to trigger full site backups without any limitations.

The plugin in question is [All In One WP Migration](https://wordpress.org/plugins/all-in-one-wp-migration/) from [ServMask](https://servmask.com).

I submitted this vulnerability to [Patchstack](https://patchstack.com) but it was rejected because it requires a secondary vulnerability. 

I also reached out to ServMask support back in early July and discussed this issue with them.

Their first response said it wasn’t a big deal 🤔

Then I had a few follow ups with their CTO Bobby Angelov, who said he’d talk to the team and look into it, but I never received any follow up.

![Ghosted GIF](/assets/legacy-images/ghosted_ignored.webp)

## How the exploit works

The scenario I’m talking about is if someone uses a secondary exploit (like [this one](https://www.exploit-db.com/exploits/50052)) to read the `wp_options` table. 

Or as Snicco [pointed out](https://snicco.io/vulnerability-disclosure/malcare/site-takeover-through-stolen-api-credentials-in-combination-with-sqli-malcare-5-09#description) recently:

> This is exploitable **if** **any of the below pre-conditions are given** :
> 
>   * The site has one of the [never-ending read-SQLi vulnerabilities](https://patchstack.com/database/) in any plugin, theme, or WordPress Core. [This recently happened with WooCommerce Stripe keys](https://webdesigneracademy.com/my-stripe-account-was-hacked-and-stripe-said-i-have-to-repay-70k/).
>   * The [site’s database is compromised at the hosting level](https://aboutus.godaddy.net/newsroom/company-news/news-details/2021/GoDaddy-Announces-Security-Incident-Affecting-Managed-WordPress-Service/default.aspx?fbclid=IwAR2zz6g0XEpSl5pGkNfe3GOhEXFgE-XRIyQVDFIMOvKqBs3AVfsIXHflmrg).
>   * Other methods that allow reading or updating WordPress options (wp_options), such as this [wildly exploited Elementor vulnerability](https://patchstack.com/database/vulnerability/elementor-pro/wordpress-elementor-pro-3-11-6-authenticated-arbitrary-options-change-vulnerability).
> 


Using one of the above methods, the attacker could grab the `ai1wm_secret_key` that AIOWPM uses and trigger a backup without ever logging into the site.

This keeps their exploit stealthy compared to adding a user that may get spotted by a website owner/maintenance company.

Once the user has the key, they can send request to this URL:

> **http://VICTIMSITE.com/wp-admin/admin-ajax.php?action=ai1wm_export &ai1wm_import=1&secret_key=SECRET_KEY_HERE&complete=1**

Doing this, while logged out, will trigger a full backup of the website, which in a lot of cases will be 2GB+ (think photographer sites or food blogs with lots of images).

By having this capability, as an attacker I would be able to trigger a DDoS attack on the site by simply creating a python script that requests the URL 100+ times consecutively.

I did this already, and it took ~30 minutes to create (no, I won’t share this script so don’t ask).

That will overload the server resources both from a disk space perspective, as well as resources being brought to a halt trying to generate backups of the site 100+ times.

For reference, the [second largest](https://cln.sh/Fh8xbzg7h5vpSK0y0kjT) managed hosting plan from WPEngine allows for 50GB of space. That means 25 requests on a 2GB website is going to max it out.

![Maxed out Workaholics GIF](/assets/legacy-images/maxed_out_workaholics_adam.webp)That’s gonna hurt 👀

## Recommendation to mitigate this issue

This isn’t 100% the AIOWPM plugin’s issue since it _does_ require a secondary exploit.

But since there are active exploits in the wild that give access to the secret key, I believe that it’s worth hardening this functionality.

A quick solution would be to limit the amount of backups that can be created per X minutes.

Doing this would help mitigate the risk since it would likely give the website owners and the hosting companies time to notice backups being generated and disk space filling up.

It would also limit the likelihood that the DDoS would bring the website down from overwhelming it with continuous requests.

![](/assets/legacy-images/its_not_that_hard.webp)

Another option would be to update the plugin with an option to email the website owner any time a backup is generated. This could be activated by default, but turned off in the settings if the website owner understood the risks and didn’t want the email(s) sent.

Having an email sent like this means as soon as an attacker triggers the backup the owner gets notified and can take appropriate actions.

## My Recommendations for users

If you’re using this plugin, my recommendation would be to stop immediately and find an alternative solution for backups.

Most reputable hosts like [WPEngine](https://wpengine.com), [Pagely](https://pagely.com), [Pressable](https://pressable.com) and others offer daily and on-demand backups. 

And beyond hosting companies, other solutions like [Blogvault](https://blogvault.com) also offer backups, so you have many other (better) options for backups than this plugin.

**Again just to make sure it’s clear: keeping the All In One WP Migration plugin active on your site does not immediately make you vulnerable to this type of attack.**

But depending on the rest of your website’s setup, you may just be playing with fire by keeping it active.

![](/assets/legacy-images/better_safe_than_sorry.webp)

## Related writing

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)

## Continue reading

**Newer:** [Improve CLS scores by dynamically setting image width and height](/improve-cls-scores-by-dynamically-setting-image-width-and-height/)

**Older:** [5 Python Scripts for OSINT and Pentesting](/5-python-scripts-for-osint-and-pentesting/)
