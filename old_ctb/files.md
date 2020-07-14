# FILES - a short story
### By Hamish Bultitude

There are two main files to this project, `scrape.py` and `app.py`. 
 - `scrape` is the file that is run to fill the drinks database with drink files & update it. This occurs at the very start for each website and continues every 24 hours using a `cron` job on AWS. 
 - `app` is the file controlling the running of flask - thus allowing the hosing of the website. 
 
There are other misc files to the project too!
 - `scripts/classItem.py` includes the class that each drink will be stored within.
 - `scripts/databaseHandler.py` includes all SQL statements for creation of tables, along with insertion and updating data.
