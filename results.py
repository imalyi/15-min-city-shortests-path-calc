import category
from database import MongoDatabase
from data import ResidentialBuilding, PointOfInterest
import logging
from config import MAX_DISTANCE


class Result:
    def __init__(self, origin: ResidentialBuilding, destination: PointOfInterest, distance: float):
        self.destination = destination
        self.origin = origin
        self.distance = distance

    def __str__(self):
        return f"{str(self.origin)} - {str(self.destination)})"

    def is_distance_acceptable(self):
        if self.distance <= MAX_DISTANCE:
            return True
        return False


class Results:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.results = []
        self.db = MongoDatabase()

    def add(self, result: Result) -> None:
        if not result.is_distance_acceptable():
            return
        self.results.append(result)

    def _prepare_to_saving(self):
        prepared_data = {}
        for result in self.results:
            if prepared_data.get(result.origin.address.full) is None:
                prepared_data[result.origin.address.full] = result.origin.to_dict()
                prepared_data[result.origin.address.full]['points_of_interest'] = {}
                for main_category, sub_categories in category.get_categories().items():
                    prepared_data[result.origin.address.full]['points_of_interest'][main_category] = {}
                    for sub_category in sub_categories:
                        prepared_data[result.origin.address.full]['points_of_interest'][main_category][sub_category] = []

            for amenity in result.destination.amenity:
                if prepared_data[result.origin.address.full]['points_of_interest'].get(result.destination.amenity.main_amenity) is None:
                    prepared_data[result.origin.address.full]['points_of_interest'][result.destination.amenity.main_amenity] = {}
                if prepared_data[result.origin.address.full]['points_of_interest'][result.destination.amenity.main_amenity].get(amenity) is None:
                    prepared_data[result.origin.address.full]['points_of_interest'][
                        result.destination.amenity.main_amenity][amenity] = []
                poi = result.destination.to_dict()
                poi['distance'] = result.distance
                prepared_data[result.origin.address.full]['points_of_interest'][result.destination.amenity.main_amenity][amenity].append(poi)
        return list(prepared_data.values())

    def save_to_db(self):
        prepared_data = self._prepare_to_saving()
        self.logger.info(f"Start saving {len(self.results)} addresses")
        self.db.insert_many(prepared_data)
        self.logger.info(f"Done saving {len(self.results)} addresses")
        self.results.clear()
