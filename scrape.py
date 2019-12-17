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
import re
from threading import Lock
from random import randint
from time import sleep
# Custom
from scripts.databaseHandler import *
import argparse

# GLOBAL VARIABLES
store = None
category = None
pages = None
beer = False

"""
The urls we will need to scrape to populate our database:
    bwsPopulateUrls = {'beer':'https://bws.com.au/beer/all-beer', 'wine':'https://bws.com.au/wine/all-wine', 'spirits':'https://bws.com.au/spirits/all-spirits'}

    liquorlandPopulateUrls = {'beer':'https://www.liquorland.com.au/beer?show=2000', 'wine':'https://www.liquorland.com.au/search?q=wine&show=2000', 'spirits':'https://www.liquorland.com.au/spirits?show=2000'}

    danmurphysPopulateUrls = {'beer':'https://www.danmurphys.com.au/beer/all', 'wine':'https://www.danmurphys.com.au/list/wine', 'spirits':'https://www.danmurphys.com.au/spirits/all'}

    firstchoiceliquorPopulateUrls = {'beer':'https://www.firstchoiceliquor.com.au/beer', 'wine':'https://www.firstchoiceliquor.com.au/search?q=wine', 'spirits':'https://www.firstchoiceliquor.com.au/spirits'}

"""

