# Group preprocessing functions to make ready for item fetching
import logging
from math import ceil

error_log = logging.getLogger("e_log")
application_log = logging.getLogger("a_log")


class ItemParser:
    def url_encode(group: dict) -> dict:
        application_log.info("Checking for url compatibility...")
        if group["letter"] == "#":
            application_log.info(
                f"Non-compatible letter found, encoding for url use. {group}"
            )
            group["letter"] = "%23"
        else:
            application_log.info(f"URL Encoding not-needed for {group}")
        return group

    def add_num_of_pages(group: dict) -> dict:
        num_of_items = group["items"]

        if num_of_items == 0:
            group.update({"num_of_pages": 0})
        else:
            num_of_pages = ceil(num_of_items / 12)
            group.update({"num_of_pages": num_of_pages})

        return group

    def build_url(group: dict, page: int, cat_num: int) -> dict:
        letter = group["letter"]
        url = f"https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category={cat_num}&alpha={letter}&page={page}"
        return url
