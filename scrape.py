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
import csv
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
    elif store == "vc":
        searched_data = vc_handler(search_term)
    

    return searched_data

"""
vc format

"""

def vc_handler(search_term: str):
    result = list()
    
    # get website for search term
    url = website_searcher("vc", search_term)
    
    # download drinks data
    data = None
    # with urlopen(url) as api_json:
        # data = json.loads(api_json.read().decode())
        # print(data)
    with open ("vc.json") as vcjson:
        data = json.load(vcjson)
        urllist = []
        result = []
        for product in data["products"]:
            productcat = (product["category"])
            productid = (product["id"])
            finalURL = f"https://www.vintagecellars.com.au/api/products/vc/qld/{productcat}/{productid}"
            urllist.append(finalURL)

        for drinkurl in urllist:    
            with open ("subdrink.json") as drinkjson:
                drink = json.load(drinkjson)
                subdrink = drink["product"]
                productcat = (subdrink["category"])
                productid = (subdrink["id"])
                price=subdrink["price"]["current"]
                old_price = subdrink["price"]["normal"]
                drink_link = f"https://www.vintagecellars.com.au/api/products/vc/qld/{productcat}/{productid}"
                style = None
                size = None
                percent_alcohol = None
                std_drinks = None
                item_numb = None
                efficiency = None
                image_link = subdrink["image"]["heroImage"]
                promotion = None
                

                # Style (type of drink)
                for i in subdrink["productProperties"]:
                    if i["key"] == "Style":
                        style = i["value"]

                # Standard Drinks
                for i in subdrink["productProperties"]:
                    if i["key"] == "Standard Drinks":
                        std_drinks = i["value"]

                # Size
                if size == None:
                    size = subdrink["volumeMl"]

                # Alcohol Percentage
                for i in subdrink["productProperties"]:
                    if i["key"] == "Alcohol Content":
                        temp_percent = i["value"]
                        percent_alcohol = temp_percent.split("%")[0]

                # Standard Drinks
                for i in subdrink["productProperties"]:
                    if i["key"] == "Standard Drinks":
                        std_drinks = i["value"]

                # Number of Items
                item_numb = 1
                if "CTN" in subdrink["unitOfMeasureLabel"]:
                    item_numb = int(temp_size.split("CTN")[1])

                # Efficiency (cartons first)
                multiplier = 1
                if "CTN" in subdrink["unitOfMeasureLabel"]:
                    temp_size = subdrink["unitOfMeasureLabel"]
                    multiplier = float(temp_size.split("CTN")[1])
                efficiency = (float(std_drinks) * multiplier)/float(price)

                # Promotion
                promotion = True
                if subdrink["promotion"] == None:
                    promotion = False
                
                item = Item(store="vc", brand=subdrink["brand"], name=subdrink["name"].strip(), type=style, 
                            price=price, link=drink_link, ml=size,
                            percent=percent_alcohol, std_drinks=std_drinks, numb_items=item_numb, efficiency=efficiency,
                            image=image_link, promotion=promotion, old_price=old_price)

                print(item)

                result.append(item)


            # item = Item(store="bws", brand=subdrink["BrandName"], name=subdrink["Name"].strip(), 
                        # type=style, price=subdrink["Price"], link=drink_link, ml=size, percent=percent_alcohol,
                        # std_drinks=std_drinks, numb_items=item_numb, efficiency=efficiency, image=image_link,
                        # promotion=subdrink['IsOnSpecial'], old_price=subdrink["WasPrice"])
            