def search(searchTerms):
    """
    The master function that handles the complete pipeline of going from a search url to returning a final list of drink items.

    Args:
        url: the url we are scraping from
    Returns:
        drinksData: A list of Items which the data for each drink
    """
    # These are the base search page urls that we will add our search terms to to search
    searchUrls = list()
    global store
    if store == 'bws':
        if searchTerms == 'beer':
            searchUrls.append('https://bws.com.au/beer/all-beer')
            global beer
            beer = True
        elif searchTerms == 'wine':
            searchUrls.append('https://bws.com.au/wine/all-wine')
        elif searchTerms == 'spirits':
            searchUrls.append('https://bws.com.au/spirits/all-spirits')
        else:
            searchUrls.append("https://bws.com.au/search?searchTerm=" + str(searchTerms))
    elif store == 'liquorland':
        print("IMPLEMENT")
        quit()

    conn = create_connection()
    # Create a list of all the drinks data that we will scrape from all of the different liquor stores
    allDrinksData = list()

    # Get the search urls for each of the liquor sites for these search terms
    for searchUrl in searchUrls:
        # Add the search terms to the base search url to get the search url to scrape
        url = searchUrl
        print(url)
        # 1 & 2. Scrape the html for the search page and create beautifulsoup (generic). Then get the url for each drink result in the search (specific)
        itemsOnPages = getDrinks(url)

        if len(itemsOnPages) == 0:
            print("NO DRINK RESULTS FOUND AT " + url + ".")
        else:
            # 3 & 4. Follow each of the drink links utilising multiple threads to speed the process. Inside of each thread, once again scrape the page to a spoup (general), then get all the drink data from the drink page (specific)
            allDrinksData.extend(getDrinksData(itemsOnPages))

    conn.close()
    # TODO remove this is done in SQL, pointless wasting compute.
    # # Sort the drinks by efficiency descending
    if len(allDrinksData) == 0:
        print("NO DRINK RESULTS FOUND ACROSS ANY SUPPORTED SITES.")
    # else:
    #     allDrinksData = sortByEfficiency(allDrinksData)

    # Return the data for all of the drinks found across the liquor sites
    return allDrinksData

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
    # Sleep for a random number of seconds between requests (this is the minimum time between requests)
    # secs = randint(10, 20)
    secs = randint(1, 3)
    print("WAITING " + str(secs) + " SECONDS BEFORE SENDING ANOTHER REQUEST.")
    sleep(secs)

    # # Get an proxy ip from free-proxy-list
    # ua = UserAgent(cache=False, use_cache_server=False)
    # # Scrape a proxy IP from a free proxy site on the internet
    # proxies = []  # Will contain proxies [ip, port]
    # proxy_url = "https://free-proxy-list.net/"
    # # proxy_url = "https://www.sslproxies.org/"
    # proxies_req = Request(proxy_url)
    # print("GETTING A PROXY FROM " + proxy_url + " ...")
    # proxies_req.add_header('User-Agent', ua.random)
    # proxies_doc = urlopen(proxies_req).read().decode('utf8')
    # proxy_soup = BeautifulSoup(proxies_doc, 'html.parser')
    # proxies_table = proxy_soup.find(id='proxylisttable')
    # for row in proxies_table.tbody.find_all('tr'):
    #     proxies.append({
    #         'ip': row.find_all('td')[0].string,
    #         'port': row.find_all('td')[1].string
    #     })
    # proxy = proxies[0]['ip'] + ":" + proxies[0]['port']
    #
    #
    # # Configure options for the chrome web driver which is used as a headless browser to scrape html and render javascript for web pages. Also include the proxy's
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--proxy-server=' + proxy) # Add the proxy ip to the chrome options
    # driver = webdriver.Chrome(options=chrome_options)
    #
    # # Get the HTML from the given url
    # driver.get(url)
    #
    # soup = BeautifulSoup(driver.page_source, 'html.parser')


    # Setup the chromewebdriver
    # ua = UserAgent(cache=False, use_cache_server=False)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # # Scrape a proxy IP from a free proxy site on the internet
    # proxies = []  # Will contain proxies [ip, port]
    # # proxy_source = 'https://free-proxy-list.net/'
    # proxy_source = 'https://www.sslproxies.org/'
    # proxies_req = Request(proxy_source)
    # proxies_req.add_header('User-Agent', ua.random)
    # proxies_doc = urlopen(proxies_req).read().decode('utf8')
    # proxy_soup = BeautifulSoup(proxies_doc, 'html.parser')
    # proxies_table = proxy_soup.find(id='proxylisttable')
    # for row in proxies_table.tbody.find_all('tr'):
    #     proxies.append({
    #         'ip': row.find_all('td')[0].string,
    #         'port': row.find_all('td')[1].string
    #     })
    # PROXY = proxies[0]['ip'] + ":" + proxies[0]['port']
    # # PROXY = "51.158.111.242:8811"
    # print("FOUND PROXY " + str(PROXY) + " FROM " + proxy_source + ".")
    # # Add this proxy ip to the chromewebdriver arguments
    # chrome_options.add_argument('--proxy-server=' + PROXY)
    PROXY = "-"

    # Run the chromewebdriver to scrape with the given proxy
    driver = webdriver.Chrome(options=chrome_options)
    # We are now downloading the html from the given url
    print("DOWNLOADING AND RENDERING HTML FROM " + url + " ...")# " WITH PROXY URL " + PROXY + " ...")
    driver.get(url)

    # Put the scraped html into a beautifulsoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Return the soup
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
    # Create a new soup all results which holds a list of html soups of each of the results pages
    allPageSoups = list()

    # Detect the liquor site we are scraping from the url. This allows to extract the drinks using the correct strategies for the specific website.
    site = getSiteFromUrl(url)


    # Get a list of the html soups of all of the search pages
    if site == "bws":
        allPageSoups.extend(getAllSearchPagesBws(url))

    elif site == "liquorland":
        # TODO: Implement liquorland functionality
        allPageSoups.extend(getAllSearchPagesLiquorland(url))

    itemsOnPage = list()
    # Get the drink items based on what site is being scraped
    if site == "bws":
        itemsOnPage = getDrinksBws(allPageSoups)
    elif site == "liquorland":
        print("Sorry, Liquorland is not currently a supported site.")
        # TODO: Implement liquorland functionality - REMEMBER REPLACE WITH DRINK ITEMS
        # drinkUrls = getDrinksLiquorland(allPageSoups)
        # print("drinkUrls: " + str(drinkUrls))
    elif site == "danmurphys":
        print("Sorry, Dan Murphy's is not currently a supported site.")
        # TODO: Implement drink url extraction from dan murphys search page
    elif site == "firstchoiceliquor":
        print("Sorry, First Choice Liquor is not currently a supported site.")
        # TODO: Implement drink url extraction from first choice liquor search page

    # Print out how many drink urls were found on the page
    print("FOUND " + str(len(itemsOnPage)) + " DRINK URLS ON PAGE.")
    # Return the list of drink urls for us to individually scrape later on
    return itemsOnPage

