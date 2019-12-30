#!/usr/bin/python3 -u

#from queue import PriorityQueue
from queue import deque
from queue import PriorityQueue

import json
from collections import defaultdict
import sys
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as gv
from networkx.drawing.nx_agraph import graphviz_layout


dirs = [(1,0),(0,1),(-1,0),(0,-1)]
def add(a,b):
    return (a[0]+b[0],a[1]+b[1])

class keyring():
    keybits = defaultdict(lambda:0)
    keybits.update({ k:2**i for i,k in enumerate('0123abcdefghijklmnopqrstuvwxyz')})
    keybits.update({ k:2**i for i,k in enumerate('0123ABCDEFGHIJKLMNOPQRSTUVWXYZ')})

    def __init__(self,keys=[]):
        self.keys = 0
        self.chars = set()
        self.add(keys)
    def add(self,keys):
        for key in keys:
            self.keys |= keyring.keybits[key]
            self.chars.add(key)
    def access(self,area):
        return ~self.keys & area.keys == 0
    def copy(self):
        other = keyring()
        other.keys = self.keys
        other.chars = self.chars.copy()
        return other
    def __repr__(self):
        return ''.join([k for k in self.chars])
    def __str__(self):
        return ''.join([k for k in self.chars])
    def __hash__(self):
        return self.keys
    def __lt__(self,other):
        return len(other)-len(self)
    def __eq__(self,other):
        return self.keys == other.keys
    def __len__(self):
        return len(self.chars)



##################################################
# read in cave, find keys and doors
##################################################
xsize = 0
ysize = 0
keypos = defaultdict(lambda:None)
doorpos = defaultdict(lambda:None)
cave = defaultdict(lambda:'!')
with open(sys.argv[1],'r') as infile:
    for y,line in enumerate([line.strip() for line in infile.readlines()]):
        for x,t in enumerate(line):
            pos = (x,y)
            cave.update({pos:t})
            if t in '0123abcdefghijklmnopqrstuvwxyz':
                keypos.update({t:pos})
            if t in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                doorpos.update({t:pos})
        ysize += 1
        xsize = len(line)

#print(doorpos)
#print(keypos)



graph = nx.Graph()

##################################################
# find access areas
##################################################
queue = deque()
visited = set()
for key in ['0','1','2','3']:
    queue.append((keypos[key],0,keyring()))
    while queue:
        pos,dist,doors = current = queue.popleft()
        newdoors = doors.copy()
        newdist = dist+1
        print(current,cave[pos])
        visited.add(pos)
        if cave[pos] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            newdoors.add(cave[pos])
        if cave[pos] in '0123abcdefghijklmnopqrstuvwxyz':
            graph.add_node(cave[pos],area=newdoors)
            newdist = 0
        for newpos in [add(pos,d) for d in dirs]:
            if cave[newpos] not in '#' and newpos not in visited:
                queue.append((newpos,newdist,newdoors))

#graphpos = graphviz_layout(graph)
#nx.draw(graph,graphpos,node_size=800,node_color='#EEEEEE')
#nx.draw_networkx_labels(graph,graphpos,{n:f"{n}:{d['area']}" for n,d in graph.nodes(data=True)},font_size=10)
#nx.draw_networkx_edge_labels(graph,graphpos,{(u,v):d['weight'] for (u,v,d) in graph.edges(data=True)})
#plt.show()


##################################################
# find shortest paths between keys
##################################################
for key in keypos:
    queue = deque()
    visited = set()
    queue.append((keypos[key],0))
    while queue:
        pos,dist = current = queue.popleft()
        newdist = dist+1
        visited.add(pos)
        if cave[pos] != key and cave[pos] in '0123abcdefghijklmnopqrstuvwxyz':
            graph.add_edge(key,cave[pos],weight=dist)
            continue
        for newpos in [add(pos,d) for d in dirs]:
            if cave[newpos] not in '#' and newpos not in visited:
                queue.append((newpos,newdist))




##################################################
# plot graph for sanity
##################################################
#print(graph.nodes(data=True))
#print(graph.edges(data=True))

graphpos = graphviz_layout(graph)
nx.draw(graph,graphpos,node_size=800,node_color='#EEEEEE')
nx.draw_networkx_labels(graph,graphpos,{n:f"{n}:{d['area']}" for n,d in graph.nodes(data=True)},font_size=10)
nx.draw_networkx_edge_labels(graph,graphpos,{(u,v):d['weight'] for (u,v,d) in graph.edges(data=True)})
plt.show()







##################################################
# do the thing
##################################################
fullkeys = keyring(keypos)
#print(sorted(str(fullkeys)))
#print(f"{fullkeys.keys:032b}")
#exit()

queue = PriorityQueue()
visited = set()

queue.put((0,('0123',keyring('0123'))))
while not queue.empty():
    dist,(pos,keys) = current = queue.get()
    print(f"pos, {pos}    dist: {dist: 5d}    keys: {str(keys):32s}    visited: {len(visited)}    qlen: {queue.qsize()}")
    if (pos,keys) in visited:
        continue
    visited.add((pos,keys))
    
    if keys.access(fullkeys):
        print(f"you did it!! in {dist} steps")
        break

    for bot,bpos in enumerate(pos):
        #print(bot,bpos)
        for neigh in graph.neighbors(bpos):
            newpos = ''.join([pos[0:bot],neigh,pos[bot+1:4]])
            neigharea = graph.nodes(data=True)[neigh]['area']
            newkeys = keys.copy()
            newkeys.add(neigh)
            newdist = dist+graph.get_edge_data(bpos,neigh)['weight']
            if keys.access(neigharea) and (newpos,newkeys) not in visited:
                queue.put((newdist,(newpos,newkeys)))
