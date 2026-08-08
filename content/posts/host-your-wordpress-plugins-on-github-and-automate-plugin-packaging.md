---
title: "Host Your WordPress Plugins on GitHub and Automate Plugin Packaging"
description: "Let’s talk plugin distribution. Hosting your plugins on GitHub provides powerful benefits such as version control, collaboration, and easy sharing. But distributing your plugin as a proper .zip file for users can be…"
custom_url: "host-your-wordpress-plugins-on-github-and-automate-plugin-packaging"
author: "Robert DeVore"
date: "2024-12-21"
canonical: "https://robertdevore.com/host-your-wordpress-plugins-on-github-and-automate-plugin-packaging/"
template: "signal-a"
nav_hide: true
excerpt: "Let’s talk plugin distribution. Hosting your plugins on GitHub provides powerful benefits such as version control, collaboration, and easy sharing. But distributing your plugin as a proper .zip file for users can be…"
categories: ["WordPress Archive"]
tags: ["WordPress"]
---

Let’s talk plugin distribution.

Hosting your plugins on GitHub provides powerful benefits such as version control, collaboration, and easy sharing.

But distributing your plugin as a proper `.zip` file for users can be tedious, especially when you need to exclude unnecessary files like `.git` folders, `node_modules`, and `.DS_Store`.

This guide walks you through:

  1. Hosting your WordPress plugins on GitHub.
  2. Automating the creation of `.zip` files, saving them one level up in the main `plugins` folder.

![Let's do this - GIF](/assets/legacy-images/lets_do_this.webp)

## **Step 1: Host Your Plugin on GitHub**

### 1.1. Create a New Repository

Log in to your GitHub account and create a new repository:

  * Go to [github.com/new](https://github.com/new).
  * Name your repository (e.g., `my-awesome-plugin`).
  * Optionally add a description.
  * Set it to **Public** if you want to share the plugin or **Private** for internal use.



Initialize the repository with:

  * A `README.md` file to describe your plugin.
  * A `.gitignore` file (select “WordPress” from the GitHub template list).




### 1.2. Push Your Plugin Code to GitHub

If your plugin already exists locally:

Open your terminal and navigate to your plugin folder:

`cd /path/to/your/plugin`

Initialize Git and link it to your GitHub repository: 

`git init git remote add origin https://github.com/your-username/my-awesome-plugin.git`

Add and commit your plugin files:

`git add . git commit -m "Initial commit"`

Push your code to GitHub:

`git branch -M main git push -u origin main`




### 1.3. Create a GitHub Release for Easy Downloads

GitHub automatically generates source code downloads for your repository, but these include the `.git` folder and may add a `-main` suffix to your plugin folder, which can break WordPress installation. To avoid this:

  1. Go to the **“Releases”** section of your GitHub repository.
  2. Click **“Draft a new release”**.
  3. Add a version tag (e.g., `v1.0.0`), title, and description.
  4. Upload your plugin `.zip` file (see the next section for how to create it).
  5. Publish the release.



Your `.zip` file will now be available for download, and GitHub will track the number of downloads.

![I'll show you automated - GIF - spongebob squarepants](/assets/legacy-images/ill_show_you_automated.webp)

## **Step 2: Automate Plugin Packaging with a Bash Script**

Manually zipping your plugin every time you update it can be time-consuming. This script simplifies the process and saves the `.zip` file in the parent `plugins` folder for better organization.

### 2.1. Create the Bash Script

Open your terminal and create a new bash script:

`nano ~/zipplugin.sh`

Add the following script to the file:

``` #!/bin/bash # Get the plugin folder name from the current directory (default) default_plugin_name=$(basename "$PWD") # Use the first argument as the plugin name, or default to the current folder name plugin_name="${1:-$default_plugin_name}" # Define the parent directory path parent_dir=$(dirname "$PWD") # Define the zip name and location (one folder up) zip_name="$parent_dir/${plugin_name}.zip" # Define default exclusions exclude="${2:-"*.git/* *.gitignore *.DS_Store node_modules/*"}" echo "Creating zip: $zip_name" echo "Excluding: $exclude" # Create the zip file in the parent directory zip -r "$zip_name" . -x $exclude ``` 

Save and close the file by pressing `CTRL+O`, then `CTRL+X`.

Make the script executable:

`chmod +x ~/zipplugin.sh`

### 2.2. Add an Alias for Convenience

To make the script easier to use, add an alias to your shell configuration file.

Open your shell configuration file (`~/.bashrc` or `~/.zshrc`):

`nano ~/.bashrc`

Add the following alias: 

`alias zipplugin="~/zipplugin.sh"`

Save and reload your shell:

`source ~/.bashrc`




### 2.3. Use the Script

Navigate to your plugin directory:

`cd /path/to/plugins/my-plugin`

Run the script to create a `.zip` file with the default folder name and exclusions:

`zipplugin`

The `.zip` file will be saved in the parent `plugins` directory:

`/path/to/plugins/my-plugin.zip`

Optionally specify a custom plugin name:

`zipplugin custom-plugin-name`

Customize the exclusions by adding a second argument:

`zipplugin custom-plugin-name "*.env/* *test*"`

![SEND IT - GIF](/assets/legacy-images/send_it.webp)

## **Step 3: Share Your Plugin**

Now that your `.zip` file is ready, upload it to your GitHub release 💪💯

This makes sure that users can download and install your plugin without encountering issues like unnecessary files or incorrectly named folders.

  1. Go to your GitHub repository.
  2. Navigate to the **“Releases”** section.
  3. Upload your `.zip` file to the release.

## Related Reading

- [Stattic v1.0: The World’s Fastest Python-based Static Site Generator](/stattic-v1-0-the-worlds-fastest-python-based-static-site-generator/)
- [Grateful to See 20 of My WordPress Plugins Live On at WebDevStudios](/grateful-to-see-21-of-my-wordpress-plugins-live-on-at-webdevstudios/)
- [The Fastest Way for PHP Devs to Learn Python](/the-fastest-way-for-php-devs-to-learn-python/)
