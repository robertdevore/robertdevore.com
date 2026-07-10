---
title: "Complete Beginner’s Guide: Building a Python URL Checker for Google Sheets"
description: "Don’t worry if you’ve never written Python before! This tutorial will explain every single line of code so you understand exactly what’s happening. Think of this like you’re building with LEGO blocks – we’ll add one…"
custom_url: "complete-beginners-guide-building-a-python-url-checker-for-google-sheets"
author: "Robert DeVore"
date: "2025-06-19"
canonical: "https://robertdevore.com/complete-beginners-guide-building-a-python-url-checker-for-google-sheets/"
template: "signal-c"
nav_hide: true
excerpt: "Don’t worry if you’ve never written Python before! This tutorial will explain every single line of code so you understand exactly what’s happening. Think of this like you’re building with LEGO blocks – we’ll add one…"
categories: ["Developer Tools"]
tags: ["Engineering"]
---

Don’t worry if you’ve never written Python before!

This tutorial will explain every single line of code so you understand exactly what’s happening.

Think of this like you’re building with LEGO blocks – we’ll add one piece at a time and explain what each piece does as we go.

## What We’re Building (In Simple Terms)

Imagine you have a huge list of website links in a Google Sheet, and you want to check if they’re all working.

Instead of clicking each one manually, we’re building a faux-bot (our Python script) that will:

  1. Read each website link from your Google Sheet
  2. Visit each website to see if it works
  3. Write the results back to your sheet (like “Working” or “Broken”)



## Before We Start: What You’ll Need

  * Python installed on your computer
  * A Google account
  * Basic text editor (like VS Code)

