from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures as threadingPool
from classItem import Item, ItemCollection
import logging

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
    # url e.g. "https://bws.com.au/search?searchTerm="vodka"
    domain = url.partition(".")[0]
    # domain e.g. "https://bws"
    liquorSite = domain[8:]
    # liquorSite e.g. "bws"
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
    # print('SCRAPED ' + str(len(drinks)))

    # Create an empty list in which to store our drinks data (each drink will have its own Item object (see classItem) which will be added to the list)
    drinksData = {}

    # Get the drink data for each drink profile we collected
    # Threading stuff basically executes multiple copies item_thread_XXX(item) concurrently
    threads = 0
    with threadingPool.ThreadPoolExecutor() as executor:
        for item in drinks:
            print("INIT_THREAD[" + str(threads) + "]")
            threads += 1
            # Execute the correct item_thread function based on the given liquorSite
            if liquorSite == "bws":
                # Run item_thread_bws(item)
                drinksData.append(executor.submit(item_thread_bws, item))
            else if liquorSite == "liquorland":
                # Run item_thread_liquorland(item)
                drinksData.append(executor.submit(item_thread_liquorland, item))

    # Return the drinksData
    return drinksData

def item_thread_bws(item):
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
    return entry

def item_thread_liquorland(item, list):
    """
    Thread function to control parsing of liquorland drink details
    """
    # brand
    brand = item.find('div', {'class': 'product-tile-brand'})
    # name
    name = item.find('div', {'class': 'product-tile-des'})
    # price
    pricespan = item.find('div', {'class': 'price-bundle-new'})
    dollar = pricespan.find('span', {'class': 'price'})
    # link
    linkdiv = item.find('div', {'class':'product-tile-brand'})
    link = linkdiv.find('a')
    pricewithsymbols = " ".join(dollar.text.splitlines())
    priceformatted = pricewithsymbols.split('$')[1]


    # alcohol content
    ua = UserAgent(cache=False, use_cache_server=False)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    proxies = []  # Will contain proxies [ip, port]
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req = Request('https://free-proxy-list.net/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')
    proxy_soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = proxy_soup.find(id='proxylisttable')
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip': row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    PROXY = proxies[0]['ip'] + ":" + proxies[0]['port']
    print(PROXY)
    chrome_options.add_argument('--proxy-server=' + PROXY)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.liquorland.com.au" + link['href'])

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    detailsRaw = soup.find('ul', {'class':'pdp-detailsTable'})
    listelements = detailsRaw.findAll('li')
    details = dict()
    for element in listelements:
        key = element.find('div', {"class":"pdp-key"}).text
        keyformatted = key.strip()
        value = element.find('div', {"class":"pdp-des"}).text
        valueformatted = value.strip()
        details[keyformatted] = valueformatted


    efficiency = float(details['Standard Drinks']) / float(priceformatted)

    entry = Item("LiquorLand", brand.text, name.text, priceformatted, "https://liquorland.com.au" + link['href'], "0",
                 details['Alcohol Content'], details['Standard Drinks'], efficiency)
    print("FOUND: " + entry.brand + entry.name + " " + priceformatted + " " + str(efficiency))
    return entry
