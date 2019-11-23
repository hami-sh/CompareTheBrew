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
    drinks = list()
    # Get the drinks profiles based on the given liquorSite
    if liquorSite == "bws":
        # Extract the drink profiles from the BeautifulSoup (configured for bws)
        drinks = soup.findAll('div', {'class':'productTile'})
    elif liquorSite == "liquorland":
        # Extract the drink profiles from the BeautifulSoup (configured for liquorland)
        specials = soup.findAll('div', {'class':'product-tile-wrapper update-specials-border'})
        drinks = soup.findAll('div', {'class': 'product-tile-wrapper'})
        drinks.append(specials)


    # Print all of the drinks profiles
    print('SCRAPED ' + str(len(drinks)))
    # Threading stuff basically executes multiple copies item_thread_bws(item, listBWS) concurrently
    threads = 0
    with threadingPool.ThreadPoolExecutor() as executor:
        for item in drinks:
            print("INIT_THREAD[" + str(threads) + "]")
            threads += 1
            if liquorSite == "bws":
                # Run item_thread_bws(item, listBWS)
                executor.submit(item_thread_bws, item, listBWS)
            elif liquorSite == "liquorland":
                executor.submit(item_thread_liquorland, item, listBWS)


