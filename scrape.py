from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures as threadingPool
from classItem import Item, ItemCollection
from fake_useragent import UserAgent
from urllib.request import Request, urlopen
import logging
from scrapeBWS import item_thread_bws
from scrapeLiquorLand import item_thread_liquorland


def getData(url):
    """
    Gets all of the drinks data given a search url and returns it as a list
    """
    liquorSite = getLiquorSiteFromUrl(url)
    soup = download(url)
    drinksData = getDrinks(soup, liquorSite)
    return drinksData


def getLiquorSiteFromUrl(url):
    """
    Takes a search url (e.g. "https://bws.com.au/search?searchTerm="vodka") and automatically detects the liquorSite name and returns it
    """

    # Separate the url into list items about the periods
    urlList = url.split(".")
    # If the first element ends in www - e.g. url of form https://www.firstchoiceliquor.com.au/, take the second element in the list as the liquorSite name
    if urlList[0][-3:] == "www" or urlList[0][-3:] == "ww2":
        liquorSite = urlList[1]
    else:
        # If we have a url without a www. url e.g. urlList=["https://bws", "com", "au/search?searchTerm='vodka'"] simply take the first element, split by the '/' and take the element in posiiton 2 of the resulting list
        liquorSite = urlList[0].split("/")[2]
    return liquorSite


def download(url):
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


def getDrinks(soup, liquorSite):
    """
    Function to get a list of drink data from a BeautifulSoup and return the data in a list

    Args:
        soup: a BeautifulSoup object

    Returns: A list of drink data
    """
    print("site: " + liquorSite)
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

    # Create an empty list in which to store our drinks data (each drink will have its own Item object (see classItem) which will be added to the list)
    drinksdata = list()

    # Get the drink data for each drink profile we collected
    # Threading stuff basically executes multiple copies item_thread_XXX(item) concurrently
    threads = 0
    with threadingPool.ThreadPoolExecutor(max_workers=3) as executor:
        for item in drinks:
            print("INIT_THREAD[" + str(threads) + "]")
            threads += 1
            # Execute the correct item_thread function based on the given liquorSite
            if liquorSite == "bws":
                # Run item_thread_bws(item)
                print(1)
                executor.submit(item_thread_bws, item, drinksdata)
            elif liquorSite == "liquorland":
                # Run item_thread_liquorland(item)
                executor.submit(item_thread_liquorland, item, drinksdata)

    # Return the drinksData
    return drinksdata