"""
bws format
bundles -> INTEGER (drink) -> Products -> INTEGER (subdrink) -> [[details required]]
"""
def bws_handler(search_term: str) -> List:
    result = list()
    
    # get website for search term
    url = website_searcher("bws", search_term)
    
    # download drinks data
    data = None
    with urlopen(url) as api_json:
        data = json.loads(api_json.read().decode())
    
    # get specific json sections
    data = data['Bundles']
    for drink in data:
        thing = drink['Products']
        for subdrink in thing:
            print(subdrink["Name"], subdrink["Price"])
            # compute from {additionaldetails} section
            parentcode = "None"
            item_numb = "None"
            percent_alcohol = "None"
            image_numb = "None"
            std_drinks = -1
            link = "None"
            style = "None"
            size = "None"
            
            for i in subdrink["AdditionalDetails"]:
                if i["Name"] == "parentstockcode":
                    parentcode = i["Value"] # important for URL
                elif i["Name"] == "productunitquantity":
                    item_numb = float(i["Value"]) # quantity of the item (a la cans in a pack)
                elif i["Name"] == "alcohol%":
                    percent_alcohol = i["Value"] # alcohol percentage
                elif i["Name"] == "image1":
                    image_numb = i["Value"]
                elif i["Name"] == "standarddrinks":
                        std_drinks = i["Value"]
                        std_drinks = std_drinks.replace('Approx.', '')
                        std_drinks = std_drinks.replace('Approx', '')
                        std_drinks = std_drinks.split(" ")[0]
                        try:
                            std_drinks = float(std_drinks.strip())
                        except:
                            std_drinks = -1
                elif i["Name"] == "bwsproducturl":
                    link = i["Value"]
                elif i["Name"] == "standardcategory":
                    style = i["Value"]
                elif i["Name"] == "liquorsize":
                    size = i["Value"]
                    if "Pack" in size:
                        try:
                            size = size.split(" ")[2]
                        except:
                            size = "-2"
                    if "ml" in size:
                        size = size.split("ml")[0]
                    elif "mL" in size:
                        size = size.split("mL")[0]
                    elif "L" in size:
                        size = float(size.split("L")[0]) * 1000
                    try:
                        size = float(size)
                    except:
                        size = "-2"
                    
            drink_link = f"https://bws.com.au/product/{parentcode}/{link}"
            image_link = f"https://edgmedia.bws.com.au/bws/media/products/{image_numb}"
            
            if std_drinks == -1:
                # search through json to find proper std drinks
                for partners in drink["Products"]:
                    for subsection in partners["AdditionalDetails"]:
                        if subsection["Name"] == "standarddrinks":
                            std_drinks = subsection["Value"]
                            print("\t FOUND", std_drinks)
                            std_drinks = std_drinks.replace('Approx.', '')
                            std_drinks = std_drinks.replace('Approx', '')
                            try:
                                std_drinks = float(std_drinks.strip())
                            except:
                                std_drinks = -2
                            break
                std_drinks = -2
            
            if percent_alcohol == "None":
                for partners in drink["Products"]:
                    for subsection in partners["AdditionalDetails"]:
                        if subsection["Name"] == "alcohol%":
                            percent_alcohol = subsection["Value"]
                            
            if size == "None":
                for partners in drink["Products"]:
                    for subsection in partners["AdditionalDetails"]:
                        if subsection["Name"] == "liquorsize":
                            size = subsection["Value"]
                            if "Pack" in size:
                                size = size.split(" ")[2]
                            if "ml" in size:
                                size = size.split("ml")[0]
                            elif "mL" in size:
                                size = size.split("mL")[0]
                            elif "L" in size:
                                size = str(float(size.split("L")[0]) * 1000)
                                
            if style == "None":
                for partners in drink["Products"]:
                    for subsection in partners["AdditionalDetails"]:
                        if subsection["Name"] == "standardcategory":
                            style = subsection["Value"]
                
            
            try:
                if std_drinks == -1:
                    raise Exception # break to failed
                
                if item_numb != 1 and std_drinks != -2 and std_drinks != -1:
                    std_drinks = item_numb * std_drinks # account for multiple items in a pack
                
                efficiency = std_drinks / float(subdrink["Price"])
            except:
                print("\t", "failed ->", std_drinks, item_numb, subdrink["Price"])
        

            # store as class
            item = Item(store="bws", brand=subdrink["BrandName"], name=subdrink["Name"].strip(), 
                        type=style, price=subdrink["Price"], link=drink_link, ml=size, percent=percent_alcohol,
                        std_drinks=std_drinks, numb_items=item_numb, efficiency=efficiency, image=image_link,
                        promotion=subdrink['IsOnSpecial'], old_price=subdrink["WasPrice"])
            
            result.append(item)
            
    return result        
    
        
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
    
    # save to csv
    with open('output.csv', 'w', newline='') as file:
        for item in data:
            file.write(repr(item) + "\n")
            
            
    
    #todo save data to db.

if __name__ == "__main__":
    main()