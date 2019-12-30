#!/usr/bin/python3

import sys
from graph import Graph

planets = Graph()
#with open('input.in','r') as input:
with open('example.1.ex','r') as input:
    for a,b in ( x.strip().split(')') for x in input.readlines() ):
        planets.add_edge(a,b)
print(planets)

print(sum(planets.distances('COM').values()))
print(planets.distances('YOU')['SAN']-2)
#print(planets.shortest_path('YOU','SAN'))

planets.dot('debug.dot')
