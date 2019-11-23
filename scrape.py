from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures as threadingPool
from classItem import Item, ItemCollection
import logging


def download(url, target_filename, filename_extension, total, listBWS):
    """
    Function to parse a site (circa November 2019) and return a BeautifulSoup of its HTML

    Args:
        url: The url to be scraped
        target_filename: the output file that the data will be saved to
        filename_extension: file type of the output file
        total:
        list: a list for the output data to be put into

    Returns: A BeautifulSoup of the page html
    """
    # Configure options for the chrome web driver which is used as a headless browser to scrape html and render javascript for web pages
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    # Get the HTML from the given url
    driver.get(url)
    # Create a BeautifulSoup object from the raw HTML string, to make it easier for us to search for particular elements later
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def get_drinks(soup, liquorSite):
    """
    Function to get a list of drink data from a BeautifulSoup and return the data in a list

    Args:
        soup: a BeautifulSoup object

    Returns: A list of drink data
    """
    # Get the drinks profiles based on the given liquorSite
    if liquorSite == "bws":
        # Extract the drink profiles from the BeautifulSoup (configured for bws)
        drinks = soup.findAll('div', {'class':'productTile'})
    else if liquorSite == "liquorland":
        # Extract the drink profiles from the BeautifulSoup (configured for liquorland)
        specials = soup.findAll('div', {'class':'product-tile-wrapper update-specials-border'})
        drinks = soup.findAll('div', {'class': 'product-tile-wrapper'})
        drinks.append(specials)

    # Extract the drink profiles from the BeautifulSoup (configured for bws)
    drinks = soup.findAll('div', {'class':'productTile'})
    # Print all of the drinks profiles
    print('SCRAPED ' + str(len(drinks)))
    # Threading stuff basically executes multiple copies item_thread_bws(item, listBWS) concurrently
    threads = 0
    with threadingPool.ThreadPoolExecutor() as executor:
        for item in drinks:
            print("INIT_THREAD[" + str(threads) + "]")
            threads += 1
            # Run item_thread_bws(item, listBWS)
            executor.submit(item_thread_bws, item, listBWS)

def item_thread_bws(item, listBWS):
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

    efficiency = float(details['Standard Drinks']) / float(price)
    entry = Item("BWS", brand.text, name.text, price, "https://bws.com.au" + link['href'], details['Liquor Size'],
                 details['Alcohol %'], details['Standard Drinks'], efficiency)
    print(entry.name + " " + entry.stdDrinks + " " + entry.price + " " + str(size) + " " + str(efficiency))
    listBWS.append(entry)
