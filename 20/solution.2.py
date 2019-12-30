#!/usr/bin/python3 -u


from queue import PriorityQueue
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
portals = set()
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
            if x < 1 or xsize < x+3 or y < 1 or ysize < y+3:
                loc = 'up'
            else:
                loc = 'dw'

            pre = add(pos,dirs[2])
            second = add(pos,dirs[0])
            if cave[second] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                third = add(second,dirs[0])
                if cave[third] in '.':
                    portal = cave[pos]+cave[second]
                    portals.add(portal)
                    graph.add_node(portal+loc+'ou',portal=True)
                    graph.add_node(portal+loc+'in',portal=True)
                    graph.add_edge(add(third,dirs[0]),portal+loc+'in',dim=0)
                    graph.add_edge(portal+loc+'ou',add(third,dirs[0]),dim=0)
                else:
                    portal = cave[pos]+cave[second]
                    portals.add(portal)
                    graph.add_node(portal+loc+'ou',portal=True)
                    graph.add_node(portal+loc+'in',portal=True)
                    graph.add_edge(add(pre,dirs[2]),portal+loc+'in',dim=0)
                    graph.add_edge(portal+loc+'ou',add(pre,dirs[2]),dim=0)

            pre = add(pos,dirs[3])
            second = add(pos,dirs[1])
            if cave[second] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                third = add(second,dirs[1])
                if cave[third] in '.':
                    portal = cave[pos]+cave[second]
                    portals.add(portal)
                    graph.add_node(portal+loc+'ou',portal=True)
                    graph.add_node(portal+loc+'in',portal=True)
                    graph.add_edge(add(third,dirs[1]),portal+loc+'in',dim=0)
                    graph.add_edge(portal+loc+'ou',add(third,dirs[1]),dim=0)
                else:
                    portal = cave[pos]+cave[second]
                    portals.add(portal)
                    graph.add_node(portal+loc+'ou',portal=True)
                    graph.add_node(portal+loc+'in',portal=True)
                    graph.add_edge(add(pre,dirs[3]),portal+loc+'in',dim=0)
                    graph.add_edge(portal+loc+'ou',add(pre,dirs[3]),dim=0)


print_cave(cave,xsize,ysize)
print("xsize",xsize,"ysize",ysize)


#print(graph.nodes(data=True))
#print(graph.edges())


##graphpos = graphviz_layout(graph)
#graphpos = nx.spring_layout(graph)
#nx.draw(graph,graphpos,node_size=400,node_color='#AADDDD')
#nx.draw_networkx_labels(graph,graphpos,{n:f"{n}" for n in graph.nodes()},font_size=10)
##nx.draw_networkx_edge_labels(graph,graphpos,{(u,v):d['weight'] for (u,v,d) in graph.edges(data=True)})
#plt.show()

#print(portals)
for a in portals:
    for b in portals:
        if a == b:
            continue
        try:
            l = len(next(nx.shortest_simple_paths(graph, a+'dw'+'ou' , b+'dw'+'in' )))-1
            graph.add_edge(a+'dw'+'ou' , b+'dw'+'in',weight=l,dim=0)
        except:
            pass
        try:
            l = len(next(nx.shortest_simple_paths(graph, a+'up'+'ou' , b+'dw'+'in' )))-1
            graph.add_edge(a+'up'+'ou' , b+'dw'+'in',weight=l,dim=0)
        except:
            pass
        try:
            l = len(next(nx.shortest_simple_paths(graph, a+'dw'+'ou' , b+'up'+'in' )))-1
            graph.add_edge(a+'dw'+'ou' , b+'up'+'in',weight=l,dim=0)
        except:
            pass
        try:
            l = len(next(nx.shortest_simple_paths(graph, a+'up'+'ou' , b+'up'+'in' )))-1
            graph.add_edge(a+'up'+'ou' , b+'up'+'in',weight=l,dim=0)
        except:
            pass

#print(graph.nodes(data=True))

for a in portals:
    graph.add_edge(a+'up'+'in',a+'dw'+'ou',weight=1,dim=-1)
    graph.add_edge(a+'dw'+'in',a+'up'+'ou',weight=1,dim= 1)
for n in [u for (u,d) in graph.nodes(data=True) if not d]:
    graph.remove_node(n)


#print(graph.nodes(data=True))

graph.remove_node('AAupin')
#graph.remove_node('AAdwin')
graph.remove_node('ZZupou')
#graph.remove_node('ZZdwou')
graph = nx.relabel_nodes(graph,{'AAupou':'AA','ZZupin':'ZZ'})

#print(graph.nodes(data=True))
graphpos = graphviz_layout(graph)
#graphpos = nx.spring_layout(graph)
nx.draw(graph,graphpos,node_size=400,node_color='#AADDDD')
nx.draw_networkx_labels(graph,graphpos,{n:f"{n}" for n in graph.nodes()},font_size=10)
nx.draw_networkx_edge_labels(graph,graphpos,{(u,v):d['weight'] if 'weight' in d else '' for (u,v,d) in graph.edges(data=True)})
plt.show()

start,finish = 'AA','ZZ'
path = nx.dijkstra_path(graph,start,finish)
length = nx.dijkstra_path_length(graph,start,finish)
print(path)
#print(length)
print(f"Shortest path from {start} to {finish}: {length}")

#for edge in graph.edges(data=True):
#    print(edge)

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

    for neigh in graph.neighbors(pos):
        newpos = neigh
        newdim = dim + graph.get_edge_data(pos,neigh)['dim']
        newdist = dist + graph.get_edge_data(pos,neigh)['weight']
        if newdim >= 0 and (newpos,newdim) not in visited:
            #print("    ",neigh,newdim,newdist)
            queue.put((newdist,(newpos,newdim)))
        #else:
        #    print("        ",neigh,newdim,newdist)
