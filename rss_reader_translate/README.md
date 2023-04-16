# HAXILL RSS Feed Translator
This script retrieves the content of an RSS feed (title, description, and link), translates the title and description of the entries into any language, removes the last sentence of the description if it is identical to the title, displays the results, and reads the title and description aloud.

# Prerequisites
Before running the script, make sure you have the following Python packages installed:

* feedparser
* beautifulsoup4
* colorama
* gtts
* pygame
* langdetect
* mtranslate

You can install them by running:

`pip install feedparser beautifulsoup4 colorama gtts pygame langdetect mtranslate`

# Usage
1 - Clone the repository or download the script file.

2 - Open a terminal and navigate to the directory containing the script.

3 - Run the script by typing `python rss_feed_translator.py`.

4 - Enter the language in which you want to read the results (e.g., "fr", "en", "es", "it", "de", "ja", "uk", etc.).

5 - The script will retrieve the content of the RSS feed, translate the titles and descriptions of the entries, remove the last sentence if necessary, display the results, and read them aloud.

# Acknowledgments
This script was created by HAXILL.
