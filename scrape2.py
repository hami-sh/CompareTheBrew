# IMPORTS
# External
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from urllib.request import Request, urlopen
# Built-in
import concurrent.futures as threadingPool
import logging
from threading import Lock
# Custom
from classItem import Item, ItemCollection

def scrape(url):
    """
    The master function that handles the complete pipeline of going from a search url to returning a final list of drink items.

    Args:
        url: the url we are scraping from
    Returns:
        drinksData: A list of Items which the data for each drink
    """
    # 1 & 2. Scrape the html for the search page and create beautifulsoup (generic). Then get the url for each drink result in the search (specific)
    drinkUrls = getDrinks(url)
    # 3 & 4. Follow each of the drink links utilising multiple threads to speed the process. Inside of each thread, once again scrape the page to a spoup (general), then get all the drink data from the drink page (specific)
    drinksData = getDrinksData(drinkUrls)
    return drinksData

def download(url):
    """
    Function to parse a site and return a BeautifulSoup of its HTML

    Args:
        url: The url to be scraped
        target_filename: the output file that the data will be saved to
        filename_extension: file type of the output file
        total:
        list: a list for the output data to be put into

    Returns: A BeautifulSoup of the page html
    """
    # TODO: Possible implement ip proxy rotation to increase ban safety
    # We are now downloading the html from the given url
    print("DOWNLOADING AND RENDERING HTML FROM " + url + " ...")

    # Configure options for the chrome web driver which is used as a headless browser to scrape html and render javascript for web pages
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    # Get the HTML from the given url
    driver.get(url)
    # Create a BeautifulSoup object from the raw HTML string, to make it easier for us to search for particular elements later
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def getSiteFromUrl(url):
    """
    Takes a search url (e.g. "https://bws.com.au/search?searchTerm="vodka") and automatically detects the site name and returns it
    """
    # Separate the url into list items about the periods
    urlList = url.split(".")
    # If the first element ends in www - e.g. url of form https://www.firstchoiceliquor.com.au/, take the second element in the list as the site name
    if urlList[0][-3:] == "www" or urlList[0][-3:] == "ww2":
        site = urlList[1]
    else:
        # If we have a url without a www. url e.g. urlList=["https://bws", "com", "au/search?searchTerm='vodka'"] simply take the first element, split by the '/' and take the element in posiiton 2 of the resulting list
        site = urlList[0].split("/")[2]
    return site

def getDrinks(url):
    """
    A function to find the link to every drink result to a liquor site search.
    """
    # Scrape the html for the search page and create beautifulsoup (generic)
    soup = download(url)

    # Detect the liquor site we are scraping from the url. This allows to extract the drinks using the correct strategies for the specific website.
    site = getSiteFromUrl(url)

    # Get the drinks profiles based on what site is being scraped
    if site == "bws":
        drinkUrls = getDrinksBws(soup)
    elif site == "liquorland":
    #     print("Yeet!")
    #     print(soup.prettify())
    #     # Extract the drink profiles from the soup
    #     specials = soup.findAll('div', {'class':'product-tile-wrapper update-specials-border'})
    #     drinks = soup.findAll('div', {'class': 'product-tile-wrapper'})
    #     drinks.append(specials)
        print("Sorry, LiquorLand is not currently a supported site.")
    elif site == "danmurphys":
        print("Sorry, Dan Murphy's is not currently a supported site.")
        # TODO: Implement drink url extraction from dan murphys search page
    elif site == "firstchoiceliquor":
        print("Sorry, First Choice Liquor is not currently a supported site.")
        # TODO: Implement drink url extraction from first choice liquor search page

    # Print out how many drink urls were found on the page
    print("FOUND " + str(len(drinkUrls)) + " DRINK URLS ON PAGE.")
    # Return the list of drink urls for us to individually scrape later on
    return drinkUrls

def getDrinksData(drinkUrls):
    """
    Function to get a list of drink data from a BeautifulSoup and return the data in a list

    Args:
        drinkUrls: a list of urls to the individual pages of the drinks found

    Returns: A list of drink data
    """
    # Now, the drink data must be extracted for each drink url found
    print('NOW EXTRACTING DRINKS DATA FROM DRINK URLS ...')

    # TODO: Remove this debug statement
    # print("###DEBUG### DRINK URLS:" + str(drinkUrls) + " ###/DEBUG###")

    # Detect the liquor site we are scraping from the url. This allows to extract the drink data using the correct strategies for the specific website.
    site = getSiteFromUrl(drinkUrls[0])

    # Create an empty list in which to store our drinks data (each drink will have its own Item object (see classItem) which will be added to the list)
    drinksdata = list()

    # Get the drink data for each drink profile we collected
    # Note: Threading stuff basically executes multiple copies item_thread_XXX(item) concurrently
    threads = 0
    _lock = Lock()
    with threadingPool.ThreadPoolExecutor(max_workers=1) as executor:
        for url in drinkUrls:
            # Print out every time a new thread is initialised
            print("INITIALISING THREAD " + str(threads) + ".")
            threads += 1

            # Extract the drink data based on the site being scraped
            if site == "bws":
                # Retrieve drink data from bws format html
                executor.submit(getDrinksDataBws, url, drinksdata, _lock)
            elif site == "liquorland":
                print("SORRY, DRINK DATA EXTRACTION IS NOT YET IMPLEMENTED FOR LIQUORLAND.")
            #     # Run item_thread_liquorland(item)
            #     executor.submit(item_thread_liquorland, item, drinksdata, _lock)

    # Return the drinksData
    return drinksdata

