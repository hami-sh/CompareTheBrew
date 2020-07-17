from urllib.request import Request, urlopen
import argparse
from typing import List
import json
import csv
import os
from scripts.databaseHandler import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Column, Integer, Float, String, Boolean
)


Base = declarative_base()


class Item(Base):
    __tablename__ = "items1"

    store = Column(String)
    brand = Column(String)
    name = Column(String)
    price = Column(String)
    type = Column(String)
    link = Column(String)
    ml = Column(String)
    percent = Column(String)
    std_drinks = Column(String)
    numb_items = Column(String)
    efficiency = Column(String)
    image = Column(String)
    promotion = Column(Boolean)
    old_price = Column(Float)
    column_not_exist_in_db = Column(Integer, primary_key=True)

    def __str__(self):
        # Create a new string
        repr_string = f"{self.store}, {self.brand}, {self.name}, " \
            f"${self.price}," \
            f"{self.type}, {self.link}, {self.ml}mL, {self.percent}, " \
            f"{self.std_drinks}, {self.numb_items}, {self.efficiency}, " \
            f"{self.image}, {self.promotion}, ${self.old_price}"
        return repr_string


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
            parentcode = None
            item_numb = None
            percent_alcohol = None
            image_numb = None
            std_drinks = -1
            link = None
            style = None
            size = None

            for i in subdrink["AdditionalDetails"]:
                if i["Name"] == "parentstockcode":
                    parentcode = i["Value"]  # important for URL
                elif i["Name"] == "productunitquantity":
                    item_numb = float(i[
                                          "Value"])  # quantity of the item (a la cans in a pack)
                elif i["Name"] == "alcohol%":
                    percent_alcohol = i["Value"]  # alcohol percentage
                    # TODO:Regex to find only the percentage number; change Item
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

            if percent_alcohol == None:
                for partners in drink["Products"]:
                    for subsection in partners["AdditionalDetails"]:
                        if subsection["Name"] == "alcohol%":
                            percent_alcohol = subsection["Value"]

            if size == None:
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

            if style == None:
                for partners in drink["Products"]:
                    for subsection in partners["AdditionalDetails"]:
                        if subsection["Name"] == "standardcategory":
                            style = subsection["Value"]

            try:
                if std_drinks == -1:
                    raise Exception  # break to failed

                if item_numb != 1 and std_drinks != -2 and std_drinks != -1:
                    std_drinks = item_numb * std_drinks  # account for multiple items in a pack

                efficiency = std_drinks / float(subdrink["Price"])
            except:
                print("\t", "failed ->", std_drinks, item_numb,
                      subdrink["Price"])

            # store as class
            item = Item(store="bws", brand=subdrink["BrandName"],
                        name=subdrink["Name"].strip(),
                        type=style, price=subdrink["Price"], link=drink_link,
                        ml=size, percent=percent_alcohol,
                        std_drinks=std_drinks, numb_items=item_numb,
                        efficiency=efficiency, image=image_link,
                        promotion=subdrink['IsOnSpecial'],
                        old_price=subdrink["WasPrice"])

            result.append(item)

    return result


def website_searcher(store: str, category: str) -> str:
    with open("websites.json") as fp:
        websites = json.load(fp)
        url = websites[store][category]
    return url


# MARK: main function 
def main():
    # get arguments from the command line
    parser = argparse.ArgumentParser(description='scrape drinks from websites')
    parser.add_argument('store', type=str, help='bws, ll, fc, dm')
    parser.add_argument('category', type=str,
                        help='beer or wine or spirits or SEARCH TERM')
    args = parser.parse_args()
    global store, category, populate
    store = args.store
    category = args.category

    engine = create_engine(
        os.getenv("DB_URL"), echo=True)

    data = search(search_term=category,
                  store=store)  # scrape all the data for those
    # search terms from bws
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine, autoflush=False)
    session = Session()

    # save to csv
    # with open('output.csv', 'w', newline='') as file:
    #     for item in data:
    #         file.write(str(item) + "\n")

    # for item in data:
    #     print(item)
        # session.add(item)
    # session.commit()


if __name__ == "__main__":
    main()
