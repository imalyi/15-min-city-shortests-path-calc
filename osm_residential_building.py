import logging
from data import Address, Location, ResidentialBuilding


class OSMResidentialBuildings:
    def __init__(self, osm):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.osm = osm
        self._data = self.get_buildings()
        self.buildings_iterator = iter(self._data)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.buildings_iterator)
        except StopIteration:
            self.buildings_iterator = iter(self._data)
            raise StopIteration

    def get_buildings(self) -> list:
        logging.info("Start loading buildings info..")
        buildings = self.osm.get_buildings()
        buildings_list = []
        for index, building in buildings.iterrows():
            address = Address(building.get('addr:street', None), building.get('addr:city', None), building.get('addr:housenumber', None))
            location = Location(building.geometry.centroid.x, building.geometry.centroid.y)
            if address.is_valid:
                buildings_list.append(ResidentialBuilding(address, location))
        logging.info(f"Collected {len(buildings_list)} residential buildings")
        return buildings_list

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

