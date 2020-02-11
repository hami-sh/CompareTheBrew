# CompareTheBrew.me
🍺🍺 Get the cheapest drink possible across all Aussie alcoholic vendors 🍺🍺

## Setup:
```bash
$ bash setup.sh
```

## API Queries:
`http://comparethebrew.me/api?term=TERM&order=score_desc`


## Run:
#### SCRAPING
###### locally
```bash
$ python3 scrape.py [store] [category] [# pages]
```
-> store (bws, others not implemented yet)

-> category (beer, wine, spirits)

-> # pages (0 for all)

###### lightsail instance (done automatically via `cron`)
```bash
$ pipeline.sh
```


#### WEB SERVER
###### locally
```bash
$ python3 app.py
```
###### lightsail instance
```bash
$ ./startserver.sh
```
```bash
$ ./seeserver.sh
```
```bash
$ ./killserver.sh
```

## Dependancies (installed in setup)
- BeautifulSoup4
- Selenium
- ChromeWebDriver (headless)
- flask
- sqlite3

___
### Made Possible by:
Hamish Bultitude

Matt Costello

Alex Nicholson
