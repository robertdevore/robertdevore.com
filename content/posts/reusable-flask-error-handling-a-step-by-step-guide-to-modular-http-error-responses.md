---
title: "Reusable Flask Error Handling: A Step-by-Step Guide to Modular HTTP Error Responses"
description: "I don’t know about you, but in code and in real life, I hate repeating myself 🤦‍♂️ And after building the Savage Scanner and Vuln Search apps, I realized quickly that I’ll be creating a lot of the same code for my Flask…"
custom_url: "reusable-flask-error-handling-a-step-by-step-guide-to-modular-http-error-responses"
author: "Robert DeVore"
date: "2025-01-02"
canonical: "https://robertdevore.com/reusable-flask-error-handling-a-step-by-step-guide-to-modular-http-error-responses/"
template: "signal-c"
nav_hide: true
excerpt: "I don’t know about you, but in code and in real life, I hate repeating myself 🤦‍♂️ And after building the Savage Scanner and Vuln Search apps, I realized quickly that I’ll be creating a lot of the same code for my Flask…"
categories: ["Developer Tools"]
tags: ["Engineering"]
---

I don’t know about you, but in code and in real life, I hate repeating myself 🤦‍♂️

And after building the [Savage Scanner](https://savage.robertdevore.com) and [Vuln Search](https://vuln.robertdevore.com) apps, I realized quickly that I’ll be creating a _lot_ of the same code for my Flask projects.

And since error handling is a key feature for creating a user-friendly and professional web application, I figured now was the perfect time to create a modular solution for it.

This how-to guide walks you through creating a reusable `errors.py` module using Flask’s `Blueprint` for handling common HTTP errors with both JSON and HTML responses.

## **Step 1: Set Up the`errors.py` Module**

This module creates a `Blueprint` for handling errors, ensuring your error-handling logic is reusable and easy to maintain.

### **Code for`errors.py`**

``` from flask import Blueprint, render_template, jsonify, request # Create a blueprint for error handling errors_blueprint = Blueprint('errors', __name__) # Utility function to determine if the request is for JSON def is_json_request(): return request.accept_mimetypes['application/json'] > request.accept_mimetypes['text/html'] # 404 Error Handler @errors_blueprint.app_errorhandler(404) def page_not_found(e): if is_json_request(): return jsonify({"error": "Resource not found", "code": 404}), 404 return render_template('errors/404.html', error=e), 404 # 500 Error Handler @errors_blueprint.app_errorhandler(500) def internal_server_error(e): if is_json_request(): return jsonify({"error": "Internal server error", "code": 500}), 500 return render_template('errors/500.html', error=e), 500 # 403 Error Handler @errors_blueprint.app_errorhandler(403) def forbidden(e): if is_json_request(): return jsonify({"error": "Forbidden", "code": 403}), 403 return render_template('errors/403.html', error=e), 403 # 400 Error Handler @errors_blueprint.app_errorhandler(400) def bad_request(e): if is_json_request(): return jsonify({"error": "Bad request", "code": 400}), 400 return render_template('errors/400.html', error=e), 400 # Generic Error Handler for other HTTP status codes @errors_blueprint.app_errorhandler(Exception) def handle_generic_error(e): code = getattr(e, 'code', 500) # Default to 500 if no specific code if is_json_request(): return jsonify({"error": "An unexpected error occurred", "code": code}), code return render_template('errors/generic.html', error=e, code=code), code # Initialization function for the blueprint def init_error_handlers(app): app.register_blueprint(errors_blueprint) ``` 

## **Step 2: Integrate the`errors.py` Module**

Add the `init_error_handlers` function to your Flask app to automatically register error handlers.

### **Code for`app.py`**

``` from flask import Flask, render_template from errors import init_error_handlers def create_app(): """Create and configure the Flask app.""" app = Flask(__name__) # Initialize error handlers init_error_handlers(app) # Example route @app.route('/') def index(): return render_template('index.html') # Simulate errors for testing @app.route('/trigger-404') def trigger_404(): return render_template('nonexistent.html') # This triggers a 404 error @app.route('/trigger-500') def trigger_500(): raise Exception("Simulated internal server error") # This triggers a 500 error return app app = create_app() if __name__ == '__main__': app.run(debug=True) ``` 

## **Step 3: Create Error Templates**

Design templates for each error to provide clear and consistent feedback to users. Here’s an example for a `404` error:

### **HTML Template for`404.html`**

``` <!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>404 - Page Not Found</title> <script src="https://cdn.tailwindcss.com"></script> </head> <body class="bg-gray-100 min-h-screen flex flex-col items-center justify-center p-6"> <h1 class="text-4xl font-bold text-gray-800 mb-4">404</h1> <p class="text-lg text-gray-600 mb-6">The page you are looking for does not exist.</p> <a href="/" class="text-blue-500 hover:text-blue-700">Go back to the home page</a> </body> </html> ``` 

### **Other Templates**

Create similar templates for `403.html`, `500.html`, `400.html`, and a generic error template (`generic.html`). Customize messages and styles as needed.

## **Step 4: Testing the Error Handlers**

To verify that the error handlers are working as intended, trigger specific errors in your application:

  1. **404 Error:** Visit a non-existent route, e.g., `/nonexistent-route`.
  2. **500 Error:** Visit `/trigger-500`.
  3. **403 Error:** Add this route to simulate forbidden access:

``` from flask import abort @app.route('/trigger-403') def trigger_403(): abort(403) ``` 

Visit `/trigger-403`.

**400 Error:** Add this route to simulate a bad request:


``` @app.route('/trigger-400') def trigger_400(): abort(400) ``` 

Visit `/trigger-400`.

## **Step 5: Advanced Enhancements**

  * **Logging Errors:** Use Flask’s `logging` module to log errors to a file or an external monitoring service.
  * **Localization:** Localize error templates for multilingual support.
  * **Custom Error Pages by Environment:** Serve detailed error pages in development and generic pages in production.



## **Wrapping up**

By using a dedicated `errors.py` module and clean error templates, we’ve created a reusable error-handling system for our Flask applications.

This approach ensures consistency and user-friendliness across projects, not to mention a lot less copy/pasting 😎

Like this article? Share this setup to help others improve their Flask apps!

## Related Reading

- [Zero Cool CLI – A Hacker’s Terminal from 1995](/zero-cool-cli-a-hackers-terminal-from-1995/)
- [Complete Beginner’s Guide: Building a Python URL Checker for Google Sheets](/complete-beginners-guide-building-a-python-url-checker-for-google-sheets/)
- [I Built a Python Stego-Cipher Tool (And You Can Have It)](/i-built-a-python-stego-cipher-tool-and-you-can-have-it/)
