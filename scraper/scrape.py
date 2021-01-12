import requests as req
import math
import json
import pandas as pd
import numpy as np
from datetime import datetime
import time


today = datetime.now().strftime("%m-%d-%Y-%H")
now = datetime.now().strftime("%m-%d-%Y-%H-%M")

categories_url = (
    "https://secure.runescape.com/m=itemdb_rs/api/catalogue/category.json?category=
    "
)
# items url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=0&alpha=a&page=1"

# Get the letter, number of items and number of pages from each item group
def get_groups(cat_response, cat_num):

    # Encode '#' for later use in the URL
    if cat_response[0]["letter"] == "#":
        cat_response[0]["letter"] = "%23"

    for i in range(len(cat_response)):
        letter = cat_response[i]["letter"]
        num_items = cat_response[i]["items"]
        # Find the number of pages there are based on the number of items (of which there are 12 per page), round up to nearest whole
        num_pages = math.ceil((num_items / 12) + 1)

        # Do not send to get_items if no pages of items exist
        if num_pages != 0:
            get_items_list(letter, num_pages, cat_num)
        else:
            pass


# Get the list of items from the each item group page
def get_items_list(letter, num_pages, cat_num):

    for page in range(num_pages):
        url = f"https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category={cat_num}&alpha={letter}&page={page}"
        print(f"Fetching items from item url. Page: {page}, Letter: {letter}")
        start = time.perf_counter()
        # Currently, this breaks the entire program if TimeOut or other failure...
        raw_items = req.get(url).json()
        print(f'URL Fetch took {round((time.perf_counter() - start), 3)} seconds...')
        print(url)
        get_single_items(raw_items)


# Get each item from the item list
def get_single_items(raw_items):
    converted_to_dict = json.dumps(raw_items)
    items = json.loads(converted_to_dict)["items"]
    add_to_df(items)


# Add each item to the pandas dataframe, remove duplicates, save to csv
def add_to_df(items):
    csv_name = f"{today}_all_items.csv"
    items_list = []

    for item in items:
        item_dict = {
            "id": item["id"],
            "name": item["name"],
            "description": item["description"],
            "type": item["type"],
            "current_price": item["current"]["price"],
            "members": item["members"],
        }
        print(f'Adding {item["name"]} to list...')
        items_list.append(item_dict)

    temp_df = pd.DataFrame(items_list).drop_duplicates(
        subset=["name", "current_price"], keep="last"
    )

    if temp_df.empty:
        print("You have no data here!")
    else:
        temp_df = temp_df.set_index(["id"])
        temp_df.to_csv(csv_name, mode="a", header=False)
        print(f"{csv_name} has been saved.")


# Iterate over each category, I have manually discovered that there are 42 categories, 43+ returns null
# For each category, get the "item groups"
for i in range(43):
    print(f"Getting Category {i}")
    category_response = req.get(categories_url + str(i)).json()["alpha"]
    get_groups(category_response, i)

print(items_list)
print(f"Completed at: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
