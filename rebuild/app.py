# Get the response from each category endpoint
# Get the groups of items in each category
# Split those groups into letters
# Generate URL's for each letter
# Get response from each generated URL
# Process response to gather necessary data
# Write processed response to dataframe
# Write dataframe to csv
from c_logger import CustomLogger
import time
import logging
import os
import pathlib

# Check for and create log folder
if not os.path.exists(str(pathlib.Path(__file__).parent.absolute()) + "/logs/"):
    os.mkdir(str(pathlib.Path(__file__).parent.absolute()) + "/logs/")


# Setup loggers
app_log = CustomLogger(
    name="app_log",
    log_file=str(pathlib.Path(__file__).parent.absolute()) + "/logs/application.log",
    level=logging.INFO,
).create_logger()

err_log = CustomLogger(
    name="err_log",
    log_file=str(pathlib.Path(__file__).parent.absolute()) + "/logs/error.log",
    level=logging.WARNING,
).create_logger()


def log_error(c_msg: str, err: str, url: str = "N/A", res: str = "N/A") -> None:
    custom_message = f"{c_msg}\n\n{err}"
    err_log.warning(custom_message)
    err_log.warning(f"Affected URL: {url}")
    err_log.warning(f"URL Response: {res}")


# Check age of csv
def file_is_old(file_path: str, max_age: int = 604800) -> bool:
    """max_age is in seconds

    minute = 60
    hour   = 3600
    12 hrs = 43200
    day    = 86400
    week   = 604800
    """
    x = os.stat(file_path)
    age = time.time() - x.st_mtime
    print(f"File {file_path} is {age} seconds old.")

    if age > max_age:
        app_log.info(f"File {file_path} is too old, generating new file.")
        return True
    else:
        app_log.info(
            f"File {file_path} is too new to replace, skipping file generation"
        )
        return False
