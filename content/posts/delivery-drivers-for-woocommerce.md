---
title: "Delivery Drivers for WooCommerce"
description: "Today I am happy to announce the release of my newest open source plugin, Delivery Drivers for WooCommerce . As you can probably guess by the name, it's a plugin for WooCommerce that adds functionality for businesses…"
custom_url: "delivery-drivers-for-woocommerce"
author: "Robert DeVore"
date: "2018-09-14"
canonical: "https://robertdevore.com/delivery-drivers-for-woocommerce/"
template: "signal-b"
nav_hide: true
excerpt: "Today I am happy to announce the release of my newest open source plugin, Delivery Drivers for WooCommerce . As you can probably guess by the name, it's a plugin for WooCommerce that adds functionality for businesses…"
categories: ["WordPress Archive"]
tags: ["WordPress", "WooCommerce"]
---

Today I am happy to announce the release of my newest open source plugin, [Delivery Drivers for WooCommerce](https://www.wordpress.org/plugins/delivery-drivers-for-woocommerce). ![Delivery Drivers for WooCommerce logo](/assets/legacy-images/ddwc_logo.webp) As you can probably guess by the name, it's a plugin for WooCommerce that adds functionality for businesses who offer delivery and would like greater control over the entire process. Part of the reason that I built this plugin is because of a client need via [WP Dispensary](https://www.wpdispensary.com), but I did not want to pigeonhole it as another [dispensary plugin](https://www.wordpress.org/plugins/wp-dispensary). Since there's many businesses that offer delivery beyond just the cannabis industry, I knew this plugin would be better built as it's own separate entity. And that's what this blog post is about - the release of the Delivery Drivers for WooCommerce plugin, and what you can expect when using it.

## Delivery Businesses & WooCommerce

We've all seen the rise of grocery delivery services - the tides are changing, and where we used to enjoy trips across town, consumers are now looking for ways to have things brought to us. And that's where delivery businesses in the food industry (hello, Pizza) come into play. Studies indicate that [10% of consumers](https://www.statista.com/topics/1986/food-delivery-industry-in-the-us/) use food delivery services at least once a week, and that's just one service business that offers delivery. Restaurant and grocery stores not only offer delivery for their customers, but place orders and have items delivered to them on a weekly basis, too. So this same plugin can power the restaurant's online delivery management, and also power the restaurant's food vendors who deliver truck loads of fresh produce every week. And while upwards of $4B dollars was spent ordering food delivery in 2015, we cannot overlook the multi-billion dollar cannabis industry that offer delivery services and need an easy way to manage drivers and track orders. With industries this large, there's no reason for WooCommerce to not have a delivery driver system for businesses who need them. Since I couldn't find anything remotely useful available, I decided to build it myself.

## How the plugin works

Now that we've covered some of the reasons behind building the plugin and the markets that it serves, let's jump into how it actually works!

### Delivery Drivers WooCommerce Settings

First things first, once you've installed & activated the plugin, you're going to want to head over to the Settings page. You can find the Delivery Drivers settings by going to `WooCommerce -> Settings -> Delivery Drivers`. ![Delivery Drivers for WooCommerce Settings screenshot](/assets/legacy-images/ddwc_screenshot_1.webp) The settings page allows you to add your Google Maps API key which is required in order for the map to display on your driver's dashboard. You can also add your dispatch phone number, which then adds a contact button on the order page in your drivers dashboard. Adding this contact info lets your drivers easily connect to your dispatch center with any questions they have about the order.

### Assigning a driver to each order

Once you've taken care of the settings page, it's time to start assigning a driver to your order. In your dashboard, go to `WooCommerce -> Orders` and then edit any of your orders, which will bring up a screen like the image below. ![Delivery Drivers for WooCommerce - Assign Driver to Order](/assets/legacy-images/ddwc_screenshot_5_1024x318.webp)click to enlarge In the **Delivery Driver** box on the right side of the screen, you'll see a list of every user in your website with the Driver role that you can choose from. Then, on the left side of the screen where the **Status:** is currently `Processing`, you can change the status to `Driver Assigned`.

## Drivers Capabilities

Now that we've covered how the administrator of the website can work with the Delivery Drivers for WooCommerce plugin, let's see what capabilities are given to your drivers.

### Views from the Driver dashboard

On the front end of your website, the plugin adds a new "Delivery Drivers" tab to the WooCommerce My Account page, as seen below. ![Assigned Orders - Driver Dashboard - Delivery Drivers for WooCommerce](/assets/legacy-images/ddwc_screenshot_3.webp) When the driver clicks to view the Delivery Drivers page, they are given a table view of each order that's been assigned to them. These details include the order ID number, the date of the order, it's current status and the total cost for the order. The order ID links to a separate page for your driver to further manage the order.

### Order status management by your drivers

Once your driver clicks the ID number they'd like to view order details for, they are shown a page with basic order details, a list of items in the order, the delivery address and Google map of the location, plus order status management.

### Order Status management

Under the map is where your driver can change the order status. The default option is to change the order status from `Driver Assigned` to `Out for Delivery`. Once they've clicked the button to mark the order as `Out for Delivery`, the status option changes to allow the driver to mark the order as `Complete` after they've made the delivery. The goal is to give your driver the ability to manage the order status themselves and free up your time to spend it elsewhere on the business - or hell, maybe even take some time off ?

## Delivery Drivers for WooCommerce PRO

I'm happy to announce that you can get the Pro version of the Delivery Drivers for WooCommerce plugin from [Devio Digital](https://www.deviodigital.com/). The Pro features include:

  * Auto-assign drivers when an order is submitted
  * Accept driver applications from the Driver Dashboard
  * Email driver when they've been assigned a new order
  * Email customer when the driver marks an order as "Out for Delivery"
  * Email administrator when the driver marks an order as "Completed"



[View DDWC Pro →](https://deviodigital.com/product/delivery-drivers-for-woocommerce-pro/) ![](/assets/legacy-images/banner_772x250.webp)

## Download the Delivery Drivers for WooCommerce Plugin

You can download the [Delivery Drivers for WooCommerce](https://www.wordpress.org/plugins/delivery-drivers-for-woocommerce) plugin from the official WordPress plugin directory, or by searching for "**Delivery Drivers** " in the WordPress dashboard under `Plugins -> Add New`.

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
