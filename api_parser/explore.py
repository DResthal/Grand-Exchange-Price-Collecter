import requests as req
import math
from datetime import datetime

categories_url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/category.json?category=0"
# items url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=0&alpha=a&page=1"

# Create dict for each group in category endpoint
def get_category_groups(raw: dict, cat: int) -> dict:
    item_attr = {
        "category": cat,
        "alpha": raw["letter"],
        "numItems": raw["items"],
        "numPages": None
    }

    pages = math.ceil(item_attr["numItems"] / 12)

    item_attr["numPages"] = pages

    return item_attr


# Get each item from each 
def get_items(item_attr: dict) -> dict:
    
    for p in range(item_attr["numPages"]):
        url = f"https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category={item_attr['category']}&alpha={item_attr['alpha']}&page={p}"
        res = req.get(url)
        print(url)



# 42 was a manually discovered integer for max number of category pages. 43 returns null
for c in range(4):
    res_data = req.get(categories_url + str(c)).json()["alpha"]
    #print(res_data)
    for i in res_data:
        #print(get_category_groups(i, c))
        get_items(get_category_groups(i, c))




print(f"Done at {datetime.now()}")