def getDrinksData(itemsOnPage):
    """
    Function to get a list of drink data from a BeautifulSoup and return the data in a list

    Args:
        itemsOnPage: a list of item objects to the individual pages of the drinks found

    Returns: A list of drink data
    """
    # Now, the drink data must be extracted for each drink url found
    print('NOW EXTRACTING DRINKS DATA FROM DRINK URLS ...')

    # Create an empty list in which to store our drinks data (each drink will have its own Item object (see classItem) which will be added to the list)
    commonList = list()
    conn = create_connection()
    # Detect the liquor site we are scraping from the url. This allows to extract the drink data using the correct strategies for the specific website.
    site = getSiteFromUrl(itemsOnPage[0].link)

    # Get the data from the drink url pages using the functions for the current liquor site
    if len(itemsOnPage) == 0:
        # If there were no drinkUrls given, don't attempt to get data
        return commonList
    else:
        # If there are drinkUrls, however, get the data from them
        threads = 0
        _lock = Lock()
        with threadingPool.ThreadPoolExecutor(max_workers=1) as executor:
            for drink in itemsOnPage:
                if is_drink_in_table(conn, drink) == False:
                    url = drink.link
                    # Print out every time a new thread is initialised
                    print("INITIALISING THREAD " + str(threads) + "." + " LINK: " + str(url))

                    # Extract the drink data based on the site being scraped
                    if site == "bws":
                        # Retrieve drink data from bws format html
                        executor.submit(getDrinksDataBws, drink, commonList, _lock)
                    elif site == "liquorland":
                        # TODO: Implement liquorland functionality
                        print("Sorry, LiquorLand is not currently a supported site.")
                        # Extract the drink data from liquorland format drink page html
                        executor.submit(getDrinksDataLiquorland, url, commonList, _lock)
                    # Update how many threads we have initialised
                    threads += 1

                    # if threads == 20:
                    #     break
                else:
                    print('THIS DRINK IS PRESENT IN THE DATABASE: update thread')
                    update_drink(conn, drink, drink.price)

                # if threads == 20:
                #     break  # todo remove for more.

    # Return the drinksData
    return commonList

def sortByEfficiency(drinksData):
    """
    A function to sort a list of drinksData by descending efficiency
    """
    # Print our current status
    print("SORTING THE DRINKS DATA BY EFFICIENCY (DSC) ...")
    # Sort the list of drinksData by descending efficiency
    drinksData.sort(key = sortEighth, reverse = True)
    # Return the drinks data
    return drinksData

def sortEighth(val):
    """
    Function to return the eighth element of the two elements passed as the parameter
    """
    return val[8]

"""________________________________________SPECIFIC FUNCTIONS____________________________________________"""

"""___________________BWS__________________"""
def getAllSearchPagesBws(url):
    """
    A function to get the html soups of all the results pages for a search, given the url for the first page of results.
    If we are on bws, the results are stored on multiple pages, loaded one at a time, so we will check each page to see if there is a "show more results" button and if there is we will go the ne next results page (page number is determined by the page url)

    Args:
        url: the url of the first page of search results
    Returns:
        allPageSoups: a list of the html soups of all the results pages
    """

    # Create a new soup all results which holds a list of html soups of each of the results pages
    allPageSoups = list()

    # Start scraping at results page one
    currentPage = 1
    # Print what page of results we are currently loading
    print("LOADING PAGE " + str(currentPage) + " OF RESULTS")        # Get the html for the current page of results
    currentPageSoup = download(url + "?pageNumber=" + str(currentPage))
    # Add current page soup to list
    allPageSoups.append(currentPageSoup)
    # Get the html element for the "load more" button
    loadMoreButtonDiv = currentPageSoup.find('div', {'class':'progressive-paging-bar--container'})
    loadMoreButton = loadMoreButtonDiv.find('a', {'class':'btn btn-secondary btn--full-width ng-scope'})

    # quit if we have reached end of required pages
    global pages
    if currentPage == pages:
        return allPageSoups

    # While the html for the "load more" button is not null there is a next page
    while loadMoreButton != None:
        # Increment the number of the current page
        currentPage = currentPage + 1
        # Print what page of results we are currently loading
        print("LOADING PAGE " + str(currentPage) + " OF RESULTS")
        # Get the html for the current page of results
        currentPageSoup = download(url + "?pageNumber=" + str(currentPage))
        # Add current page soup to list
        allPageSoups.append(currentPageSoup)
        # Get the html element for the "load more" button
        loadMoreButtonDiv = currentPageSoup.find('div', {'class':'progressive-paging-bar--container'})
        loadMoreButton = loadMoreButtonDiv.find('a', {'class':'btn btn-secondary btn--full-width ng-scope'})

        # quit if we have reached end of required pages
        if currentPage == pages:
            return allPageSoups

    # Return the list containing all of html soup for every search page
    return allPageSoups