"""________________________________________SPECIFIC FUNCTIONS____________________________________________"""

def getDrinksBws(soup):
    """
    Drink url extraction for bws

    Args:
        soup: a html soup of a liquor site search page
    Returns:
        drinkUrls: a list of urls for specific drink pages
    """
    # Create a new list to store the drinks
    drinks = list()
    # Create a new list to store the urls to each drinks
    drinkUrls = list()
    #
    # Extract the drink cards from the search page soup
    drinksList = soup.find('div', {'class':'center-panel-ui-view ng-scope'})
    drinks = drinksList.findAll('div', {'class':'productTile'})
    for drink in drinks:
        # Extract the urls to each individual drink page
        relativePath = drink.find('a', {'class':'link--no-decoration'})['href']
        drinkUrls.append("https://bws.com.au" + relativePath)

    return drinkUrls


def getDrinksDataBws(url, drinksdata, _lock):
    """
    Thread function to control parsing of BWS drink details

    Args:
        url: the url of the website for the specific drink product we are collecting the data for
        drinksdata: the list of drink Items that all threads store their results in
        _lock: some threading shit (ask Hamish I guess)

    Returns:
        none (simply adds the result to the common list, since this function is running within a multi-threaded environment)
    """
    # Print our current status
    print("GETTING DRINK DATA FROM A DRINK PAGE ...")

    # Get the html soup for the drink page
    soup = download(url)

    # Extract the name
    name = soup.find('div', {'class':'detail-item_title'}).text

    # Extract the price
    priceElement = soup.find('span', {'class': 'trolley-controls_volume_price'})
    dollar = priceElement.find('span', {'class': 'ng-binding'}).text
    cents = priceElement.find('sup', {'class': 'ng-binding'}).text
    price = str(dollar) + '.' + str(cents)

    # Get the element containing all the details
    detailsRaw = soup.find('div', {'class':'product-additional-details_container text-center ng-isolate-scope'})
    # Get the ul of details inside the element
    list = detailsRaw.find('ul', {'class':'text-left'})
    # TODO: Remove this debug statement
    # Get all the titles of the properties
    keys = list.findAll('strong', {'class':'list-details_header ng-binding'})
    # Get all the values of the proverties
    values = list.findAll('span', {'class':'pull-right list-details_info ng-binding ng-scope'})
    # Put the titles and values as K,V pairs into a dictionary
    details = dict()
    for x in range(0, len(keys)):
        details[keys[x].text] = values[x].text

    # Extract the product brand
    brand = details['Brand']

    # Extract the bottle volume
    size = 0
    if details['Liquor Size'].find('mL') != -1:
        # measurement in mL
        strSize = details['Liquor Size'][0:len(details['Liquor Size']) - 2]
        size = int(strSize) / 1000
    else:
        # measurement in L
        strSize = details['Liquor Size'][0:len(details['Liquor Size']) - 1]
        size = int(strSize)

    # Find the price per standard by getting the number of standard drinks and dividing it by the price
    efficiency = float(details['Standard Drinks']) / float(price)

    # Put all of the details found for the drink into an Item object
    # entry = Item("BWS", brand.text, name.text, price, "https://bws.com.au" + link['href'], details['Liquor Size'], details['Alcohol %'], details['Standard Drinks'], efficiency)
    entry = ["BWS", details['Brand'], name, price, url, size, details['Alcohol %'], details['Standard Drinks'], efficiency]

    # Print out the list of drink data
    print("GOT DRINK DATA FOR: " + str(entry))

    # Add the list of data for this drink to the list of drinksData
    commonList.append(entry)

    # Handle the closing of the thread
    _lock.acquire()
    _lock.release()


"""________________________________________DEBUG MAIN FUNCTION____________________________________________"""

def main():
    print("START DEBUG SCRIPT")
    scrape("https://bws.com.au/search?searchTerm=thin")
    print("END DEBUG SCRIPT")

main()
