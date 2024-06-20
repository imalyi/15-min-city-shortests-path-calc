import json
from data import PointOfInterest, Amenity, Location, Address, BuildingName
import logging
import os
from config import JSON_DATA_PATH

class PointsOfInteresJsonLoader:
    # Load data from multiple json files.
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._data = []
        self.poi_iterator = iter(self._data)
        self.load_data()

    def read_file_list(self):
        return os.listdir(JSON_DATA_PATH)

    def read_data(self, filename: str) -> list:
        with open(f"{JSON_DATA_PATH}/{filename}", "r") as f:
            raw_json = f.read()
        try:
            return json.loads(raw_json)
        except json.decoder.JSONDecodeError:
            self.logger.error(f"Error load json file {filename}", exc_info=True)
            return []

    def load_data(self):
        i = 0
        for file in self.read_file_list():
            self.logger.info(f"Reading file {file}")
            for poi_in_json in self.read_data(file):
                amenities = Amenity(**poi_in_json.get('categories'))
                location = Location(**poi_in_json.get('location'))
                address = Address(**poi_in_json.get('address'))
                name = BuildingName(poi_in_json.get('name'))
                poi = PointOfInterest(amenities, address, location, name)
                self._data.append(poi)
                i += 1
        self.logger.info(f"Found {i} pois in {JSON_DATA_PATH}")

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

t = PointsOfInteresJsonLoader()