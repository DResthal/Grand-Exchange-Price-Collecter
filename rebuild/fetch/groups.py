import requests
import logging
import time
from .request_retry import ReqRetry
import json
import sys
import concurrent.futures

app_log = logging.getLogger("app_log")
err_log = logging.getLogger("err_log")

retry = ReqRetry(retries=5).retry()


def fetch_url(category: int) -> str:
    url = f"https://secure.runescape.com/m=itemdb_rs/api/catalogue/category.json?category={str(category)}"
    # Get url response
    try:
        res = retry.get(url)
    except:
        e = sys.exec.info()
        err_log.warning(e)

    res = json.loads(res.text)

    print(category)
    print(type(res))
    print(res)
    print("\n")

    # Append category number
    # Convert to string
    # Return string


def get_categories(ncats: int = 42) -> str:
    start = time.time()
    app_log.info("Starting scraper job at %s", start)

    with concurrent.futures.ThreadPoolExecutor() as exec:
        alphas = [exec.submit(fetch_url, cat) for cat in range(ncats)]

    end = time.time() - start
    app_log.info(f"Operation completed in {end} seconds.")
