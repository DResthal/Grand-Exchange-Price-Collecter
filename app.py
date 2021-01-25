# Main application will go here
# Rewrite coming soon.
from apifetch.fetch_categories import get_all_categories
from apifetch.logger_setup import CustomLogger
import logging
import os

error_log = CustomLogger("e_log", "error.log", level=logging.WARNING).create_logger()
application_log = CustomLogger("a_log", "app.log", level=logging.INFO).create_logger()

if not os.path.exists('group_urls.csv'):
    print("Getting categories")
    get_all_categories(43)
else:
    print('NOT getting categories')

print("Testing...")