def getDrinksBws(soups):
    """
    Drink url extraction for bws

    Args:
        soup: a html soup of a liquor site search page
    Returns:
        drinkUrls: a list of urls for specific drink pages
    """
    # Create a new list to store the urls to each of the drinks
    itemsOnPage = list()
    # For each page of results, scrape all of the drink urls off of the page

    print("---------")
    global beer
    print("BEER = " + str(beer))
    if beer:
        for soup in soups:
            # Create a new list to store the drinks
            drinks = list()
            # Extract the drink cards from the search page soup
            drinksList = soup.find('div', {'class': 'center-panel-ui-view ng-scope'})
            drinks = drinksList.findAll('div', {'class': 'productTile'})
            for drink in drinks:
                print("--------")
                print('FOUND A CARD!')
                # Extract the urls to each individual drink page
                relativePath = drink.find('a', {'class': 'link--no-decoration'})['href']

                # Extract store, brand
                store = 'BWS'
                brand = drink.find('h2', {'class': 'productTile_brand ng-binding'}).text
                overname = drink.find('div', {'class': 'productTile_name ng-binding'}).text

                # Determine how many sections there are
                sections = drink.findAll('div', {'class':'trolley-controls_volume'})
                print("CARD HAS " + str(len(sections)) + " SECTIONS.")
                for section in sections:
                    name = section.find('span', {'class':'trolley-controls_volume_title ng-binding'}).text
                    name = name.strip()
                    name = name.split(" ")
                    name = name[0]
                    count = None
                    try:
                        count = section.find('small', {'class':'text-xs ng-binding ng-scope'}).text
                    except:
                        count = '(1)'
                    combinedName = overname + " - " + name + " " + count
                    print(">>", overname, "---", name, "###", count, "###")
                    price = section.find('span', {'class':'trolley-controls_volume_price'})
                    dollars = price.find('span', {'class':'ng-binding'}).text
                    cents = price.find('sup', {'class':'ng-binding'}).text
                    priceStr = str(dollars) + '.' + str(cents)
                    image = None
                    print("||", brand, "###", combinedName, "###", priceStr, "###")
                    entry = Item(store, brand, combinedName, None, priceStr, "https://bws.com.au" + relativePath, None, None, None,
                             None, image)
                    itemsOnPage.append(entry)
    else:
        for soup in soups:
            # Create a new list to store the drinks
            drinks = list()
            # Extract the drink cards from the search page soup
            drinksList = soup.find('div', {'class':'center-panel-ui-view ng-scope'})
            drinks = drinksList.findAll('div', {'class':'productTile'})
            for drink in drinks:
                # Extract the urls to each individual drink page
                relativePath = drink.find('a', {'class':'link--no-decoration'})['href']

                # Extract store, brand, name, type to check if stepping into page needed.
                store = 'BWS'
                brand = drink.find('h2', {'class':'productTile_brand ng-binding'}).text
                name = drink.find('div', {'class':'productTile_name ng-binding'}).text
                priceElement = drink.find('div', {'class': 'productTile_price ng-scope'})

                try:
                    dollar = priceElement.find('span', {'class': 'productTile_priceDollars ng-binding'}).text
                    cents = priceElement.find('span', {'class': 'productTile_priceCents ng-binding'}).text
                except AttributeError as e:
                    print(e)
                    print("at" + relativePath)
                    continue
                price = str(dollar) + '.' + str(cents)
                image = drink.find('img', {'class':'productTile_image'})['src']
                print(">>", brand, name, price)
                entry = Item(store, brand, name, None, price, "https://bws.com.au" + relativePath, None, None, None, None,
                             image)
                itemsOnPage.append(entry)
    # print(itemsOnPage)
    # print("QUIT")
    # quit()
    # Return the list containing the urls to each drink on each results page
    return itemsOnPage


