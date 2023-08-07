# __________                  __             __     ________             .___ 
# \______   \  ____    ____  |  | __  ____ _/  |_  /  _____/   ____    __| _/ 
#  |       _/ /  _ \ _/ ___\ |  |/ /_/ __ \\   __\/   \  ___  /  _ \  / __ |  
#  |    |   \(  <_> )\  \___ |    < \  ___/ |  |  \    \_\  \(  <_> )/ /_/ |  
#  |____|_  / \____/  \___  >|__|_ \ \___  >|__|   \______  / \____/ \____ |  
#         \/              \/      \/     \/               \/              \/  
#
# HTML Squasher by RocketGod
# Evil Portal html squashing tool. 
# The Flipper Zero WiFi Dev Board's Evil Portal only allows 20KB single file html for the actual portals. 
# This script is intended to take your output from the "SingleFile" Chrome extension and compress it as much as possible.
# All uninstalled packages we need will automatically install if needed.
# If the output is still too large of a file, you'll need to start deleting elements like footers, or embedded SVG images, etc. using a tool like Chrome Developer Console and then run this script again.
# Evil Portal can be found at https://github.com/bigbrodude6119/flipper-zero-evil-portal - big thanks for all the work there.
#
# https://github.com/RocketGod-git/evilportal-htmlsquash

"""
This script is designed to reduce the file size of single file HTML pages that have embedded CSS, fonts, and images. 
It does this by removing unused CSS classes and ids from the HTML and CSS, replacing base64 encoded fonts with client-side standard fonts, removing empty `div` tags, and minifying the HTML. 
The script reads an HTML file, parses it using BeautifulSoup, performs the optimizations, and then writes the optimized and minified HTML to new files. 
The script also calculates the initial, final, and minified file sizes to show how much the file size has been reduced. 
At the end of the script, it displays a final printout to the user with the original, stripped, and minified file sizes and provides instructions on the location of the output files.
"""

import os
import sys
import subprocess

# Check if required packages are installed
required_packages = ["bs4", "cssutils", "htmlmin"]
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print(f"The following packages are missing: {', '.join(missing_packages)}")
    print("Attempting to install missing packages using pip...")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
        print("Successfully installed missing packages")
    except Exception as e:
        print(f"Error installing missing packages: {e}")
        print(f"Please install the missing packages manually using the following command:")
        print(f"{sys.executable} -m pip install {' '.join(missing_packages)}")
        sys.exit(1)

from bs4 import BeautifulSoup
import cssutils
import re
from htmlmin import minify
import logging

cssutils.log.setLevel(logging.CRITICAL)

STANDARD_FONTS = [
    "Arial, sans-serif",
    "Verdana, sans-serif",
    "Georgia, serif",
    "Helvetica, sans-serif",
    "Open Sans, sans-serif",
    "Roboto, sans-serif",
    "Lato, sans-serif",
    "Source Sans Pro, sans-serif",
    "PT Sans, sans-serif"
]

def read_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(f"Successfully opened file {file_path}")
            content = file.read()
            print(f"Successfully read file {file_path}")
            return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def write_html(file_path, html):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # create directory if it does not exist
        with open(file_path, 'w', encoding='utf-8') as file:
            print(f"Successfully opened file {file_path} for writing")
            file.write(html)
            print(f"Successfully wrote to file {file_path}")
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")

