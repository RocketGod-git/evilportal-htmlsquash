# Evil Portal - HTML Squasher by RocketGod

HTML Squasher is an Evil Portal HTML squashing tool for the Flipper Zero WiFi Dev Board. The Evil Portal only allows 20KB single file HTML for the actual portals, and this script is intended to take your output from the "SingleFile" Chrome extension and compress it as much as possible. Any packages we need will automatically install if needed.

If the output file is still too large, you'll need to start deleting elements like footers, embedded SVG images, etc., using a tool like the Chrome Developer Console and then run this script again.

Big thanks to [Evil Portal](https://github.com/bigbrodude6119/flipper-zero-evil-portal) for all their work. Bigbrodude6119 provides amazing instructions [here](LINK_TO_THE_INSTRUCTIONS).

## How it works

HTML Squasher operates in multiple steps to optimize and reduce the size of your HTML file:

1. **Checking Required Packages:** Verifies if required Python packages (bs4, cssutils, htmlmin) are installed, and installs any missing ones automatically.
2. **Reading the HTML File:** Opens and reads the input HTML file.
3. **HTML Parsing:** Utilizes BeautifulSoup to parse the HTML content.
4. **Changing Form Methods:** Converts all POST methods in forms to GET and modifies the form action to "/get".
5. **Removing Base64 Data:** Replaces base64 encoded fonts with standard client-side fonts, and removes base64 icons and background images.
6. **Extracting Classes and IDs:** Retrieves all the classes and IDs from the HTML.
7. **Optimizing CSS:** Removes unused CSS rules by cross-referencing the HTML classes/IDs with CSS classes/IDs.
8. **Cleaning up the HTML:** Removes empty div elements from the HTML.
9. **Writing Optimized HTML:** Outputs the optimized HTML to a new file.
10. **HTML Minification:** Minifies the optimized HTML for further size reduction.
11. **Final Report:** Displays the original, optimized, and minified file sizes to the user.

The end goal is to ensure the final minified file size is below the 20KB limit imposed by Evil Portal.

## Installation

To install HTML Squasher from GitHub, follow these steps:

1. Clone the repository: `git clone https://github.com/RocketGod-git/evilportal-htmlsquash`
2. Navigate to the cloned repository: `cd evilportal-htmlsquash`
3. The required packages will be installed automatically on the first run.

## Usage

To use HTML Squasher on single file HTML portals captured with the SingleFile extension for Chrome Browser, follow these steps:

1. Download the SingleFile Chrome extension.
2. Navigate to the login portal for your target website.
3. Make sure there are no popups on the screen or these will save too.
4. For some portals, you may need to enter placeholder text in the username and password fields to ensure the submit button is saved in a working state.
5. If that was the case, use a unique placeholder like "evilportal" so you can easily find and replace it with an empty string ("") later.
6. Then just run `python htmlsquash.py <filename>`

Note: Don't be a dick. Please use these portals responsibly and not in real-world situations. This is intended for educational purposes only and DEFCON shenanigans.