import json
import os
import argparse
from graph import Graph
import pickle
from galaxy import *
from graphregion import GraphRegion, GraphSystem
import utils

def create_graph(region: GraphRegion) -> Graph:
    graph = Graph()
    for s in region.solar_systems:
        graph.add_node(region.solar_systems[s])
    return graph


def main():
    parser = argparse.ArgumentParser(description="Find an approximate shortest path in a region.")
    parser.add_argument('--solarsystem', help='Name of solar system to start with', required=True)
    parser.add_argument('--jumpdistance', help='Maxmimum jump distance of fully fueled ship in light years.')
    parser.add_argument('--format', help='This will format the output into a copy/pasteable format for Eve: Frontier', action='store_true')
    args = parser.parse_args()

    if args.jumpdistance:
        max_jump_distance_ly = args.jumpdistance
    else:
        max_jump_distance_ly = 168

    max_jump_distance_meters = utils.convert_light_years_to_meters(max_jump_distance_ly)

    galaxy = None
    pickle_file = 'data/mapdata.pkl'
    try:
        with open(pickle_file, 'rb') as f:
            galaxy = pickle.load(f)
    except FileNotFoundError:
        print(f"File not found: {pickle_file}")
        return

    try:
        solar_system = galaxy["solarsystems"][args.solarsystem]
    except KeyError:
        print(f"solar system name not found: {args.solarsystem}")
        return

    region_name = solar_system.region_name

    region = GraphRegion(galaxy["regions"][region_name], galaxy)
    graph = create_graph(region)
    system = graph.get_node_by_name(args.solarsystem)
    graph.set_max_distance(max_jump_distance_meters)
    graph.preprocess_edges()
    path = graph.greedy(args.solarsystem)
    distance = 0
    for i, p in enumerate(path[:-1]):
        distance += utils.distance(path[i].center, path[i+1].center)
    length = 0
    for p in path:
        if args.format:
            string = f'<font size="14" color="#bfffffff"></font><font size="14" color="#ffd98d00"><a href="showinfo:5//{p.solarsystemid}">{p.name}</a></font>'
            length += len(string)
            if length < 3900:
                print(string)
            else:
                print(f"\nNew note required:")
                print(string)
                length = len(string)
        else:
            print(p.name)
    print(f"Number of jumps: {len(path)}")

if __name__ == "__main__":
    main()