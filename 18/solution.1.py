#!/usr/bin/python3 -u

# low: 4088

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
    keybits.update({ k:2**i for i,k in enumerate('@abcdefghijklmnopqrstuvwxyz')})
    keybits.update({ k:2**i for i,k in enumerate('@ABCDEFGHIJKLMNOPQRSTUVWXYZ')})

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

#keys = keyring()
#area = keyring()
#keys.add('a')
#keys.add('b')
#keys.add(['b','c','r'])
#keys.add('tam')
##area.add('A')
##area.add('C')
#print(keys)
#print(area)
#print(keys.access(area))
#exit()




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
            if t in '@abcdefghijklmnopqrstuvwxyz':
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
queue.append((keypos['@'],0,keyring()))
while queue:
    pos,dist,doors = current = queue.popleft()
    newdoors = doors.copy()
    newdist = dist+1
    #print(current,cave[pos])
    visited.add(pos)
    if cave[pos] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        newdoors.add(cave[pos])
    if cave[pos] in '@abcdefghijklmnopqrstuvwxyz':
        graph.add_node(cave[pos],area=newdoors)
        newdist = 0
    for newpos in [add(pos,d) for d in dirs]:
        if cave[newpos] not in '#' and newpos not in visited:
            queue.append((newpos,newdist,newdoors))

graphpos = graphviz_layout(graph)
nx.draw(graph,graphpos,node_size=800,node_color='#EEEEEE')
nx.draw_networkx_labels(graph,graphpos,{n:f"{n}:{d['area']}" for n,d in graph.nodes(data=True)},font_size=10)
nx.draw_networkx_edge_labels(graph,graphpos,{(u,v):d['weight'] for (u,v,d) in graph.edges(data=True)})
plt.show()


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
        if cave[pos] != key and cave[pos] in '@abcdefghijklmnopqrstuvwxyz':
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
#graphpos = nx.spring_layout(graph)
#graphpos = nx.circular_layout(graph)
nx.draw(graph,graphpos,node_size=800,node_color='#EEEEEE')
nx.draw_networkx_labels(graph,graphpos,{n:f"{n}:{d['area']}" for n,d in graph.nodes(data=True)},font_size=10)
nx.draw_networkx_edge_labels(graph,graphpos,{(u,v):d['weight'] for (u,v,d) in graph.edges(data=True)})
plt.show()







##################################################
# do the thing
##################################################
fullkeys = keyring(keypos)
#print(f"{fullkeys.keys:030b}")
#exit()

queue = PriorityQueue()
visited = set()

queue.put((0,('@',keyring('@'))))
while queue:
    dist,(pos,keys) = current = queue.get()
    print(f"pos, {pos}, dist: {dist: 5d} {str(keys):28s}, visited: {len(visited)}")
    if (pos,keys) in visited:
        continue
    visited.add((pos,keys))
    if keys.access(fullkeys):
        print(f"you did it!! in {dist} steps")
        break
    
    for neigh in graph.neighbors(pos):
        neigharea = graph.nodes(data=True)[neigh]['area']
        newkeys = keys.copy()
        newkeys.add(neigh)
        if keys.access(neigharea) and (neigh,newkeys) not in visited:
            #print("   ",(newdist,(neigh,newkeys)))
            newdist = dist+graph.get_edge_data(pos,neigh)['weight']
            queue.put((newdist,(neigh,newkeys)))
    #break