def getDrinksDataBws(drink, commonList, _lock):
    """
    Thread function to control parsing of BWS drink details

    Args:
        drink: object to parse from
        commonList: the list of drink data that all threads store their results in
        _lock: some threading shit (ask Hamish I guess)

    Returns:
        none (simply adds the result to the common list, since this function is running within a multi-threaded environment)
    """
    # Print our current status
    print("GETTING DRINK DATA FROM A DRINK PAGE ...")

    # Get the html soup for the drink page
    url = drink.link
    soup = download(url)

    print(beer)
    if beer:
        # treat product as beer
        # find what is on the page
        print(0)
        canOrBottle = False
        pack = False
        case = False
        control = soup.find('div', {'class':'product-detail_controls-col'})
        print(0.25)
        products = control.findAll('span', {'class':'trolley-controls_volume_title ng-binding'})

        print(0.5)
        for product in products:
            if 'Can' in product.text or 'Bottle' in product.text:
                canOrBottle = True
            elif 'Pack' in product.text:
                pack = True
            elif 'Case' in product.text:
                case = True

        print(1)
        # Get the footer element containing all the rest of the details
        detailsRaw = soup.find('div', {'class': 'product-additional-details_container text-center ng-isolate-scope'})
        # Get the ul of details inside the element
        list = detailsRaw.find('ul', {'class': 'text-left'})
        # Get all the titles of the properties
        keys = list.findAll('strong', {'class': 'list-details_header ng-binding'})
        # Get all the values of the proverties
        values = list.findAll('span', {'class': 'pull-right list-details_info ng-binding ng-scope'})
        # Put the titles and values as K,V pairs into a dictionary
        details = dict()
        for x in range(0, len(keys)):
            details[keys[x].text] = values[x].text

        print(2)

        # Extract the product brand
        brand = details['Brand']
        old_name = drink.name

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

        print(3)

        # standard drinks float extract
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", details['Standard Drinks'])
        percent = re.findall(r"[-+]?\d*\.\d+|\d+", details['Alcohol %'])

        print(drink.name)
        split = drink.name.split("-")[-1]
        standard_drinks_parsed = None
        if "Can" in split or "Bottle" in split:
            print("a")
            standard_drinks_parsed = float(numbers[0])
            print(standard_drinks_parsed)
        elif "Pack" in split or "Case" in split:
            print("b")
            try:
                split_name = drink.name.split('-')[-1]
                drink_count_in_item = re.findall(r"\((\d+)\)", split_name)[0]
                standard_drinks_parsed = float(float(numbers[0]) * float(drink_count_in_item))
                print(split_name)
                print(drink_count_in_item)
                print(standard_drinks_parsed)
            except Exception as e:
                print(e)

        try:
            print(type(drink.price))
            print(drink.price)
        except Exception as e:
            print(e)

        # Find the price per standard by getting the number of standard drinks and dividing it by the price
        efficiency = standard_drinks_parsed / float(drink.price)
        print('x')
        # get image - slick track holds all images
        slick_track = soup.find('div', {'class':'slick-track'})
        print('y')
        # count number of images inside.
        images = soup.findAll('img', {'class':'product-image'})
        print(len(images))
        link_images = dict()
        i = 0
        for image in images:
            link_images[i] = image['src']
            i += 1

        for bruh in link_images.values():
            print(bruh)
            print("-----")

        print('z')

        print(5)

        try:
            image = None
            if not canOrBottle and not pack and case:
                # F F T
                if 'Case' in old_name:
                    image = link_images[0]
            elif not canOrBottle and pack and not case:
                # F T F
                if 'Pack' in old_name:
                    image = link_images[0]
            elif not canOrBottle and pack and case:
                # F T T
                if 'Pack' in old_name:
                    image = link_images[0]
                if 'Case' in old_name:
                    image = link_images[1]
            elif canOrBottle and not pack and not case:
                # T F F
                if 'Can' in old_name or 'Bottle' in old_name:
                    image = link_images[0]
            elif canOrBottle and not case and pack:
                # T F T
                if 'Can' in old_name or 'Bottle' in old_name:
                    image = link_images[0]
                if 'Pack' in old_name:
                    image = link_images[1]
            elif canOrBottle and case and not pack:
                # T T F
                if 'Can' in old_name or 'Bottle' in old_name:
                    image = link_images[0]
                if 'Case' in old_name:
                    image = link_images[1]
            elif canOrBottle and case and pack:
                # T T T
                if 'Can' in old_name or 'Bottle' in old_name:
                    image = link_images[0]
                if 'Case' in old_name:
                    image = link_images[1]
                if 'Pack' in old_name:
                    image = link_images[2]
        except Exception as e:
            print(e)
        print(6)

        print(details['Brand'])
        print(old_name)
        print(details['Liquor Style'])
        print(drink.price)
        print(url)
        print(float(size))
        print(float(percent[0]))
        print(standard_drinks_parsed)
        print(efficiency)
        print(image)

        # Put all of the details found for the drink into an Item object
        entry = Item("BWS", details['Brand'], old_name, details['Liquor Style'], drink.price, url, float(size),
                     float(percent[0]), standard_drinks_parsed, float(efficiency), image, None)

        print(7)

        # Print out the list of drink data
        print("<" + str(len(commonList)) + "> GOT DRINK DATA FOR: " + entry.name)

        # Thread safety
        _lock.acquire()
        commonList.append(entry)
        _lock.release()

    else:
        # Extract the name
        name = soup.find('div', {'class': 'detail-item_title'}).text
        # Extract the price
        priceElement = soup.find('span', {'class': 'trolley-controls_volume_price'})
        dollar = priceElement.find('span', {'class': 'ng-binding'}).text
        cents = priceElement.find('sup', {'class': 'ng-binding'}).text
        price = str(dollar) + '.' + str(cents)

        # Extract the product image link (the src attribute of the image)
        image = soup.find('img', {'class': 'product-image'})['src']

        # Get the footer element containing all the rest of the details
        detailsRaw = soup.find('div', {'class': 'product-additional-details_container text-center ng-isolate-scope'})
        # Get the ul of details inside the element
        list = detailsRaw.find('ul', {'class': 'text-left'})
        # TODO: Remove this debug statement
        # Get all the titles of the properties
        keys = list.findAll('strong', {'class': 'list-details_header ng-binding'})
        # Get all the values of the proverties
        values = list.findAll('span', {'class': 'pull-right list-details_info ng-binding ng-scope'})
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

        # standard drinks float extract
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", details['Standard Drinks'])
        percent = re.findall(r"[-+]?\d*\.\d+|\d+", details['Alcohol %'])
        # Find the price per standard by getting the number of standard drinks and dividing it by the price
        efficiency = float(numbers[0]) / float(price)

        # Put all of the details found for the drink into an Item object
        entry = Item("BWS", details['Brand'], name, details['Liquor Style'], price, url, float(size), float(percent[0]),
                     float(numbers[0]), efficiency, image, None)

        # Print out the list of drink data
        print("<" + str(len(commonList)) + "> GOT DRINK DATA FOR: " + entry.name)

        # Thread safety
        _lock.acquire()
        commonList.append(entry)
        _lock.release()


