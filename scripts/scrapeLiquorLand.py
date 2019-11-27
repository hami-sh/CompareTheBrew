from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures as threadingPool
from classItem import Item, ItemCollection
import logging
from fake_useragent import UserAgent
import random
from urllib.request import Request, urlopen

def item_thread_liquorland(item, commonList, _lock):
    """
    Thread function to control parsing of BWS drink details
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

    # Setup the chromewebdriver
    ua = UserAgent(cache=False, use_cache_server=False)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Scrape a proxy IP from a free proxy site on the internet
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
    # Run the chromewebdriver to scrape with the given proxy
    chrome_options.add_argument('--proxy-server=' + PROXY)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.liquorland.com.au" + link['href'])

    # Put the scraped html into a beautifulsoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract the drinks data from the page html
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
    # Create a new instance of the Item class and use it to store our drinksData
    entry = Item("LiquorLand", brand.text, name.text, priceformatted, "https://liquorland.com.au" + link['href'], "0",
                 details['Alcohol Content'], details['Standard Drinks'], efficiency)
    # Print the alcohol data to the console
    print("FOUND: " + entry.brand + entry.name + " " + priceformatted + " " + str(efficiency))

    # Add the drinks data to the commmon list whose reference was passed into this thread
    _lock.acquire()
    commonList.append(entry)
    _lock.release()
