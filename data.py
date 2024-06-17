import logging
import json
from geometry import Geometry

class Location:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}; {self.y})"

    def __repr__(self):
        return f"Location({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Location):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y,))

    def to_dict(self):
        return [self.x, self.y]


class Address:
    def __init__(self, street, city, housenumber = None):
        self.street = street
        self._housenumber = housenumber
        self.city = city

    @property
    def housenumber(self):
        if self._housenumber:
            return self._housenumber
        return ""
    @property
    def full(self) -> str:
        if self.housenumber:
            return f"{self.street} {self.housenumber}, {self.city}"
        else:
            return f"{self.street}, {self.city}"

    @property
    def is_valid(self) -> bool:
        if self.street is not None and self.city is not None:
            return True
        return False

    def __str__(self):
        return self.full

    def __repr__(self):
        return self.full

    def to_dict(self) -> dict:
        return {
            'city': self.city,
            'housenumber': self.housenumber,
            'street': self.street,
            'full': self.full
        }

    def __eq__(self, other):
        if isinstance(other, Address):
            return (self.street, self.housenumber, self.city) == (other.street, other.housenumber, other.city)
        return False

    def __hash__(self):
        return hash((self.street, self.housenumber, self.city))


class BuildingName:
    def __init__(self, name: str) -> None:
        if name is None:
            name = 'unknown'
        self.name = name.strip()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, BuildingName):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)


class ResidentialBuilding:
    def __init__(self, address: Address, location: Location, geometry: Geometry):
        self.address = address
        self.location = location
        self.geometry = geometry
        self.id_ = None
        self.data_source = 'https://www.openstreetmap.org'

    def to_dict(self):
        return {
            'address': self.address.to_dict(),
            'location': self.location.to_dict(),
            'source': self.data_source,
            'geometry': self.geometry.to_dict()
        }

    def __str__(self):
        return f"{self.address}"

    def __eq__(self, other):
        if isinstance(other, ResidentialBuilding):
            return (self.address, self.location) == (other.address, other.location)
        return False

    def __hash__(self):
        return hash((self.address, self.location))


class Amenity:
    def __init__(self, main: str, sub: str) -> None:
        self.main = main
        self.sub = sub

    @property
    def main_amenity(self):
        return self.main

    @property
    def sub_amenity(self):
        return self.sub
    
    def __str__(self):
        return ', '.join([self.main, "->", self.sub])

    def __repr__(self):
        return ', '.join([self.main, "->", self.sub])

    def __eq__(self, other):
        if isinstance(other, Amenity):
            return self.main == other.main and self.sub == other.sub
        return False

    def __hash__(self):
        return hash(str(self))

    def __iter__(self):
        self._index = 0
        return self


class Tags:
    def __init__(self, tags: str) -> None:
        try:
            self.tags = json.loads(tags)
        except Exception:
            logging.warning(f"Error convert {tags} to dict", exc_info=True)
            self.tags = {}

    def to_dict(self):
        return self.tags

    def __str__(self):
        return json.dumps(self.tags)

    def __repr__(self):
        return json.dumps(self.tags)

    def __eq__(self, other):
        if isinstance(other, Tags):
            return self.tags == other.tags
        return False

    def __hash__(self):
        return hash(json.dumps(self.tags))


class PointOfInterest:
    def __init__(self, amenity: Amenity, address: Address, location: Location, name: BuildingName, tags: Tags=None):
        self.address = address
        self.location = location
        self.tags = tags
        self.amenity = amenity
        self.name = name
        self.id_ = None
        self.data_source = 'https://www.openstreetmap.org'

    def to_dict(self) -> dict:
        data = {
                'name': str(self.name),
                'location': self.location.to_dict(),
        }
        if self.tags:
            data['tags'] = self.tags.to_dict()
        if self.address.is_valid:
            data['address'] = self.address.to_dict()
        return data

    @property
    def is_allowed(self) -> bool:
        return self.amenity.is_allowed()

    def __eq__(self, other):
        if isinstance(other, PointOfInterest):
            return (
                self.address == other.address and
                self.location == other.location and
                self.tags == other.tags and
                self.amenity == other.amenity and
                self.name == other.name
            )
        return False

    def __hash__(self):
        return hash((
            self.address,
            self.location,
            self.tags,
            self.amenity,
            self.name
        ))

    def __str__(self):
        return f"{self.name}-{self.address}-{self.tags}"