"""___________________LIQUORLAND__________________"""
def getAllSearchPagesLiquorland(url):
    """
    A function to get the html soups of all the results pages for a search, given the url for the first page of results. Since Liquorland allows us to simply show however many results we want, we just tell it to give us 2000 results (which is more than enough to show every item) in the url, so all the results will be on the first page.

    Args:
        url: the url of the first page of search results
    Returns:
        allPageSoups: a list of the html soups of all the results pages
    """
    # print("___HERE IS WHERE WE WERE GETTING THE ERROR___")
    soup = download(url)
    return soup

    # # Create a new soup all results which holds a list of html soups of each of the results pages
    # allPageSoups = list()
    #
    # # Start scraping at results page one
    # currentPage = 1
    # # Print what page of results we are currently loading
    # print("LOADING PAGE " + str(currentPage) + " OF RESULTS")        # Get the html for the current page of results
    # currentPageSoup = download(url)
    # # Add current page soup to list
    # allPageSoups.append(currentPageSoup)
    # # Get the html element for the page prev/next controls bar
    # nextButtonDiv = currentPageSoup.find('div', {'class':'pagination'})
    # # Get the button inside the div
    # nextButton = nextButtonDiv.find('a', {'title':'Next page'})
    # # Get the href property of the button
    # href = nextButton.get('href')
    # # print("### href: " + str(href) + " ###")
    #
    # # While the hmtl for the "load more" button is not null there is a next page
    # while href != None:
    #     # Increment the number of the current page
    #     currentPage = currentPage + 1
    #     # Print what page of results we are currently loading
    #     print("LOADING PAGE " + str(currentPage) + " OF RESULTS")        # Get the html for the current page of results
    #     currentPageSoup = download("https://www.liquorland.com.au" + str(href))
    #     # Add current page soup to list
    #     allPageSoups.append(currentPageSoup)
    #     # Get the html element for the page prev/next controls bar
    #     nextButtonDiv = currentPageSoup.find('div', {'class':'pagination'})
    #     # Get the button inside the div
    #     nextButton = nextButtonDiv.find('a', {'title':'Next page'})
    #     # Get the href property of the button
    #     href = nextButton.get('href')
    #     # print("### href: " + str(href) + " ###")
    #
    # # Return the list containing all of html soup for every search page
    # return allPageSoups

