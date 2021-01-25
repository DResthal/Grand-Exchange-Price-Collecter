# Remember "Category -> Groups -> Items"
from apifetch.fetch_categories import get_all_categories
from apifetch.logger_setup import CustomLogger
import logging
import time
import os

error_log = CustomLogger("e_log", "error.log", level=logging.WARNING).create_logger()
application_log = CustomLogger("a_log", "app.log", level=logging.INFO).create_logger()

### Function Definitions ###
def check_file_age(file_path: str, max_age: int = 604800) -> None:
    x = os.stat(file_path)
    age = time.time() - x.st_mtime
    print(f"File {file_path} is {age} seconds old.")

    if age > max_age:
        application_log.info(f"group_urls.csv is too old, fetching new list")
        print("Fetching new url list, list is too old.")
        get_all_categories(43)
    else:
        application_log.info(f"group_urls.csv is less than 7 days old, moving on.")
        print("Skipping group url list fetch, file is too new")
        pass


# Check if group_urls.csv exists
# If not, fetch urls
# If yes, fetch items
# Save items to db if not exists
# Save prices to db

url_file_path = os.path.abspath("group_urls.csv")


if not os.path.exists(url_file_path):
    application_log.info("groups_urls.csv not found, fetching urls")
    print("Fetching group url list")
    get_all_categories(43)
else:
    application_log.info("groups_urls.csv exists, checking age")
    check_file_age(url_file_path)