![Let's Go Baby! Jellyroll GIF](/assets/legacy-images/lets_go_baby.webp)

## Part 1: The Shopping List (Imports)

Just like cooking, we need to gather our ingredients first. 

In Python, these “ingredients” are called **libraries** – pre-written code that does specific jobs for us.

``` import gspread import requests import time import json from google.auth.transport.requests import Request from google.oauth2.service_account import Credentials ``` 

Let’s break this down line by line:

**Line 1:`import gspread`**

  * This is like hiring a translator who speaks “Google Sheets language”
  * It lets our Python script talk to Google Sheets



**Line 2:`import requests`**

  * This is our website visitor
  * It can go to any website and tell us if it’s working or broken



**Line 3:`import time`**

  * This is our timer/stopwatch
  * We’ll use it to pause between checking websites (so we don’t overwhelm them)



**Line 4:`import json`**

  * JSON is a way to store information in a file
  * Think of it like a digital notebook that both humans and computers can read



**Lines 5-6: The Google authentication imports**

  * These are like security guards that prove we’re allowed to access Google Sheets
  * They handle all the permission checking for us



## Part 2: Setting Up Our Configuration (The Settings)

``` # Config SPREADSHEET_NAME = "Redirections" SHEET_NAME = "Redirections" BATCH_SIZE = 100 PROGRESS_FILE = "progress.json" ``` 

In Python, lines starting with `#` are **comments** – they’re notes for humans and the computer ignores them.

**Line 2:`SPREADSHEET_NAME = "Redirections"`**

  * This tells our script which Google Sheet to open
  * Change “Redirections” to whatever your sheet is called
  * The quotes tell Python this is text (called a “string”)



**Line 3:`SHEET_NAME = "Redirections"`**

  * Google Sheets can have multiple tabs – this picks which tab to use
  * If your tab has a different name, change this



**Line 4:`BATCH_SIZE = 100`**

  * Instead of checking all URLs at once, we’ll do them in groups
  * 100 means “check 100 websites, then take a break”
  * This prevents Google from thinking we’re a spam robot



**Line 5:`PROGRESS_FILE = "progress.json"`**

  * This creates a digital bookmark
  * If our script stops halfway through, it remembers where it left off



## Part 3: Connecting to Google Sheets (The Handshake)

``` # Auth & connect to Google Sheet SCOPES = ["https://www.googleapis.com/auth/spreadsheets"] creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES) client = gspread.authorize(creds) sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME) ``` 

**Line 2:`SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]`**

  * This is like asking for a specific key to a specific room
  * We’re asking Google: “Please let us read and write spreadsheets”
  * The square brackets `[]` create a **list** – a container that holds multiple items



**Line 3:`creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)`**

  * This reads our secret key file (credentials.json)
  * It’s like showing your ID card to get into a building
  * `creds` is a **variable** – a box where we store information



**Line 4:`client = gspread.authorize(creds)`**

  * This uses our credentials to create a connection to Google Sheets
  * Think of `client` as our personal assistant who can talk to Google



**Line 5:`sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)`**

  * This opens our specific spreadsheet and sheet tab
  * Now `sheet` represents our actual Google Sheet that we can read and write to



## Part 4: Building Our Memory System (Progress Tracking)

### Function 1: Remembering Where We Left Off

``` def load_progress(): try: with open(PROGRESS_FILE, "r") as f: return json.load(f).get("startRow", 2) except FileNotFoundError: return 2 ``` 

**What’s a function?** Think of a function like a mini-robot that does one specific job. 

When you call its name, it does its job and gives you an answer.

**Line 1:`def load_progress():`**

  * `def` means “define a new function”
  * `load_progress` is the name we gave our function
  * The `()` is where we could give the function information, but this one doesn’t need any
  * The `:` tells Python “the function’s instructions start on the next line”



**Line 2:`try:`**

  * This means “try to do the following, but if something goes wrong, don’t crash”
  * It’s like saying “attempt this, but have a backup plan”



**Line 3:`with open(PROGRESS_FILE, "r") as f:`**

  * This opens our progress file for reading (the “r” means “read”)
  * `with` is polite – it automatically closes the file when we’re done
  * `as f` gives the opened file a nickname: `f`



**Line 4:`return json.load(f).get("startRow", 2)`**

  * `json.load(f)` reads the JSON file and turns it into Python data
  * `.get("startRow", 2)` looks for a value called “startRow”
  * If it finds it, it returns that number
  * If it doesn’t find it, it returns 2 (our default starting row)
  * `return` means “give this answer back to whoever called this function”



**Line 5:`except FileNotFoundError:`**

  * This is our backup plan if the progress file doesn’t exist
  * “If you can’t find the file, do this instead”



**Line 6:`return 2`**

  * If there’s no progress file, start from row 2
  * (Row 1 usually has column headers like “URL” and “Status”)



### Function 2: Saving Our Progress

``` def save_progress(row): with open(PROGRESS_FILE, "w") as f: json.dump({"startRow": row}, f) ``` 

**Line 1:`def save_progress(row):`**

  * This function takes one piece of information: `row`
  * `row` is the row number we want to remember



**Line 2:`with open(PROGRESS_FILE, "w") as f:`**

  * Opens our progress file for writing (the “w” means “write”)
  * This will create the file if it doesn’t exist, or replace it if it does



**Line 3:`json.dump({"startRow": row}, f)`**

  * `{"startRow": row}` creates a **dictionary** – like a mini-database with one entry
  * It stores the row number with the label “startRow”
  * `json.dump()` writes this information to the file in JSON format



## Part 5: The Website Checker (The Core Function)

``` def check_url_status(url): try: response = requests.get(url, timeout=5) if response.status_code == 404: return "404 Not Found" else: return f"Status Code: {response.status_code}" except Exception as e: return f"Error: {str(e)}" ``` 

This is our website visitor function. Let’s break it down:

**Line 1:`def check_url_status(url):`**

  * This function takes one input: a website URL
  * It will return a message about whether the website is working



**Line 2:`try:`**

  * Again, we’re being careful – “try this, but have a backup plan”



**Line 3:`response = requests.get(url, timeout=5)`**

  * `requests.get(url)` visits the website
  * `timeout=5` means “if the website doesn’t respond in 5 seconds, give up”
  * `response` stores the website’s answer



**Line 4:`if response.status_code == 404:`**

  * Every website gives back a status code (like a report card)
  * 404 means “page not found” – the website is broken
  * `if` means “only do the next thing IF this condition is true”
  * `==` means “is equal to” (different from `=` which means “assign”)



**Line 5:`return "404 Not Found"`**

  * If the website is broken, return this friendly message



**Line 6:`else:`**

  * “If the condition above wasn’t true, do this instead”



**Line 7:`return f"Status Code: {response.status_code}"`**

  * For working websites, return the status code
  * The `f` before the quotes creates an **f-string** – it lets us insert variables into text
  * `{response.status_code}` gets replaced with the actual number



**Line 8:`except Exception as e:`**

  * Our backup plan if anything goes wrong (network error, invalid URL, etc.)



**Line 9:`return f"Error: {str(e)}"`**

  * Return an error message with details about what went wrong
  * `str(e)` converts the error into readable text



## Part 6: The Main Brain (The check_urls Function)

This is our biggest function – it coordinates everything. 

Let’s break it into digestible pieces:

### Getting Started and Loading Data

``` def check_urls(): urls = sheet.col_values(1)[1:] start_row = load_progress() total_urls = len(urls) ``` 

**Line 1:`def check_urls():`**

  * Our main function that doesn’t need any input



**Line 2:`urls = sheet.col_values(1)[1:]`**

  * `sheet.col_values(1)` gets all values from column 1 (column A)
  * `[1:]` is **slicing** – it takes everything except the first item
  * This skips the header row and gives us just the URLs
  * Square brackets `[]` access specific parts of a list



**Line 3:`start_row = load_progress()`**

  * Calls our progress function to see which row to start from



**Line 4:`total_urls = len(urls)`**

  * `len()` counts how many URLs we have
  * `total_urls` stores this number for later



### Checking If We’re Done

``` if start_row > total_urls + 1: print("All URLs processed.") return ``` 

**Line 1:`if start_row > total_urls + 1:`**

  * If our starting row is past the end of our URLs, we’re done
  * `+1` accounts for the header row



**Line 2:`print("All URLs processed.")`**

  * `print()` displays a message on the screen
  * Like the script talking to us



**Line 3:`return`**

  * Exit the function early – we’re done!



### Calculating Our Batch

``` end_row = min(start_row + BATCH_SIZE - 1, total_urls + 1) print(f"Processing rows {start_row} to {end_row}...") updates = [] ``` 

**Line 1:`end_row = min(start_row + BATCH_SIZE - 1, total_urls + 1)`**

  * `min()` picks the smaller of two numbers
  * We want to process either our full batch size OR up to the last URL
  * This prevents us from trying to process URLs that don’t exist



**Line 2:`print(f"Processing rows {start_row} to {end_row}...")`**

  * Tell the user what we’re doing
  * The `f` string inserts our row numbers into the message



**Line 3:`updates = []`**

  * Create an empty list to store our results
  * `[]` creates an empty list



### Processing Each URL

``` for i in range(start_row - 2, end_row - 1): url = urls[i] result = check_url_status(url) updates.append([result]) ``` 

**Line 1:`for i in range(start_row - 2, end_row - 1):`**

  * A **for loop** – repeat the following code for each number in a range
  * `range()` creates a sequence of numbers
  * The math adjusts for the difference between row numbers and list positions
  * `i` is our counter variable



**Line 2:`url = urls[i]`**

  * Get the URL at position `i` from our list



**Line 3:`result = check_url_status(url)`**

  * Call our URL checker function and store the result



**Line 4:`updates.append([result])`**

  * Add the result to our updates list
  * `[result]` puts the result in its own list (required by Google Sheets)
  * `append()` adds an item to the end of a list



### Saving Results and Planning Next Steps

``` sheet.update(f"B{start_row}:B{end_row}", updates) save_progress(end_row + 1) if end_row < total_urls + 1: print("Sleeping before next batch...") time.sleep(3) check_urls() else: print("Processing complete.") save_progress(2) ``` 

**Line 1:`sheet.update(f"B{start_row}:B{end_row}", updates)`**

  * Write all our results to column B in Google Sheets
  * `f"B{start_row}:B{end_row}"` creates a range like “B2:B101”
  * This is much faster than writing one cell at a time



**Line 2:`save_progress(end_row + 1)`**

  * Save where we should start next time



**Line 3:`if end_row < total_urls + 1:`**

  * Check if there are more URLs to process



**Line 4:`print("Sleeping before next batch...")`**

  * Tell the user we’re taking a break



**Line 5:`time.sleep(3)`**

  * Pause for 3 seconds
  * This prevents us from overwhelming Google’s servers



**Line 6:`check_urls()`**

  * Call ourselves again to process the next batch
  * This is called **recursion** – a function calling itself



**Line 7:`else:`**

  * If we’ve processed all URLs…



**Line 8:`print("Processing complete.")`**

  * Celebrate! We’re done!



**Line 9:`save_progress(2)`**

  * Reset our progress for the next time we run the script



## Part 7: Starting the Engine

``` # Run it check_urls() ``` 

This final line actually starts our script. 

Without this, we’d have defined all our functions but never used them.

## The Complete Script (With Comments)

Here’s everything together with helpful comments:

``` # Import our tools import gspread # Google Sheets connector import requests # Website visitor import time # Timer for pauses import json # File format handler from google.auth.transport.requests import Request # Google authentication from google.oauth2.service_account import Credentials # Google credentials # Settings - change these to match your needs SPREADSHEET_NAME = "Redirections" # Your Google Sheet name SHEET_NAME = "Redirections" # Your sheet tab name BATCH_SIZE = 100 # How many URLs to check at once PROGRESS_FILE = "progress.json" # Where to save our progress # Connect to Google Sheets SCOPES = ["https://www.googleapis.com/auth/spreadsheets"] # Permission we need creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES) client = gspread.authorize(creds) # Create connection sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME) # Open our sheet def load_progress(): """Remember where we left off""" try: with open(PROGRESS_FILE, "r") as f: return json.load(f).get("startRow", 2) except FileNotFoundError: return 2 # Start from row 2 if no progress file def save_progress(row): """Save our current position""" with open(PROGRESS_FILE, "w") as f: json.dump({"startRow": row}, f) def check_url_status(url): """Visit a website and check if it's working""" try: response = requests.get(url, timeout=5) if response.status_code == 404: return "404 Not Found" else: return f"Status Code: {response.status_code}" except Exception as e: return f"Error: {str(e)}" def check_urls(): """Main function - coordinates everything""" # Get all URLs from column A (skip header) urls = sheet.col_values(1)[1:] start_row = load_progress() total_urls = len(urls) # Check if we're already done if start_row > total_urls + 1: print("All URLs processed.") return # Figure out which batch to process end_row = min(start_row + BATCH_SIZE - 1, total_urls + 1) print(f"Processing rows {start_row} to {end_row}...") updates = [] # Store our results here # Check each URL in this batch for i in range(start_row - 2, end_row - 1): url = urls[i] result = check_url_status(url) updates.append([result]) # Write results to Google Sheets sheet.update(f"B{start_row}:B{end_row}", updates) save_progress(end_row + 1) # Check if we need to do more batches if end_row < total_urls + 1: print("Sleeping before next batch...") time.sleep(3) # Be polite to Google's servers check_urls() # Process next batch else: print("Processing complete.") save_progress(2) # Reset for next run # Start the script! check_urls() ``` 

## How to Use This Script

  1. **Set up your Google Sheet** with URLs in column A (starting from A2, with A1 as your header)
  2. **Get your credentials file** from Google Cloud Console and save it as `credentials.json`
  3. **Update the configuration** at the top to match your sheet names
  4. **Run the script** and watch it work!



## What You’ve Learned

Congratulations! You’ve just learned about:

  * **Variables** (storing information)
  * **Functions** (reusable pieces of code)
  * **Lists** (containers for multiple items)
  * **Loops** (repeating actions)
  * **Conditionals** (making decisions)
  * **Error handling** (dealing with problems gracefully)
  * **File operations** (reading and writing files)
  * **API interactions** (talking to other services)



You’re now ready to start modifying this script for your own needs!

If you’re looking to learn more about [programming with Python](https://python.robertdevore.com), I put out a course for that 💪

## Related Reading

- [Zero Cool CLI – A Hacker’s Terminal from 1995](/zero-cool-cli-a-hackers-terminal-from-1995/)
- [I Built a Python Stego-Cipher Tool (And You Can Have It)](/i-built-a-python-stego-cipher-tool-and-you-can-have-it/)
- [Extreme Programming for Extreme Leaders](/extreme-programming-for-extreme-leaders/)