def getDrinksLiquorland(soups):
    """
    Drink url extraction for bws

    Args:
        soup: a html soup of a liquor site search page
    Returns:
        drinkUrls: a list of urls for specific drink pages
    """
    # Create a new list to store the urls to each of the drinks
    drinkUrls = list()
    # For each page of results, scrape all of the drink urls off of the page
    for soup in soups:
        # Create a new list to store the drinks
        drinks = list()
        # Extract the drink cards from the search page soup
        drinks = soup.findAll('div', {'class':'product-tile-wrapper'})
        for drink in drinks:
            # Extract the urls to each individual drink page
            relativePath = drink.find('a')['href']
            drinkUrls.append("https://www.liquorland.com.au" + relativePath)
    # Return the list containing the urls to each drink on each results page
    print("### HERE ARE ALL THE DRINK URLS: " + str(drinkUrls) + " ###")
    return drinkUrls

def getDrinksDataLiquorland(url, commonList, _lock):
    """
    Thread function to control parsing of BWS drink details

    Args:
        url: the url of the website for the specific drink product we are collecting the data for
        commonList: the list of drink data that all threads store their results in
        _lock: some threading shit (ask Hamish I guess)

    Returns:
        none (simply adds the result to the common list, since this function is running within a multi-threaded environment)
    """
    # Print our current status
    print("GETTING DRINK DATA FROM A DRINK PAGE ...")

    # Get the html soup for the drink page
    soup = download(url)
    # print("### " + soup + " ###")
    print(0)

    # Extract the name
    name = soup.find('h2', {'class':'sm title_r1'}).text
    print(1)
    print("NAME: " + name)

    # Extract the product brand
    brand = soup.find('h1', {'class':'sm brand_r1'}).text
    print(2)
    print("BRAND: " + brand)

    # Extract the price
    priceElementDiv = soup.find('div', {'class': 'pdp-bundle-price'})
    print("priceElementDiv: " + str(priceElementDiv))
    priceElement = priceElementDiv.find('span', {'class': 'price'})
    dollar = priceElement.text[1, -1]
    print("dollar: " + str(dollar))
    cents = priceElement.find('span', {'class': 'cents'}).text[1:]
    print("cents: " + str(cents))
    price = str(dollar) + '.' + str(cents)
    price = float(price)
    print(3)
    print("PRICE: " + str(price))

    # Extract the product image link (the src attribute of the image)
    imageElement = soup.find('figure', {'class': 'mz-figure mz-hover-zoom mz-no-expand mz-ready'})
    image = imageElement.find('img')['src']
    print(4)
    print("IMAGE: " + image)
    # quit()

    # Get the list containing all the rest of the details
    list = soup.find('ul', {'class':'pdp-detailsTable'})
    listelements = list.findAll('li')
    details = dict()
    for element in listelements:
        # Get all the titles of the properties
        key = element.find('div', {"class":"pdp-key"}).text
        keyformatted = key.strip()
        # Get all the values of the proverties
        value = element.find('div', {"class":"pdp-des"}).text
        valueformatted = value.strip()
        # Put the titles and values as K,V pairs into a dictionary
        details[keyformatted] = valueformatted

    # Extract the bottle volume from the name
    size = 0 # Size in litres
    # Forms we need to handle: "L" "Litre" "Litres" "mL"
    if (name.find("L ") != -1) or (name.find("Litre ") != -1) or (name.find("Litres ") != -1):
        # If the units were "L" or "Litre" or "Litres"
        before = name[0:units_index]
        before.strip() # Strip any spaces between the number and the units
        before.split(" ") # split the string into its individual words (the drink size value should be the last word)
        size = float(before[-1])
    elif (name.find("mL") != -1):
        # If the units were "mL"
        before = name[0:units_index]
        before.strip() # Strip any spaces between the number and the units
        before.split(" ") # split the string into its individual words (the drink size value should be the last word)
        size = float(before[-1]) / float(1000)
    else:
        # Else I haven't written enough else statements so i'm going to have to go and fix this
        print("UNRECOGNISED DRINK VOLUME FORMAT FOUND FOR LIQUORLAND")
    print(9999)
    print("SIZE: " + str(size))

    # size = 0
    # if details['Liquor Size'].find('mL') != -1:
    #     # measurement in mL
    #     strSize = details['Liquor Size'][0:len(details['Liquor Size']) - 2]
    #     size = int(strSize) / 1000
    # else:
    #     # measurement in L
    #     strSize = details['Liquor Size'][0:len(details['Liquor Size']) - 1]
    #     size = int(strSize)
    # print(5)

    # Get the number of standard drinks
    standard_drinks = float(details['Standard Drinks'])
    print(5)
    print("STANDARD DRINKS: " + str(standard_drinks))

    # Find the price per standard by getting the number of standard drinks and dividing it by the price
    efficiency = standard_drinks / price
    print(6)
    print("EFFICIENCY: " + str(efficiency))

    # Find the alcohol percentage
    alcohol_percentage = float(details['Alcohol Content'])
    print(7)
    print("ALCOHOL PERCENTAGE: " + str(alcohol_percentage))

    # Put all of the details found for the drink into an Item object
    # entry = Item("BWS", brand.text, name.text, price, "https://bws.com.au" + link['href'], details['Liquor Size'], details['Alcohol %'], details['Standard Drinks'], efficiency)
    entry = ["LIQUORLAND", brand, name, price, url, size, alcohol_percentage, standard_drinks, efficiency, image]
    print(8)
    print("ENTRY: " + str(entry))

    # # Extract the drinks data from the page html
    # detailsRaw = soup.find('ul', {'class':'pdp-detailsTable'})
    # listelements = detailsRaw.findAll('li')
    # details = dict()
    # for element in listelements:
    #     key = element.find('div', {"class":"pdp-key"}).text
    #     keyformatted = key.strip()
    #     value = element.find('div', {"class":"pdp-des"}).text
    #     valueformatted = value.strip()
    #     details[keyformatted] = valueformatted
    # efficiency = float(details['Standard Drinks']) / float(priceformatted)
    # # Create a new instance of the Item class and use it to store our drinksData
    # entry = Item("LiquorLand", brand.text, name.text, priceformatted, "https://liquorland.com.au" + link['href'], "0",
    #              details['Alcohol Content'], details['Standard Drinks'], efficiency)


    # Print out the list of drink data
    print("GOT DRINK DATA FOR: " + str(entry))

    print("QUITTING ...")
    quit()

    # Add the list of data for this drink to the list of drinksData
    commonList.append(entry)

    # Handle the closing of the thread
    _lock.acquire()
    _lock.release()


"""________________________________________MAIN FUNCTION____________________________________________"""


def main():
    # get arguments from the command line
    parser = argparse.ArgumentParser(description='scrape drinks from websites')
    parser.add_argument('store', type=str, help='bws or NOT IMPLEMENTED YET')
    parser.add_argument('category', type=str, help='beer or wine or spirits or SEARCH TERM')
    parser.add_argument('pages', type=int, help='how many pages to parse [0 for all]')
    args = parser.parse_args()

    global store
    store = args.store
    global category
    category = args.category
    global pages
    pages = args.pages

    data = search(category)  # scrape all the data for those search terms from bws
    conn = create_connection()
    dbhandler(conn, data, 'u')  # append new drinks to the database.


if __name__ == "__main__":
    main()
