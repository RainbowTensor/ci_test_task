## C&I Test Task
This repo contains code for C&I test task. Project consists of python web scraper, csv import script and SQL queries.

### Setup
Clone the repo and install dependencies:
```bash
pip install -r requirements.txt
```
Then run setup script that will create SQLite database together with initial table. Table definition can be found in /database/queries/setup_table.sql
```bash
python3 setup_db.py
```
### Run scraper
```bash
python3 scraper.py --csv_path ./path_to_urls.csv
```
Specify path to the file containing list of URLs from which to scrape. Scraper will output the scraped data in output.csv file in project root.

### Import csv file
To import csv file, run the following script:
```bash
python3 import.py --csv_path ./path_to_csv.csv
```
Specify path to csv file e.g. ./playersData.csv for import of provided data or ./output.csv for scraped data.