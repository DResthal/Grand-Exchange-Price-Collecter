import requests as req
import math
from datetime import datetime

# import json

categories_url = (
    "https://secure.runescape.com/m=itemdb_rs/api/catalogue/category.json?category=0"
)
# items url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=0&alpha=a&page=1"


def get_groups(cat):
    item_list = []

    for i in range(len(cat)):
        item_group = {cat[i]["letter"], cat[i]["items"]}
        item_list.append(item_group)

    print(item_list)


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
for i in range(1):
    category_response = req.get(categories_url + str(i)).json()["alpha"]
    get_groups(category_response)
