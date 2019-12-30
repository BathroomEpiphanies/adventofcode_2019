#!/usr/bin/python3 -u


from collections import defaultdict
import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
import graphviz as gv
from networkx.drawing.nx_agraph import graphviz_layout


dirs = [(1,0),(0,1),(-1,0),(0,-1)]
def add(a,b):
    return (a[0]+b[0],a[1]+b[1])
def print_cave(cave,xsize,ysize):
    for y in range(ysize):
        for x in range(xsize):
            print(cave[(x,y)],end='')
        print()


xsize = 0
ysize = 0
warppos = defaultdict(lambda:None)
cave = defaultdict(lambda:'!')
graph = nx.DiGraph()
with open(sys.argv[1],'r') as infile:
    for y,line in enumerate([line[:-1] for line in infile.readlines()]):
        for x,t in enumerate(line):
            pos = (x,y)
            cave.update({pos:t})
        ysize += 1
    xsize = max(xsize,len(line))



for y in range(ysize):
    for x in range(xsize):
        pos = (x,y)
        if cave[pos] in '.':
            for newpos in [add(pos,d) for d in dirs]:
                if cave[newpos] in '.':
                    graph.add_edge(pos,newpos)
                    graph.add_edge(newpos,pos)
        if cave[pos] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            pre = add(pos,dirs[2])
            second = add(pos,dirs[0])
            if cave[second] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                third = add(second,dirs[0])
                if cave[third] in '.':
                    portal = cave[pos]+cave[second]
                    graph.add_edge(add(third,dirs[0]),portal+'in')
                    graph.add_edge(portal+'ou',add(third,dirs[0]))
                    graph.add_edge(portal+'in',portal+'ou')
                else:
                    portal = cave[pos]+cave[second]
                    graph.add_edge(add(pre,dirs[2]),portal+'in')
                    graph.add_edge(portal+'ou',add(pre,dirs[2]))
                    graph.add_edge(portal+'in',portal+'ou')
            pre = add(pos,dirs[3])
            second = add(pos,dirs[1])
            if cave[second] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                third = add(second,dirs[1])
                if cave[third] in '.':
                    portal = cave[pos]+cave[second]
                    graph.add_edge(add(third,dirs[1]),portal+'in')
                    graph.add_edge(portal+'ou',add(third,dirs[1]))
                    graph.add_edge(portal+'in',portal+'ou')
                else:
                    portal = cave[pos]+cave[second]
                    graph.add_edge(add(pre,dirs[3]),portal+'in')
                    graph.add_edge(portal+'ou',add(pre,dirs[3]))
                    graph.add_edge(portal+'in',portal+'ou')

print(xsize,ysize)
print_cave(cave,xsize,ysize)


print(graph.edges())


##graphpos = graphviz_layout(graph)
#graphpos = nx.spring_layout(graph)
#nx.draw(graph,graphpos,node_size=400,node_color='#AADDDD')
#nx.draw_networkx_labels(graph,graphpos,{n:f"{n}" for n in graph.nodes()},font_size=10)
##nx.draw_networkx_edge_labels(graph,graphpos,{(u,v):d['weight'] for (u,v,d) in graph.edges(data=True)})
#plt.show()


start,finish = 'AAou','ZZin'
path = next( nx.shortest_simple_paths(graph,start,finish) )
print(f"Shortest path from {start} to {finish}: {len(path)-1}")
#
#start,finish = 'DEou','ZZin'
#path = next( nx.shortest_simple_paths(graph,start,finish) )
#print(f"Shortest path from {start} to {finish}: {len(path)-1}")
#
#start,finish = 'DEou','AAin'
#path = next( nx.shortest_simple_paths(graph,start,finish) )
#print(f"Shortest path from {start} to {finish}: {len(path)-1}")

# wrong: 58
