import logging
import requests
import json
import os
from config import JSON_DATA_PATH

GEOCODINGAPI = '65a53f8bc1037243302270wem37f6cb'


REPLACE = [
    ['al.', 'Aleja'],
    ['marsz.', 'marszałka'],
    ['gen.', 'generała'],
    ['pl.', 'plac'],
    ['adm.', 'admirała'],
    ['płk.', 'pułkownika'],
    ['ks.', 'księdza'],
    ['prof.', 'profesora'],
    ['kmdr.', 'komandora'],
]

class GeoCodingAPI:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_street(self, address: str):
        url = f"https://geocode.maps.co/search?q={address}&api_key={GEOCODINGAPI}"
        response = requests.get(url)
        if response.status_code == 200:
            res = json.loads(response.text)
            try:
                result = (float(res[0].get('boundingbox')[0]), float(res[0].get('boundingbox')[2]))
                self.logger.info(f"For {address} found {result}")
                return result
            except IndexError:
                self.logger.warning(f"Cant find {address}")
        else:
            return self.get_street(address)


def add_coorinates():
    geocodingapi = GeoCodingAPI()
    files = os.listdir(JSON_DATA_PATH)
    for file in files:
        print(f"Handling file {file}")
        data_with_location = []
        with open(f"{JSON_DATA_PATH}/{file}") as f:
            data = json.loads(f.read())
        print("found items: ", len(data))
        i = 0
        for row in data:
            i += 1
            if row.get('location'):
                continue
            try:
                street = row.get('address').get('street').replace("ul. ", "")
                latitude, longitude = geocodingapi.get_street(f"{street}, {row.get('address').get('city')}")
            except TypeError:
                print(f"cant find {row.get('address')}")
                continue
            row.update({"location":{"latitude": latitude, "longitude": longitude}})
            data_with_location.append(
                row
            )
            if i % 1000 == 0:
                print(i)
        with open(f"{JSON_DATA_PATH}/add_location_{file}.json", "w") as f:
            f.write(json.dumps(data_with_location, indent=4, ensure_ascii=False))


add_coorinates()