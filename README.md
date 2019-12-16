# CompareTheBrew.com.au
🍺🍺 Get the cheapest drink possible, and make money doing so 🍺🍺

## Setup:
```bash
$ bash setup.sh
```

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

## TODO
- [ ] finalise image displays [nearly done, files are present but waiting on mcost and alex]
- [ ] beer parsing for bws. find an efficient approach? 

- [ ] Setup hosting on aws
  - [ ] Setup hosting on aws
  - [ ] Scheduling time-staggered scraping of liquor sites (using Cron most likely)
  - [ ] Buy a Domain and DNS

___
### Made Possible by:
Hamish Bultitude
Matt Costello
Alex Nicholson
Stekaz
