import os
import argparse
from graph import Graph
import pickle
from galaxy import *
from graphregion import GraphRegion, GraphSystem
import utils

def create_full_graph(galaxy: GraphRegion) -> Graph:
    graph = Graph()
    for s in galaxy["solarsystems"]:
        graph.add_node(s)
    return graph

def create_graph(region: GraphRegion) -> Graph:
    graph = Graph()
    for s in region.solar_systems:
        graph.add_node(region.solar_systems[s])
    return graph

def main():
    parser = argparse.ArgumentParser(description="Various analysis on map data.")
    parser.add_argument('--jumpdistance', help='Maxmimum jump distance of fully fueled ship in light years.')
    args = parser.parse_args()

    if args.jumpdistance:
        jumpdistance = int(args.jumpdistance)
    else:
        jumpdistance = None

    pickle_file = 'data/mapdata.pkl'
    try:
        with open(pickle_file, 'rb') as f:
            galaxy = pickle.load(f)
    except FileNotFoundError:
        print(f"File not found: {pickle_file}")
        return

    graph = create_full_graph(galaxy)
    print(f"Number of solar systems: {len(galaxy['solarsystems'])}")
    print(f"Number of Regions: {len(galaxy['regions'])}")
    print(f"Number of Constellations: {len(galaxy['constellations'])}")
    solar_systems = []
    for g in galaxy['solarsystems']:
        solar_systems.append(galaxy['solarsystems'][g])
    groups = graph.group_solar_systems(solar_systems) #Leaving out jumpdistance to take default ~500LY amount
    filtered_groups = graph.filter_groups_by_which_are_connected(groups)
    print(f"Size of groups seperated by a max distance of {utils.convert_meters_to_light_years(graph.max_distance)} LY")
    biggest = 0
    biggest_group = []
    group_len = []
    for g in groups:
        l = len(g)
        if l > biggest:
            biggest = l
            biggest_group = g
    group_len.append(biggest)
    total = 0
    for g in filtered_groups:
        l = len(g)
        group_len.append(l)
        total += l
    for g in group_len:
        print(f'\t{g}')
    print(f"Number of groups {len(group_len)}") #This will be off if a connected system becomes untraversable (like the admin region)
    print(f"Number of ungateable star systems {total}")

    smallest = (None, int(2**32))
    for region in galaxy['regions']:
        connected = False
        for s in galaxy['regions'][region].solarsystems:
            if len(galaxy['solarsystems'][s].neighbors) > 0:
                connected = True
                break
        if connected:
            continue
        graph_region = GraphRegion(galaxy["regions"][region], galaxy)
        graph = create_graph(graph_region)
        if jumpdistance is not None:
            graph.set_max_distance(utils.convert_light_years_to_meters(jumpdistance))
        graph.preprocess_edges()
        if graph.is_traversable():
            if len(graph.nodes) < smallest[1]:
                for b in biggest_group:
                    if b.name in [n.name for n in graph.nodes]:
                        smallest = (region, len(graph.nodes))
                        break

    print(f"Smallest unconnected region traversable by {jumpdistance} LY: {smallest[0]} with {smallest[1]} systems")


if __name__ == "__main__":
    main()