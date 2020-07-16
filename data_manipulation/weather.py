import json

import requests
from bs4 import BeautifulSoup


class WeatherAndPollutionData(object):

    def __init__(self, country="italy", region="sardinia", city="cagliari"):
        self.base_url = "https://www.iqair.com"
        url = self.base_url + "/" + country + "/" + region + "/" + city
        page = requests.get(url)
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def actual_weather(self):
        try:
            data = {}

            table_rows = self.soup.find_all('div', class_='weather__detail')[0].next_element.next_sibling.contents[
                0].contents

            for row in table_rows:
                data[row.contents[0].text] = row.contents[1].text if row.contents[0].text != 'Wind' else row.contents[
                    1].text.replace("mp", "km")

            data['icon'] = self.base_url + self.soup.find_all('img', class_='weather__icon')[0].attrs['src']

            #f = "default_weather.json"
            #with open(f, 'w') as outfile:
            #    json.dump(data, outfile)

            return data
        except Exception as e:
            try:
                f = "data_manipulation/default_weather.json"
                data = json.load(open(f))
                return data
            except:
                return None

    def actual_pollution(self):
        try:
            data = {}
            icon_pollution = self.soup.find_all('div', class_='aqi-overview__summary aqi-green')[0].contents[1].attrs['src']
            table_row = self.soup.find_all('table', class_='aqi-overview-detail__main-pollution-table')[0].contents

            key_row = [e.text for e in table_row[0].contents[0].contents]
            values_row = [e.text for e in table_row[1].contents[0].contents]

            for el in zip(key_row, values_row):
                data[el[0]] = el[1]

            data['icon'] = self.base_url + icon_pollution

            #f = "default_pollution.json"
            #with open(f, 'w') as outfile:
            #    json.dump(data, outfile)

            return data
        except Exception as e:
            try:
                f = "data_manipulation/default_pollution.json"
                data = json.load(open(f))
                return data
            except:
                return None





WeatherAndPollutionData().actual_pollution()
