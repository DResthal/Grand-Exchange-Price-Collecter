import requests as req
import math
import json
import csv
import os
from datetime import datetime

# import json

categories_url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/category.json?category=0"
# items url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=0&alpha=a&page=1"

# Pass each category's groups of items to another function
def get_groups(cat_response, cat_num):

    # Encode '#' for later use in the URL
    if cat_response[0]["letter"] == '#':
        cat_response[0]["letter"] = '%23'

    for i in range(len(cat_response)):
        letter = cat_response[i]['letter']
        num_items = cat_response[i]["items"]

        # Find the number of pages there are based on the number of items (of which there are 12 per page), round up to nearest whole
        num_pages = math.ceil((num_items / 12) + 1)

        # Do not send to get_items if no pages of items exist
        if num_pages != 0:
            get_items_list(letter, num_pages, cat_num)
        else:
            pass



def get_items_list(letter, num_pages, cat_num):

    for page in range(num_pages):
        url = f'https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category={cat_num}&alpha={letter}&page={page}'
        raw_items = req.get(url).json()

        # logging all things before processing
        # I want to avoid writing this, when necessary, but because it is a loop, it is proving somewhat challenging
        # checking if the file exists would stop all other categories from writing to the page, but not checking
        # wastes time by writing to this csv every single run...
        # I'm honestly not sure if I will keep this level of logging in the future, why do I need it?
        with open('all_items.csv', 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(raw_items)

        get_single_items(raw_items)


def get_single_items(raw_items):
    converted_to_dict = json.dumps(raw_items)
    items = json.loads(converted_to_dict)['items']
    today = datetime.now().strftime("%m-%d-%Y-%H")
    csv_columns = ['id', 'name', 'description', 'type', 'current_price', 'members']

    for item in items:

        item_dict = {
        'id' : item['id'],
        'name' : item['name'],
        'description' : item['description'],
        'type' : item['type'],
        'current_price' : item['current']['price'],
        'members' : item['members']
        }

        # logging individual items
        with open(f'{today}_single_items.csv', 'a') as f:
            file_writer = csv.DictWriter(f, delimiter=',', fieldnames=csv_columns)
            file_writer.writeheader()
            file_writer.writerow(item_dict)

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

for i in range(43):
    print(f"cat: {i}")
    category_response = req.get(categories_url + str(i)).json()["alpha"]
    get_groups(category_response, i)

print(f"Completed at: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}"