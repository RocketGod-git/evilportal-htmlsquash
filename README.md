# Evil Portal - HTML Squasher by RocketGod

HTML Squasher is an Evil Portal HTML squashing tool for the Flipper Zero WiFi Dev Board. The Evil Portal only allows 20KB single file HTML for the actual portals, and this script is intended to take your output from the "SingleFile" Chrome extension and compress it as much as possible. Any packages we need will automatically install if needed. 

If the output is still too large of a file, you'll need to start deleting elements like footers, or embedded SVG images, etc. using a tool like Chrome Developer Console and then run this script again.

Big thanks to [Evil Portal](https://github.com/bigbrodude6119/flipper-zero-evil-portal) for all their work. 
Bigbrodude6119 provides amazing instructions here.

## How it works

This script is designed to reduce the file size of single file HTML pages that have embedded CSS, fonts, and images. It does this by removing unused CSS classes and ids from the HTML and CSS, replacing base64 encoded fonts with client-side standard fonts, removing empty `div` tags, and minifying the HTML. The script reads an HTML file, parses it using BeautifulSoup, performs the optimizations, and then writes the optimized and minified HTML to new files. The script also calculates the initial, final, and minified file sizes to show how much the file size has been reduced. At the end of the script, it displays a final printout to the user with the original, stripped, and minified file sizes and provides instructions on the location of the output files.

## Installation

To install HTML Squasher from GitHub, follow these steps:

1. Clone the repository: `git clone https://github.com/RocketGod-git/evilportal-htmlsquash.git`
2. Navigate to the cloned repository: `cd evilportal-htmlsquash`
3. Install the required packages: `automatic on first run!`

## Usage

To use HTML Squasher on single file HTML portals captured with the SingleFile extension for Chrome Browser, follow these steps:

1. Save the single file HTML page using the SingleFile extension for Chrome Browser while your target website portal is open.
2. Run the script on the saved HTML file: `python htmlsquash.py path/to/saved/file.html`
3. Follow the instructions displayed by the script to locate the optimized and minified output files.

I hope this helps! Let me know if you have any questions or need further assistance. PRs always welcome.

![rocketgod_logo_transparent](https://github.com/RocketGod-git/evilportal-htmlsquash/assets/57732082/0331ca12-3dea-473b-a4ca-07d647020992)

