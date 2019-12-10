# CompareTheBrew.com.au
🍺🍺 Get the cheapest drink possible 🍺🍺

## Setup:
```bash
$ bash setup.sh
```

## Run:
```bash
$ python3 main.py
```

## Dependancies (installed in setup)
- BeautifulSoup4
- Selenium
- ChromeWebDriver (headless)
___

## TODO
- [x] Move to next page of search results if multiple pages
- [x] Remove search query dependency (waiting on mcost)
- [x] thread safety

- [ ] Frontend
  - [x] Design Mockup
  - [x] HTML Scaffold
  - [x] CSS Styling
  - [ ] Sending inputs to backend

- [ ] Backend
  - [x] Scraping
    - [x] Single Site Scraping Script (BWS)
    - [x] Optimisation
    - [x] Expansion to other Australian Liquor Stores (Liquorland, Dan Murphy's, First Choice Liquor)
  - [ ] Expansion to American Liqour Stores

- [x] Database
  - [x] Basic database storing
  - [x] Storing scrape results to the database
  - [x] Taking queries to the database from users and sending the data to the frontend

- [] Operations
  - [x] Hosting web server off of personal computer
  - [ ] Scheduling time-staggered scraping of liquor sites (using Cron most likely)
  - [ ] Buy a Domain and DNS
  - [x] Setup server hosting in the cloud on free trial program

___
### Made Possible by:
Hamish Bultitude
Matt Costello
Alex Nicholson
Stekaz
