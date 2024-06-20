import re
from typing import Union
import uuid
from bs4 import BeautifulSoup
import pandas as pd

from scraper.extractors.regex import REGEX_ANY_IN_BRACKETS, REGEX_ANY_IN_SQUARE_BRACKETS, REGEX_NO_U_SUFIX, REGEX_NON_NUMERIC, REGEX_ONLY_LETTERS


class FootballPlayerWikipediaExtractor():
    def extract(self, soup: BeautifulSoup) -> pd.Series:
        raw_data = self.__get_raw_data(soup)
        clean_data = self.__format_data(raw_data)

        return pd.Series(clean_data)

    def __get_raw_data(self, soup: BeautifulSoup) -> dict:
        raw_data = {}
        table = soup.find("table", {"class": "infobox infobox-table vcard"})

        if not table:
            return raw_data

        rows = table.find_all("tr")
        heading = soup.find("h1", {"id": "firstHeading"})
        player_name = heading.findChild("span").getText(strip=True)

        raw_data["name"] = player_name

        for row in rows:
            label = row.find("th", {"class": "infobox-label"})
            data = row.find("td", {"class": "infobox-data"})

            if not label or not data:
                continue

            label = self.__format_label(label.get_text(strip=True))
            raw_data[label] = data.get_text(strip=True).replace("\xa0", ' ')

            if row.find("td", {"class": "infobox-data-a"}) is None:
                continue

            club_name = self.__format_club_name(row.find(
                "td", {"class": "infobox-data-a"}).getText(strip=True))
            appearances = row.find(
                "td", {"class": "infobox-data-b"}).getText(strip=True)
            goals = row.find("td", {"class": "infobox-data-c"})
            if goals:
                goals = goals.getText(strip=True)

            if club_name and "current_team" in raw_data.keys() and club_name == raw_data["current_team"]:
                raw_data["appearances_in_current_club"] = appearances
                raw_data["goals_in_current_club"] = goals

            if club_name and "place_of_birth" in raw_data.keys():
                country_of_birth = self.__get_place_and_country_of_birth(
                    raw_data["place_of_birth"])[1]

                if country_of_birth in club_name or country_of_birth == club_name:
                    raw_data["national_team"] = club_name

        return raw_data

    def __format_data(self, raw_data: dict) -> dict:
        clean_data = {
            "PlayerID": str(uuid.uuid4()),
            "Name": self.__format_name(raw_data["name"]) if "name" in raw_data.keys() else None,
            "FullName": self.__format_full_name(raw_data["full_name"]) if "full_name" in raw_data.keys() else None,
            "DateOfBirth": self.__get_date_of_birth_and_age(raw_data["date_of_birth"])[0] if "date_of_birth" in raw_data.keys() else None,
            "Age": self.__get_date_of_birth_and_age(raw_data["date_of_birth"])[1] if "date_of_birth" in raw_data.keys() else None,
            "PlaceOfBirth": self.__get_place_and_country_of_birth(raw_data["place_of_birth"])[0] if "place_of_birth" in raw_data.keys() else None,
            "CountryOfBirth": self.__get_place_and_country_of_birth(raw_data["place_of_birth"])[1] if "place_of_birth" in raw_data.keys() else None,
            "Position": self.__remove_special_characters(raw_data["positions"]) if "positions" in raw_data.keys() else None,
            "CurrentClub": self.__format_name(raw_data["current_team"]) if "current_team" in raw_data.keys() else None,
            "NationalTeam": self.__format_national_team(raw_data["national_team"]) if "national_team" in raw_data.keys() else None,
            "NumberOfAppearancesInTheCurrentClub": self.__safe_cast_to_int(raw_data["appearances_in_current_club"]) if "appearances_in_current_club" in raw_data.keys() else None,
            "GoalsInTheCurrentClub": self.__safe_cast_to_int(raw_data["goals_in_current_club"].strip("()")) if "goals_in_current_club" in raw_data.keys() else None,
        }

        return clean_data

    def __format_label(self, label: str) -> str:
        return label.lower().replace(" ", "_").replace("(", "").replace(")", "")

    def __format_full_name(self, full_name: str) -> str:
        return re.sub(REGEX_ANY_IN_SQUARE_BRACKETS, "", full_name)    
    
    def __format_name(self, full_name: str) -> str:
        return re.sub(REGEX_ANY_IN_BRACKETS, "", full_name).strip(" ")
    
    def __format_national_team(self, club_name: str) -> str:
        return re.sub(REGEX_NO_U_SUFIX, "", club_name)

    def __get_date_of_birth_and_age(self, data_of_birth: str) -> tuple:
        result = re.findall(REGEX_ANY_IN_BRACKETS, data_of_birth)

        if len(result) == 2:
            date_of_birth, age = result
            age = int(self.__remove_non_numeric(age))

            return date_of_birth, age

        return None, None

    def __get_place_and_country_of_birth(self, place_of_birth: str) -> tuple:
        result = place_of_birth.split(",")
        city = result[0].strip(" ")
        country = self.__remove_special_characters(result[-1]).strip(" ")

        return ", ".join([city, country]), country

    def __remove_non_numeric(self, string: str) -> str:
        return re.sub(REGEX_NON_NUMERIC, "", string)

    def __format_club_name(self, club_name: str) -> str:
        return re.sub(REGEX_ANY_IN_BRACKETS, "", club_name).replace("→", "")

    def __remove_special_characters(self, string: str) -> str:
        return re.sub(REGEX_ONLY_LETTERS, "", string)

    def __safe_cast_to_int(self, value: str) -> Union[int, None]:
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
