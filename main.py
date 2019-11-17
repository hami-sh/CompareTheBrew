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
            total.collection.append(item_thread.result())
            print(item_thread.result().name + " " + item_thread.result().price)


def item_thread_bws(item):
    # brand
    brand = item.find('h2', {'class': 'productTile_brand ng-binding'})
    # name
    name = item.find('div', {'class': 'productTile_name ng-binding'})
    # price
    dollar = item.find('span', {'class': 'productTile_priceDollars ng-binding'})
    cents = item.find('span', {'class': 'productTile_priceCents ng-binding'})
    price = str(dollar.text) + '.' + str(cents.text)

    entry = Item("BWS", brand.text, name.text, price)
    return entry


def main():
    parser = argparse.ArgumentParser(description='Enter alcohol to search')
    parser.add_argument("--drink", default='vodka', help="The drink")
    args = parser.parse_args()

    total = ItemCollection()
    # BWS
    bws = "https://bws.com.au/search?searchTerm=" + args.drink
    download_bws(bws, "bws", "txt", total)

    # Dan Murphy

    # ...

if __name__ == '__main__':
    main()
