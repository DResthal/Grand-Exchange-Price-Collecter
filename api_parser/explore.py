import requests as req
import math
from datetime import datetime

categories_url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/category.json?category="
items_url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=0&alpha=a&page=1"

def get_item_attr(data: dict) -> dict:
    for i in data:

        item_attr = {
            "letter": i["letter"],
            "numItems": i["items"],
            "numPages": None
        }

    print(f"Category: {i}")
    get_item_attr(item_dict)
    
    

print(f"Done at {datetime.now()}")