from pyrosm import OSM, get_data
from osm_residential_building import OSMResidentialBuildings
from pairs import Pairs
from logging_config import configure_logging
from pandana_graph import PandanaGraph
from shortest_path_calculator import PathCalculator
from points_of_interest import PointsOfInteresJsonLoader


def main():
    configure_logging()
    osm = OSM(get_data('Gdansk'))
    b = OSMResidentialBuildings(osm)

    pois = PointsOfInteresJsonLoader()

    p = Pairs(pois, b)
    pd = PandanaGraph(osm)
    pthc = PathCalculator(pd, p)
    pthc.calc_paths()


main()