import json
from typing import List, Tuple
from galaxy import Region
from galaxy import SolarSystem
from galaxy import Constellation

class GraphSystem(SolarSystem):

    def __init__(self, name:str, solarsystemid:int, region_name: str, constellation_name: int, center: list, neighbors: list, planets: list):
            super().__init__(name, solarsystemid, region_name, constellation_name, center, neighbors, planets)
            self.edges = {}

class GraphConstellations(Constellation):
    pass


class GraphRegion:
    def __init__(self, region: Region, galaxy: dict):
        self.name = region.name
        self.region_id = region.regionid
        self.solar_systems = self.__populate_graphsystems(region.solarsystems, galaxy)
        self.constellations = self.__populate_graphconstellations(region.constellations, galaxy)
        self.connected = False

    def __populate_graphsystems(self, solarsystems: list, galaxy: dict):
        solar_systems = {}
        for s in solarsystems:
            ss = galaxy['solarsystems'][s]
            solar_systems[s] = GraphSystem(ss.name, ss.solarsystemid, ss.region_name, ss.constellation_name, ss.center, ss.neighbors, ss.planets)
        if len(solar_systems[s].neighbors) > 1:
            self.connected = True
        return solar_systems

    def __populate_graphconstellations(self, constellations: list, galaxy: dict):
        constel = {}
        for c in constellations:
            constellation = galaxy["constellations"][c]
            constel[c] = GraphConstellations(constellation.name, constellation.constellationid, constellation.region_name, constellation.solarsystems)
        return constel

    def list_solar_systems(self) -> List[str]:
        return list(self.solar_systems.keys())

    def __str__(self):
        return f"Region {self.name} with {len(self.constellations)} Constellatiosn and {len(self.solar_systems)} solar systems. Connected = {self.connected}"