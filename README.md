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
| Competed Working Stores: | Under Development Stores:       | Future Development Stores: |
| ------------------------- | ------------------------------- | -------------------------- |
| BWS                       | First Choice Liquor (Nicholson) | Vintage Cellars            |
| Liquorland                | Dan Murphy's (Hamish?)          | Celebrations               |
|                           |                                 | AMEEEERICAAAA!             |

- [ ] Move to next page of search results if multiple pages
- [ ] Remove search query dependency (waiting on mcost)
- [ ] thread safety

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

- [ ] Database
  - [ ] Basic datavase storing
  - [ ] Storing scrape results to the database
  - [ ] Taking queries to the database from users and sending the data to the frontend

- [ ] Operations
  - [ ] Hosting web server off of personal computer
  - [ ] Scheduling time-staggered scraping of liquor sites (using Cron most likely)
  - [ ] Buy a Domain and DNS
  - [ ] Setup server hosting in the cloud on free trial program

___
### Made Possible by:
Alex Junner
Hamish Bultitude
Matt Costello
Alex Nicholson
