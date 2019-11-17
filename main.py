from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def download(url, target_filename, filename_extension):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # items = driver.find_elements_by_class_name('productTile')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    drinks = soup.findAll('div', {'class':'productTile'})
    print('found ' + str(len(drinks)))

    for item in drinks: 
        print("--------")
        # brand
        brand = item.find('h2', {'class':'productTile_brand ng-binding'})        
        print(brand.text)

        # name
        name = item.find('div', {'class':'productTile_name ng-binding'})        
        print(name.text)

        # price
        dollar = item.find('span', {'class':'productTile_priceDollars ng-binding'})  
        cents = item.find('span', {'class':'productTile_priceCents ng-binding'})  
        print(str(dollar.text) + '.' + str(cents.text))

def main():
    download("https://bws.com.au/spirits/vodka", "contents", "txt")

if __name__ == '__main__':
    main()

    