import logging
import json

class Geometry:
    def __init__(self, geometry) -> None:
        self.geometry = geometry

    @property
    def coords(self):
        """Extract coordinates from the building geometry."""
        if self.geometry.geom_type == 'Polygon':
            return [list(self.geometry.exterior.coords)]
        elif self.geometry.geom_type == 'MultiPolygon':
            coords = []
            for poly in self.geometry.geoms:
                coords.extend(list(poly.exterior.coords))
            return [coords]
        elif self.geometry.geom_type == 'LineString':
            return [list(self.geometry.coords)]
        else:
            return []
        
    def to_dict(self):
        return self.coords
    
    def __str__(self):
        return str(len(self.polygon))
    
class Location:
    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"({self.latitude}; {self.longitude})"

    def __repr__(self):
        return f"Location({self.latitude}, {self.longitude})"

    def __eq__(self, other):
        if isinstance(other, Location):
            return self.latitude == other.latitude and self.longitude == other.longitude
        return False

    def __hash__(self):
        return hash((self.latitude, self.longitude,))

    def to_dict(self):
        return [self.latitude, self.longitude]


class Address:
    def __init__(self, street: str, city: str, postcode: str = None):
        self.street = street
        self.city = city
        self.postcode = postcode
    
    @property
    def full(self) -> str:
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
            'street': self.street,
            'full': self.full,
            'postcode': self.postcode
        }

    def __eq__(self, other):
        if isinstance(other, Address):
            return (self.street, self.city) == (other.street, other.housenumber, other.city)
        return False

    def __hash__(self):
        return hash((self.street, self.city))


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
        data['address'] = self.address.to_dict()
        return data

    def __eq__(self, other):
        if isinstance(other, PointOfInterest):
            return (
                self.address == other.address and
                self.location == other.location and
                self.amenity == other.amenity and
                self.name == other.name
            )
        return False

    def __hash__(self):
        return hash((
            self.address,
            self.location,
            self.amenity,
            self.name
        ))

    def __str__(self):
        return f"{self.name}({self.address})"


class Geometry:
    def __init__(self, geometry) -> None:
        self.geometry = geometry

    @property
    def coords(self):
        """Extract coordinates from the building geometry."""
        if self.geometry.geom_type == 'Polygon':
            return [list(self.geometry.exterior.coords)]
        elif self.geometry.geom_type == 'MultiPolygon':
            coords = []
            for poly in self.geometry.geoms:
                coords.extend(list(poly.exterior.coords))
            return [coords]
        elif self.geometry.geom_type == 'LineString':
            return [list(self.geometry.coords)]
        else:
            return []
        
    def to_dict(self):
        return self.coords
    
    def __str__(self):
        return str(len(self.polygon))
    

class Distance:
    def __init__(self, distance):
        self.distance = distance

    @property
    def is_acceptable(self) -> bool:
        if self.distance < 1200:
            return True
        return False
