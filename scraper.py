import argparse
from typing import List
from urllib.request import urlopen
from bs4 import BeautifulSoup

from scraper.consts import FOOTBALL_PLAYERS__EXTRACTOR_TYPE
from scraper.scrape_manager import ScrapeManager


parser = argparse.ArgumentParser(
    description='Scrape provided list of urls')
parser.add_argument("--csv_path", required=True,
                    help="csv file with list of URLs to be scraped")
parser.add_argument("--extractor_type", required=False,
                    default=FOOTBALL_PLAYERS__EXTRACTOR_TYPE, help="extractor to use to extract data from html")


def scrape(url_list: List, extractor_type) -> None:
    manager = ScrapeManager(url_list, extractor_type)
    manager.start()


if __name__ == "__main__":
    args = parser.parse_args()

    with open(args.csv_path, "r") as f:
        url_list = f.read().splitlines()
        # print(url_list)

    scrape(url_list, args.extractor_type)
