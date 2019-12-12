from lxml.html import fromstring
import requests
# from itertools import cycle
import traceback

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('q//tbody/tr'): #[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


#If you are copy pasting proxy ips, put in the list below
#proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080']
proxies = get_proxies()
proxy_pool = list(proxies)
print("LENGTH: " + str(len(proxy_pool)))

url = 'https://httpbin.org/ip'
# for i in range(1,11):
#     #Get a proxy from the pool
#     proxy = next(proxy_pool)
#     print("Checking proxy #%d"%i)
#     try:
#         response = requests.get(url,proxies={"http": proxy, "https.png": proxy}, timeout=3)
#         print(response.json())
#     except:
#         #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
#         #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
#         print("Skipping. Connnection error")
working_proxy_found = False
i = 0
while (working_proxy_found == False) and (i < len(proxies)):
    #Get a proxy from the pool
    proxy = proxy_pool[i]
    print("Checking proxy #%d"%i)
    try:
        response = requests.get(url,proxies={"http": proxy, "https.png": proxy}, timeout=3)
        response_string = str(response.json())
        working_proxy_found = True
    except:
        #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
        #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
        print("Skipping. Connnection error")
    i = i+1
print("We got one : " + response_string)
