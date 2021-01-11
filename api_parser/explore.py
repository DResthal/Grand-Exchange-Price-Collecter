import requests as req
import math
from datetime import datetime
#import json

categories_url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/category.json?category=0"
# items url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=0&alpha=a&page=1"

# Iterate over each category, I have manually descovered that there are 42 categories, 43+ returns null
# Example response
# [
#    {'letter': '#', 'items': 3}, 
#    {'letter': 'a', 'items': 65}, 
#    {'letter': 'b', 'items': 82}, 
#    {'letter': 'c', 'items': 91}, 
#    {'letter': 'd', 'items': 53}, 
#    {'letter': 'e', 'items': 15}, 
#    {'letter': 'f', 'items': 24}, 
#    {'letter': 'g', 'items': 46}, 
#    {'letter': 'h', 'items': 22}, 
#    {'letter': 'i', 'items': 22}, 
#    {'letter': 'j', 'items': 2}, 
#    {'letter': 'k', 'items': 10}, 
#    {'letter': 'l', 'items': 21}, 
#    {'letter': 'm', 'items': 39}, 
#    {'letter': 'n', 'items': 6}, 
#    {'letter': 'o', 'items': 25}, 
#    {'letter': 'p', 'items': 95}, 
#    {'letter': 'q', 'items': 0}, 
#    {'letter': 'r', 'items': 41}, 
#    {'letter': 's', 'items': 118}, 
#    {'letter': 't', 'items': 30}, 
#    {'letter': 'u', 'items': 1}, 
#    {'letter': 'v', 'items': 22}, 
#    {'letter': 'w', 'items': 19}, 
#    {'letter': 'x', 'items': 1}, 
#    {'letter': 'y', 'items': 2}, 
#    {'letter': 'z', 'items': 9}
# ]
for i in range(42):
    category_response = req.get(categories_url + str(i)).json()['alpha']
    print(category_response)

'''
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


# extracting the item groups from the returned category json
def get_items(item_attr: dict) -> dict:
    
    for p in range(item_attr["numPages"]):
        url = f"https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category={item_attr['category']}&alpha={item_attr['alpha']}&page={p}"
        res = req.get(url)
        if 'json' in res.headers:
            print(res.json())
        else:
            print("No JSON to display")
'''