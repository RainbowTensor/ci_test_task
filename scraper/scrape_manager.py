from typing import List
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

from scraper.consts import EXTRACTOR_REGISTRY


class ScrapeManager():
    def __init__(self, url_list: List, extractor_type: str) -> None:
        self.url_list = url_list
        self.extractor_type = extractor_type

        if not extractor_type in EXTRACTOR_REGISTRY.keys():
            raise Exception(
                f"Extractor class for extractor type {extractor_type} does not exist.")

        data_extractor_class = EXTRACTOR_REGISTRY[extractor_type]
        self.data_extractor = data_extractor_class()

    def start(self):
        series = []
        for url in self.url_list:
            print(url)
            try:
                soup = self.__open_and_parse_url(url)
            except:
                continue

            result_series = self.data_extractor.extract(soup)
            if result_series.count() <= 1:
                continue

            result_series["URL"] = url
            result_series["ScrapingTimestamp"] = datetime.now()

            series.append(result_series)

        result_df = pd.DataFrame(series)
        result_df = result_df.to_csv("./output.csv", index=False, sep=";")

        return

    def __open_and_parse_url(self, url: str) -> BeautifulSoup:
        page = urlopen(url)
        html = page.read().decode("utf-8")

        return BeautifulSoup(html, "html.parser")