def parse_html(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        print("Successfully parsed HTML")
        return soup
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None

def change_form_method(soup):
    try:
        forms = soup.find_all('form', method='POST')
        for form in forms:
            form['method'] = 'GET'
        print("Successfully changed form methods from POST to GET")
    except Exception as e:
        print(f"Error changing form methods: {e}")

def get_html_classes_ids(soup):
    try:
        html_classes_ids = set()
        for tag in soup.find_all(True):
            if 'class' in tag.attrs:
                html_classes_ids.update(tag['class'])
            if 'id' in tag.attrs:
                html_classes_ids.add(tag['id'])
        print("Successfully extracted classes and ids from HTML")
        return html_classes_ids
    except Exception as e:
        print(f"Error extracting classes and ids from HTML: {e}")
        return set()

def get_css_classes_ids(css):
    try:
        css_classes_ids = set()
        for rule in css:
            if rule.type == rule.STYLE_RULE:
                for selector in rule.selectorList:
                    css_classes_ids.update(re.findall(r'\.(\w+)|#(\w+)', selector.selectorText))
        print("Successfully extracted classes and ids from CSS")
        return css_classes_ids
    except Exception as e:
        print(f"Error extracting classes and ids from CSS: {e}")
        return set()

def remove_unused_css(soup, html_classes_ids, css):
    try:
        for rule in css:
            if rule.type == rule.STYLE_RULE:
                selectors = rule.selectorList
                for selector in selectors:
                    classes_ids = set(re.findall(r'\.(\w+)|#(\w+)', selector.selectorText))
                    if not classes_ids.intersection(html_classes_ids):
                        css.deleteRule(rule)
        style_tag = soup.find('style')
        style_tag.string.replace_with(css.cssText.decode('utf-8'))  # convert bytes to string
        print("Successfully removed unused CSS")
        return soup
    except Exception as e:
        print(f"Error removing unused CSS: {e}")
        return soup

def replace_base64_data(soup):
    try:
        # Replace base64 fonts
        for style in soup.find_all('style'):
            style.string = re.sub(r'@font-face\s*{[^}]*}', '', style.string)  # Remove @font-face rules with base64 data
            for font in STANDARD_FONTS:
                style.string = re.sub(r'font-family:[^;]*;', f'font-family: {font};', style.string)

        # Remove base64 icons
        for tag in soup.find_all(['img', 'link'], {'src': True}):
            if 'base64' in tag['src']:
                tag.decompose()

        for tag in soup.find_all('link', {'href': True}):
            if 'base64' in tag['href']:
                tag.decompose()

        # Remove base64 background images in CSS
        for style in soup.find_all('style'):
            style.string = re.sub(r'url\(data:image[^)]*\)', '', style.string, flags=re.DOTALL)

        print("Successfully replaced base64 data")
    except Exception as e:
        print(f"Error replacing base64 data: {e}")

def remove_empty_divs(soup):
    try:
        divs = soup.find_all('div')
        for div in divs:
            if not div.text.strip() and not div.contents:
                div.decompose()
        
        print("Successfully removed empty divs")
    except Exception as e:
        print(f"Error removing empty divs: {e}")

def get_file_size(file_path):
    try:
        size = os.path.getsize(file_path)
        print(f"Successfully got file size of {file_path}")
        return size
    except Exception as e:
        print(f"Error getting file size of {file_path}: {e}")
        return 0

# Main script

if len(sys.argv) < 2:
    print("Please provide the file name as a command line argument.")
    sys.exit(1)

file_path = sys.argv[1]
output_dir = "./evilportals/"
output_path = os.path.join(output_dir, os.path.basename(file_path))
minified_output_path = os.path.join(output_dir, f"minified_{os.path.basename(file_path)}")

print("Reading HTML file...")
html = read_html(file_path)

if html is not None:
    initial_file_size = get_file_size(file_path)
    print(f"Initial file size: {initial_file_size} bytes")

    print("Parsing HTML...")
    soup = parse_html(html)
    change_form_method(soup)

    if soup is not None:
        print("Replacing base64 data...")
        replace_base64_data(soup)

        print("Extracting classes and ids from HTML...")
        html_classes_ids = get_html_classes_ids(soup)

        print("Extracting CSS...")
        style_tag = soup.find('style')
        css = cssutils.parseString(style_tag.string)

        print("Extracting classes and ids from CSS...")
        css_classes_ids = get_css_classes_ids(css)

        print("Removing unused CSS...")
        soup = remove_unused_css(soup, html_classes_ids, css)

        print("Removing empty divs...")
        remove_empty_divs(soup)

        print("Writing optimized HTML...")
        write_html(output_path, str(soup))

        final_file_size = get_file_size(output_path)
        print(f"Final file size: {final_file_size} bytes")
        print(f"Optimized HTML saved to: {output_path}")

        print("Minifying HTML...")
        minified_html = minify(str(soup))
        
        print("Writing minified HTML...")
        write_html(minified_output_path, minified_html)
        
        minified_file_size = get_file_size(minified_output_path)
        print(f"Minified file size: {minified_file_size} bytes")
        print(f"Minified HTML saved to: {minified_output_path}")

        # Final printout to the user
        print("\nFinal results:")
        print(f"Original file size: {initial_file_size} bytes")
        print(f"Stripped file size: {final_file_size} bytes")
        print(f"Minified file size: {minified_file_size} bytes")
        
        if minified_file_size > 20000:
            print("\nWarning: The minified file size is above 20KB. Evil Portal requires 20KB or less. You should use the Chrome Developer Console to remove useless elements from the original HTML saved by the SingleFile Chrome extension. Then run this script again.")
        
    else:
        print("Aborting due to HTML parsing error.")
else:
    print("Aborting due to file read error.")
