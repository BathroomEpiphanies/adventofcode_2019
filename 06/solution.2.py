#!/usr/bin/python3

import sys
import networkx as nx

planets = nx.Graph()
for a,b in ( x.strip().split(')') for x in sys.stdin.readlines() ):
    planets.add_edge(a,b)

dists = nx.single_source_shortest_path_length(planets,'COM')
print(sum(dists.values()))

path = next( nx.shortest_simple_paths(planets,'SAN','YOU') )
print( path )
print( len(path)-3 )
