import json
from data import PointOfInterest, Amenity, Location, Address, BuildingName, Tags
import logging
import requests
from config import GEOCODINGAPI
import json
import time


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
                result = Location(res[0].get('boundingbox')[2], res[0].get('boundingbox')[0])
                self.logger.info(f"For {address} found {result}")
                return result
            except IndexError:
                self.logger.warning(f"Cant find {address}")
        else:
            time.sleep(1)
            return self.get_street(address)


class AddressToCoordinates:
    def __init__(self, residential_buildings):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.residential_buildings = residential_buildings
        self.data = {}
        self.geocoding_api = GeoCodingAPI()
        self.create()

    def create(self):
        i = 0
        for building in self.residential_buildings:
            city = building.address.city
            street = (building.address.street + ' ' + building.address.housenumber)
            i += 1
            if city not in self.data:
                self.data[city] = {}

            if street not in self.data[city]:
                self.data[city][street] = building
        self.logger.info(f"Loaded {i} addresses from OSM")

    def get(self, city: str, street: str) -> Location:
        res = self.data[city].get(street)
        if res:
            location = res.location
            self.logger.info(f"For {street}, {city} found {location}")
        if not res:
            location = self.geocoding_api.get_street(f"{city}, {street}")
        return location


class TrojmiastoPlPointsOfInterest:
    def __init__(self, address_to_coordinates):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.read_data()
        self.address_to_coordinates = address_to_coordinates
        self._data = []
        self.poi_iterator = iter(self._data)
        self.find_address()

    def read_data(self):
        with open("poi_data/data_test.json", "r") as f:
            self.raw_data = json.loads(f.read())

    def find_address(self):
        i = 0
        not_found_addresses = []
        for row in self.raw_data:
            try:
                street = row.get('address').get('street').split("/")[0]
            except IndexError:
                street = row.get('address').get('street')
            for from_, to in REPLACE:
                street = street.replace(from_, to)

            street = street.split("/")[0]
            location = self.address_to_coordinates.get(city=row.get('address').get('city'), street=street)
            if location:
                amenities = Amenity(**row.get('categories'))
                address = Address(street, row.get('address').get('city'))
                name = BuildingName(row.get('name'))
                poi = PointOfInterest(amenities, address, location, name)
                self._data.append(poi)
                self.logger.info(f"Found {poi}")
            else:
                self.logger.warning(f"For data {row} cant find {street}")
                i += 1
                not_found_addresses.append(street)
        self.logger.warning(f"Cant find {i} addresses: {not_found_addresses}")

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.poi_iterator)
        except StopIteration:
            self.poi_iterator = iter(self._data)
            raise StopIteration

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

