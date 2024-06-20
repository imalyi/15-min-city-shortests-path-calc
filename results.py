from database import MongoDatabase
from data import ResidentialBuilding, PointOfInterest
import logging
from data import Distance
from categories.category import generate_dict_with_empty_categories


class Result:
    def __init__(self, residential_building: ResidentialBuilding):
        self.residential_building = residential_building
        self.pois = {}
        self._create_pois_structure()

    def _create_pois_structure(self):
        self.pois = generate_dict_with_empty_categories()

    def __str__(self):
        return f"{str(self.residential_building)}"

    @property
    def residential_building_full_address(self) -> str:
        return self.residential_building.address.full

    @property
    def get_residential_building(self) -> ResidentialBuilding:
        return self.residential_building

    def add_pois(self, poi: PointOfInterest, distance: Distance):
        if not self.pois.get(poi.amenity.main_amenity):
            self.pois[poi.amenity.main_amenity] = {}

        if not self.pois.get(poi.amenity.main_amenity).get(poi.amenity.sub_amenity):
            self.pois[poi.amenity.main_amenity][poi.amenity.sub_amenity] = []
        dict_poi = poi.to_dict()
        dict_poi.update({'distance': distance.distance})
        self.pois[poi.amenity.main_amenity][poi.amenity.sub_amenity].append(dict_poi)

    @property
    def to_dict(self) -> dict:
        data = self.residential_building.to_dict()
        data.update({
            'points_of_interest': self.pois
        })
        return data


class Results:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.results = {}
        self.db = MongoDatabase()

    def add(self, residential_building: ResidentialBuilding, poi: PointOfInterest, distance: Distance) -> None:
        if not distance.is_acceptable:
            return
        if residential_building.address.full not in self.results:
            self.results[residential_building.address.full] = Result(residential_building)
        self.results[residential_building.address.full].add_pois(poi, distance)

    def save_to_db(self):
        self.logger.info(f"Start saving {len(self.results)} addresses")
        prepared_data = []
        for _, result in self.results.items():
            prepared_data.append(result.to_dict)
        self.db.insert_many(prepared_data)
        self.logger.info(f"Done saving {len(self.results)} addresses")
        self.results.clear()
