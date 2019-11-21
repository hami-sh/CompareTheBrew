import argparse
import logging
import concurrent.futures as threadingpool
from classItem import Item, ItemCollection
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

threads = list()
parsedBWS = list()


def download_bws(url, target_filename, filename_extension, total):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    drinks = soup.findAll('div', {'class':'productTile'})
    print('found ' + str(len(drinks)))

    j = 0
    with threadingpool.ThreadPoolExecutor() as executor:
        for item in drinks:
            print("thread start")
            executor.submit(item_thread_bws, item)

def item_thread_bws(item):
    print("start parse")
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

    # alcohol content
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://bws.com.au" + link['href'])
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    detailsRaw = soup.find('div', {'class':'product-additional-details_container text-center ng-isolate-scope'})
    list = detailsRaw.find('ul', {'class':'text-left'})
    keys = list.findAll('strong', {'class':'list-details_header ng-binding'})
    values = list.findAll('span', {'class':'pull-right list-details_info ng-binding ng-scope'})
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

    efficiency = size / float(price)

    entry = Item("BWS", brand.text, name.text, price, "https://bws.com.au" + link['href'], details['Liquor Size'],
                 details['Alcohol %'], details['Standard Drinks'], efficiency)

    # parsedBWS.append(entry)
    print(entry.name + " " + entry.stdDrinks + " " + entry.price)

def organize(drinks):
    # in Aus, std drink == 10g
    # efficiency -> std drinks / price
    # sorted(drinks)

    for drink in drinks:
        print(drink.name + " " + drink.stdDrinks + " " + drink.price)



def main():
    parser = argparse.ArgumentParser(description='Enter alcohol to search')
    parser.add_argument("--drink", default='vodka', help="The drink")
    args = parser.parse_args()

    total = ItemCollection()
    # BWS
    bws = "https://bws.com.au/search?searchTerm=" + args.drink
    bwsPool = download_bws(bws, "bws", "txt", total)

    # Dan Murphy

    # ...
    organize(parsedBWS)


if __name__ == '__main__':
    main()
