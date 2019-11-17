import argparse
import concurrent.futures as thread
from classItem import Item, ItemCollection
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def download_bws(url, target_filename, filename_extension, total):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    drinks = soup.findAll('div', {'class':'productTile'})
    print('found ' + str(len(drinks)))

    for item in drinks:
        with thread.ThreadPoolExecutor() as executor:
            item_thread = executor.submit(item_thread_bws, item)
            print(item_thread.result().name + " " + item_thread.result().price + " " + str(item_thread.result().ml)
                  + " " + str(item_thread.result().efficiency) + " " + item_thread.result().link)


def item_thread_bws(item):
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

    size = 0;
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

    return entry


def organize(drinks):
    # in Aus, std drink == 10g
    # efficiency -> std drinks / price
    sorted(drinks)

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
    organize(bwsPool)


if __name__ == '__main__':
    main()
