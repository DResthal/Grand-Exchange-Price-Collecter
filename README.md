# miniature-octo-guide  

Scrape the entirety of the Runescape grand exchange api and collect price information of all items included.  
This API is not very clean, nor reliable and during each run, some errors may result from fetching urls, and this seems to happen at random. Visiting these URLs manually correctly returns the JSON response desired 90% of the time.  
For this reason, the resulting all_items.csv will NOT contain all items and prices, and each consecutive run may contain different missing values.  

This script is intended to be run as a Linux cron-job and the api scraped at 00:00 GMT and 12:00 GMT each day. Time-series data is NOT collected from this api so an amount of time equal to the date-range desired must pass with this script being reliably run during this time to collect such data.  

all_items.csv contains all information of each item provided by the API, including links to icons, category icons, descriptions, names, current and "today" prices and more. Please provide your own data pre-processing pipeline to the resultant data if you wish to collect less information, or manipulate / append columns in any way.