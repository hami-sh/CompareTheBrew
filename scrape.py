# IMPORTS
# External
from urllib.request import Request, urlopen 

# Built-in
import logging
import re
# from threading import Lock
from random import randint
from time import sleep
import argparse
from typing import List
import json
# Custom
from scripts.databaseHandler import *

# GLOBAL VARIABLES
store = None
category = None
populate = False

def search(search_term: str, store: str) -> List:
    searched_data = list()
    
    if store == "bws":
        searched_data = bws_handler(search_term)
    

    return searched_data


"""
bws format
bundles -> INTEGER (drink) -> Products -> INTEGER (subdrink) -> [[details required]]
"""
def bws_handler(search_term: str) -> List:
    # get website for search term
    url = website_searcher("bws", search_term)
    
    # download drinks data
    data = None
    with urlopen(url) as api_json:
        data = json.loads(api_json.read().decode())
    
    # get specific json section
    data = data['Bundles']
    for drink in data:
        drink = drink['Products']
        for subdrink in drink:
            print(subdrink["Name"], subdrink["Price"])
    
        
def website_searcher(store: str, category: str) -> str:
    url = ""
    with open("websites.json") as fp:
        websites = json.load(fp)
        url = websites[store][category]
    return url


# MARK: main function 
def main():
    # get arguments from the command line
    parser = argparse.ArgumentParser(description='scrape drinks from websites')
    parser.add_argument('store', type=str, help='bws, ll, fc, dm')
    parser.add_argument('category', type=str, help='beer or wine or spirits or SEARCH TERM')
    args = parser.parse_args()

    global store, category, populate
    store = args.store
    category = args.category

    data = search(search_term=category, store=store)  # scrape all the data for those search terms from bws
    
    #todo save data to db.

if __name__ == "__main__":
    main()
