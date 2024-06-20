from pairs import Pairs
from results import Results, Result
from pairs import Pairs
import logging
from id_to_data import IDToData
from data import Distance


class PathCalculator:
    def __init__(self, graph, pairs: Pairs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.graph = graph
        self.pairs = pairs
        self.results = Results()

    def calc_paths(self):
        i = 1
        for residential_buildings, pois in self.pairs:
            logging.info(
                f"Start calculating shortest paths for {i}/{self.pairs.chunk_amounts}. Pairs count {len(residential_buildings)}")
            dists = self.graph.calculate_shortest_path(residential_buildings, pois)
            logging.info(
                f"Done calculating shortest paths for {i}/{self.pairs.chunk_amounts}. Calculated {len(dists)} paths for {len(list(set(residential_buildings.copy())))} points")
            for residential_building, poi, dist in zip(residential_buildings, pois, dists):
                self.results.add(residential_building, poi, Distance(dist))
            i += 1
        self.results.save_to_db()
