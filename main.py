from pyrosm import OSM, get_data
from osm_residential_building import *
from pairs import Pairs
from logging_config import configure_logging
from pandana_graph import PandanaGraph
from shortest_path_calculator import PathCalculator
from trojmiasto_points_of_Interest import AddressToCoordinates, TrojmiastoPlPointsOfInterest

configure_logging()
osm = OSM(get_data('Gdansk'))
b = OSMResidentialBuildings(osm)
address_to_coordinates = AddressToCoordinates(b)
pois = TrojmiastoPlPointsOfInterest(address_to_coordinates)

p = Pairs(pois, b)
pd = PandanaGraph(osm)
pthc = PathCalculator(pd, p)
pthc.calc_paths()
