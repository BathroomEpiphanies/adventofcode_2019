#!/usr/bin/python3 -u


from queue import PriorityQueue
from itertools import combinations
from collections import defaultdict
import sys
import networkx as nx
import matplotlib.pyplot as plt
import graphviz as gv
from networkx.drawing.nx_agraph import graphviz_layout

def print_cave(cave,xsize,ysize):
    for y in range(ysize):
        for x in range(xsize):
            print(cave[x+y*1j],end='')
        print()


xsize = 0
ysize = 0
portals = set()
cave = defaultdict(lambda:'!')
graph = nx.Graph()
with open(sys.argv[1],'r') as infile:
    for y,line in enumerate([line[:-1] for line in infile.readlines()]):
        for x,t in enumerate(line):
            pos = x+y*1j
            cave.update({pos:t})
        ysize += 1
    xsize = max(xsize,len(line))

for y in range(ysize):
    for x in range(xsize):
        pos = x+y*1j
        if cave[pos] in '.':
            for d in [1,1j]:
                if cave[pos+d] in '.':
                    graph.add_edge(pos,pos+d)

        if cave[pos] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            shift = 'd' if ((0<x and x<xsize-2) and (0<y and y<ysize-2)) else 'u'
            for d in [1,1j]:
                if cave[pos+d] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    portal = cave[pos]+cave[pos+d]
                    portals.add(portal)
                    portal += shift
                    graph.add_node(portal,portal=True)
                    if cave[pos+2*d] in '.':
                        graph.add_edge(portal,pos+3*d)
                    else:
                        graph.add_edge(portal,pos-2*d)
                    cave[pos] = cave[pos].lower()
                    cave[pos+d] = cave[pos+d].lower()



print_cave(cave,xsize,ysize)
print("xsize",xsize,"ysize",ysize)
#print("portals",portals)

graphpos = graphviz_layout(graph)
nx.draw(graph,graphpos,node_size=400,node_color='#AADDDD')
nx.draw_networkx_labels(graph,graphpos,{n:f"{n}" for n in graph.nodes()},font_size=10)
#nx.draw_networkx_edge_labels(graph,graphpos,{(u,v):d['weight'] for (u,v,d) in graph.edges(data=True)})
#nx.draw_networkx_edge_labels(graph,graphpos,{(u,v):f"{d['weight']}:{d['warp']}" for (u,v,d) in graph.edges(data=True)})
nx.drawing.nx_pydot.write_dot(graph,"debug.dot")
plt.show()

reduced = graph.copy()
for node in [u for (u,d) in reduced.nodes(data=True) if not d]:
    for n1,n2 in combinations(reduced.neighbors(node),2):
        reduced.add_edge(n1,n2)
    reduced.remove_node(node)

nx.set_edge_attributes( reduced , {(n1,n2):{'weight':nx.shortest_path_length(graph,n1,n2),'warp':0} for n1 in reduced.nodes() for n2 in reduced.neighbors(n1)} )
reduced = reduced.to_directed()
for portal in portals:
    if portal+'u' in reduced.nodes() and portal+'d' in reduced.nodes():
        reduced.add_edge(portal+'u',portal+'d',weight=1,warp=-1)
        reduced.add_edge(portal+'d',portal+'u',weight=1,warp=+1)

reduced = nx.relabel_nodes(reduced,{'AAu':'AA','ZZu':'ZZ'})

graphpos = graphviz_layout(reduced)
nx.draw(reduced,graphpos,node_size=400,node_color='#AADDDD')
nx.draw_networkx_labels(reduced,graphpos,{n:f"{n}" for n in reduced.nodes()},font_size=10)
nx.draw_networkx_edge_labels(reduced,graphpos,{(u,v):d['weight'] for (u,v,d) in reduced.edges(data=True)})
nx.draw_networkx_edge_labels(reduced,graphpos,{(u,v):f"{d['weight']}:{d['warp']}" for (u,v,d) in reduced.edges(data=True)})
nx.drawing.nx_pydot.write_dot(reduced,"debug.dot")
plt.show()



start,finish = 'AA','ZZ'
path = nx.dijkstra_path(reduced,start,finish)
length = nx.dijkstra_path_length(reduced,start,finish)
print(f"Shortest path (length {length}) from {start} to {finish}: {path}")


queue = PriorityQueue()
visited = set()
start = ('AA',0)
goal = ('ZZ',0)
print(start)
print(goal)
queue.put((0,start))
while not queue.empty():
    dist,(pos,dim) = current = queue.get()
    print(f"pos×dim: {pos}×{dim}    dist: {dist: 5d}    visited: {len(visited)}    qlen: {queue.qsize()}")
    if (pos,dim) in visited:
        continue
    visited.add((pos,dim))
    if (pos,dim) == goal:
        print(f"you did it!! in {dist} steps")
        break

    for neigh in reduced.neighbors(pos):
        pos2 = neigh
        newdim = dim + reduced.get_edge_data(pos,neigh)['warp']
        newdist = dist + reduced.get_edge_data(pos,neigh)['weight']
        if newdim >= 0 and (pos2,newdim) not in visited:
            #print("    ",neigh,newdim,newdist)
            queue.put((newdist,(pos2,newdim)))
        #else:
        #    print("        ",neigh,newdim,newdist)
