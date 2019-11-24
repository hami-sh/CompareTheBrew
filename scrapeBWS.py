from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures as threadingPool
from classItem import Item, ItemCollection
import logging
from scrape import *

def item_thread_bws(item, commonList):
    """
    Thread function to control parsing of BWS drink details
    """
    # brand
    brand = item.find('h2', {'class': 'productTile_brand ng-binding'})
    # name
    name = item.find('div', {'class': 'productTile_name ng-binding'})
    # price
    dollar = item.find('span', {'class': 'productTile_priceDollars ng-binding'})
    cents = item.find('span', {'class': 'productTile_priceCents ng-binding'})
    price = str(dollar.text) + '.' + str(cents.text)
    # link
    link = item.find('a', {'class':'link--no-decoration'})
    print(2)

    # Scrape the html using the general scrape.download function rather than duplicate fucking code
    url = "https://bws.com.au" + link['href']

    soup = download(url)
    # # Configure options for the chrome web driver which is used as a headless browser to scrape html and render javascript for web pages
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(options=chrome_options)
    # # Get the HTML from the given url
    # driver.get(url)
    # # Create a BeautifulSoup object from the raw HTML string, to make it easier for us to search for particular elements later
    # soup = BeautifulSoup(driver.page_source, 'html.parser')

    detailsRaw = soup.find('div', {'class':'product-additional-details_container text-center ng-isolate-scope'})
    list = detailsRaw.find('ul', {'class':'text-left'})
    keys = list.findAll('strong', {'class':'list-details_header ng-binding'})
    values = list.findAll('span', {'class':'pull-right list-details_info ng-binding ng-scope'})
    print(3)
    details = dict()
    for x in range(0, len(keys)):
        details[keys[x].text] = values[x].text

    size = 0
    if details['Liquor Size'].find('mL') != -1:
        # measurement in mL
        strSize = details['Liquor Size'][0:len(details['Liquor Size']) - 2]
        size = int(strSize) / 1000
    else:
        # measurement in L
        strSize = details['Liquor Size'][0:len(details['Liquor Size']) - 1]
        size = int(strSize)
    print(4)
    efficiency = float(details['Standard Drinks']) / float(price)
    entry = Item("BWS", brand.text, name.text, price, "https://bws.com.au" + link['href'], details['Liquor Size'],
                 details['Alcohol %'], details['Standard Drinks'], efficiency)
    print(5)
    print(entry.name + " " + entry.stdDrinks + " " + entry.price + " " + str(size) + " " + str(efficiency))
    commonList.append(entry)
    print(6)
