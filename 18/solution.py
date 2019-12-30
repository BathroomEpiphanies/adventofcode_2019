#!/usr/bin/python3 -u

from copy import deepcopy
from collections import defaultdict
import sys
import networkx as nx

doorkey = {'a':'A','b':'B','c':'C','d':'D','e':'E','f':'F','g':'G','h':'H','i':'I','j':'J','k':'K','l':'L','m':'M','n':'N','o':'O','p':'P','q':'Q','r':'R','s':'S','t':'T','u':'U','v':'V','w':'W','x':'X','y':'Y','z':'Z'}
cave = defaultdict(lambda:'!')
xsize = 0
ysize = 0
graph = nx.Graph()
startpos = None
keypos = {}
doorpos = defaultdict(lambda:None)


def add(a,b):
    #print("add",a,b)
    return (a[0]+b[0],a[1]+b[1])
                 
def add_edges_at(pos):
    #print("add_edge",pos)
    global cave,graph
    for d in [(1,0),(0,1),(-1,0),(0,-1)]:
        if cave[add(pos,d)] in '.@abcdefghijklmnopqrstuvwxyz':
            graph.add_edge(pos,(add(pos,d)))

def del_edges_at(pos):
    global graph
    graph.remove_node(pos)
    
def parse_cave():
    global cave,startpos,keypos,doorpos
    graph = nx.Graph()
    for pos in cave:
        if cave[pos] in 'abcdefghijklmnopqrstuvwxyz':
            keypos.update({cave[pos]:pos})
        if cave[pos] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            doorpos.update({cave[pos]:pos})
        if cave[pos] in '@':
            startpos = pos
        if cave[pos] in '.@abcdefghijklmnopqrstuvwxyz':
            add_edges_at(pos)
    return


def print_cave():
    global xsize,ysize
    for y in range(ysize):
        for x in range(xsize):
            print(cave[(x,y)],end='')
        print()

def collect_keys(cutoff,accum):
    global graph,cave,startpos,keypos,doorpos
    #print(accum)
    if not keypos:
        if accum <= cutoff:
            #print("returning true")
            return True
        else:
            return False
    elif accum > cutoff:
        return False

    keydists = {}
    for key,pos in keypos.items():
        try:
            #print(pos,startpos)
            keydists.update({key:nx.shortest_path_length(graph,startpos,pos)})
        except Exception as e:
            #print(e)
            pass

    #print("keydists",keydists)
    #print("keypos",keypos)
    for key in list(keydists):
        pos = keypos.pop(key)
        savepos = startpos
        startpos = pos
        if doorkey[key] in doorpos:
            add_edges_at(doorpos[doorkey[key]])
        success = collect_keys(cutoff,accum+keydists[key])
        if doorkey[key] in doorpos:
            del_edges_at(doorpos[doorkey[key]])
        startpos = savepos
        keypos.update({key:pos})
        if success:
            return True
    return False



with open(sys.argv[1],'r') as infile:
    for y,line in enumerate([line.strip() for line in infile.readlines()]):
        for x,t in enumerate(line):
            cave.update({(x,y):t})
        ysize += 1
        xsize = len(line)


parse_cave()
print_cave()

#collect_keys(40,0)
#exit()

for middle in range(int(sys.argv[2]),0,-1):
    print(f"testing for {middle}",end=' ')
    if collect_keys(middle,0):
        upper = middle
        print(f"success")
    else:
        lower = middle
        print(f"fail")

#lower = 0
#upper = 100
#while lower<upper-1:
#    middle = (upper+lower)//2
#    #print(f"testing for {middle}",end=' ')
#    print(f"testing for {middle}")
#    if collect_keys(middle,0):
#        upper = middle
#        print(f"success")
#    else:
#        lower = middle
#        print(f"fail")
