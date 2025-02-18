import utils
import math
from collections import defaultdict, deque

import numpy as np
from scipy.spatial import distance_matrix
import heapq


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.max_distance = 4730365236290022000  #default to just under 500LY
        self.current = None
        self.visited = set()
        self.path = []
        self.start_system = None

    def set_max_distance(self, distance):
        self.max_distance = distance

    def add_node(self, solar_system):
        n = solar_system
        if n not in self.nodes:
            self.nodes.add(n)
            self.edges[n] = {}

    #Takes solar system as nodes
    def add_edge(self, node1, node2, weight):
        self.edges[node1][node2] = weight
        self.edges[node2][node1] = weight

    def remove_edge(self, node1, node2):
        if node2 in self.edges[node1]:
            del self.edges[node1][node2]
            del self.edges[node2][node1]

    def get_neighbors(self, node):
        #print(self.edges[node].keys())
        return list(self.edges[node].keys())

    def find_neighbors(self, node):
        for n in self.edges:
            if n.name != node.name:
                distance = utils.distance(node.center, n.center)
                if distance < self.max_distance:
                    self.add_edge(node, n, distance)

    def remove_all_edges(self):
        for n in self.edges:
            self.edges[n] = {}

    def is_traversable(self):
        traversable = []
        for n in self.edges:
            if n in traversable:
                break
            for m in self.edges:
                if utils.distance(n.center, m.center) < self.max_distance and m != n:
                    traversable.append(n)
                    break

        if len(traversable) == len(self.edges):
            return True

        return False

    def get_node_by_name(self, name):
        for n in self.edges:
            if n.name.lower() == name.lower():
                return n

    def group_solar_systems(self, solar_systems, max_distance):
        '''Group solar systems by max distance. This show groups of solar systems that can't be traveled between'''
        groups = defaultdict(list)
        visited = set()

        group_id = 0
        print("Processing. Please wait")
        for start_system in solar_systems:
            if start_system in visited:
                continue

            queue = deque([start_system])
            visited.add(start_system)
            groups[group_id].append(start_system)

            while queue:
                current_system = queue.popleft()
                for other in solar_systems:
                    if other not in visited:
                        distance = utils.distance(current_system.center, other.center)
                        if distance <= max_distance:
                            queue.append(other)
                            visited.add(other)
                            groups[group_id].append(other)

            group_id += 1

        return list(groups.values())

    def filter_groups_by_which_are_connected(self, groups):
        new_groups = []
        for g in groups:
            connected = False
            for s in g:
                if len(s.neighbours) > 0:
                    connected = True 
                    break
            if not connected:
                new_groups.append(g)
        return new_groups

    def preprocess_edges(self):
        for n in self.edges:
            self.find_neighbors(n)

    def all_nodes_visited(self):
        return self.nodes == self.visited

    def all_neighbors_visited(self):
        neighbors_visited = True
        neighbors = self.get_neighbors(self.current)
        for n in neighbors:
            if n not in self.visited:
                neighbors_visited = False
                break
        return neighbors_visited

    def get_next_shortest_unvisted_node(self, node):
        current = node
        shortest = -1
        system = None
        neighbors = self.get_neighbors(node)
        for n in neighbors:
            if self.edges[current][n] < shortest or shortest < 0:
                if n in self.visited:
                    continue
                shortest = self.edges[current][n]
                system = n
        return system if shortest > 0 else None

    def backtrack(self):
        backtrack_path = {}
        for n in self.path[::-1]:
            if self.get_next_shortest_unvisted_node(n) is not None:
                return n

    def dijkstra(self, start, end):
        path = []
        distances = {node: float('inf') for node in self.nodes}
        distances[start] = 0
        pq = [(0, start)]
        previous = {node: None for node in self.nodes}

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node == end:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = previous[current_node]
                return path[::-1]

            if current_distance > distances[current_node]:
                continue

            for neighbor in self.edges[current_node].keys():
                distance = current_distance + self.edges[current_node][neighbor]
                if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous[neighbor] = current_node
                        heapq.heappush(pq, (distance, neighbor))

        return None

    def greedy(self, start_system_name):
        self.start_system = self.get_node_by_name(start_system_name)
        self.visited.add(self.start_system)
        self.path.append(self.start_system)
        self.current = self.start_system
        while not self.all_nodes_visited():
            neighbors = self.get_neighbors(self.current)
            if (self.current == self.start_system and self.all_neighbors_visited()):
                print("Cannot Traverse entire graph")
                break
            shortest = self.get_next_shortest_unvisted_node(self.current) ##Get unvisited node with shortest path
            if shortest is None:
                target = self.backtrack() ##Backtrack to latest shortest (Don't add to path)
                path = self.dijkstra(self.current, target) ##Use dijkstra alg to add to path to target. Should never be None since we can backtrack
                self.path += path
                shortest = target
            else:
                self.path.append(shortest)
            self.current = shortest
            self.visited.add(shortest)
        path = self.optimize(self.path)
        return path

    def remove_consecutive_duplicates(self, path):
        return [x for i, x in enumerate(path) if i == 0 or x != path[i-1]]

    def optimize(self, path):
        path = self.remove_consecutive_duplicates(path)
        return path


    def __str__(self):
        result = []
        for node, neighbors in self.edges.items():
            for neighbor, weight in neighbors.items():
                result.append(f"{node} -- {weight} --> {neighbor}")
        return "\n".join(result)
