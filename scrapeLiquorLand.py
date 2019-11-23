from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures as threadingPool
from classItem import Item, ItemCollection
import logging
from fake_useragent import UserAgent
import random
from urllib.request import Request, urlopen


def download_liquorland(url, target_filename, filename_extension, LiqourLandList):
    """
    Function to parse BWS site (circa November 2019) and return all drinks
    """
    soup = BeautifulSoup(url, 'html.parser')
    specials = soup.findAll('div', {'class':'product-tile-wrapper update-specials-border'})
    drinks = soup.findAll('div', {'class': 'product-tile-wrapper'})

    print('LiqLand SCRAPED normal:' + str(len(drinks)))
    print('LiqLand SCRAPED specials: ' + str(len(specials)))

    threads = 0
    with threadingPool.ThreadPoolExecutor(max_workers=3) as executor:
        for item in drinks:
            #print("INIT_THREAD[" + str(threads) + "]")
            threads += 1
            executor.submit(item_thread_liquorland, item, list)

        for item in specials:
            #print("INIT_THREAD[" + str(threads) + "]")
            threads += 1
            executor.submit(item_thread_liquorland, item, list)


def item_thread_liquorland(item, list):
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
