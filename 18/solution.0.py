#!/usr/bin/python3

from copy import deepcopy
from collections import defaultdict
import sys
import networkx as nx


with open(sys.argv[1],'r') as infile:
    cave = [[x for x in line.strip()] for line in infile.readlines()]

ysize,xsize = len(cave),len(cave[0])
print(xsize,ysize)
for line in cave:
    print(''.join([str(i) for i in line]))

doorkey = {'a':'A','b':'B','c':'C','d':'D','e':'E','f':'F','g':'G','h':'H','i':'I','j':'J','k':'K','l':'L','m':'M','n':'N','o':'O','p':'P','q':'Q','r':'R','s':'S','t':'T','u':'U','v':'V','w':'W','x':'X','y':'Y','z':'Z'}

maxdepth = 30
totalmaxlen = None
def find_keys(cave,depth,lensofar):
    global totalmaxlen
    if depth > maxdepth:
        #print(f"maxdepth, returning: 0")
        return 0
    #print(depth)
    #for line in cave:
    #    print(''.join([str(i) for i in line]))
    #print()
    #sys.stdin.readline()
    keypos = {}
    doorpos = defaultdict(lambda:None)
    graph = nx.Graph()
    startpos = None
    for y in range(1,ysize-1):
        for x in range(1,xsize-1):
            if cave[y][x] in 'abcdefghijklmnopqrstuvwxyz':
                keypos.update({cave[y][x]:(x,y)})
            if cave[y][x] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                doorpos.update({cave[y][x]:(x,y)})
            if cave[y][x] in '@':
                startpos = (x,y)
            if cave[y][x] in '.@abcdefghijklmnopqrstuvwxyz':
                if cave[y][x+1] in '.@abcdefghijklmnopqrstuvwxyz':
                    graph.add_edge((x,y),(x+1,y))
                if cave[y+1][x] in '.@abcdefghijklmnopqrstuvwxyz':
                    graph.add_edge((x,y),(x,y+1))
                if cave[y][x-1] in '.@abcdefghijklmnopqrstuvwxyz':
                    graph.add_edge((x,y),(x-1,y))
                if cave[y-1][x] in '.@abcdefghijklmnopqrstuvwxyz':
                    graph.add_edge((x,y),(x,y-1))
    
    keydists = {}
    for k,p in keypos.items():
        try:
            keydists.update({k:nx.shortest_path_length(graph,startpos,p)})
        except:
            pass
    #print(keydists)
    if not keydists:
        if totalmaxlen is None or lensofar<totalmaxlen:
            totalmaxlen = lensofar
            print(f"setting totalmaxlen to {totalmaxlen}")
        #print(f"out of keys, returning: 0")
        return 0
    elif totalmaxlen is not None and lensofar>=totalmaxlen:
        #print(f"hopeless, at depth: {depth}")
        return 100000000000000

    #searchkeys = sorted(list(keydists.items()),lambda x:x[1])
    searchkeys = list(keydists.items())
    searchkeys.sort(key=lambda x:x[1])

    #print(searchkeys)
    minpath = None
    for k,_ in searchkeys:
        pathlen = keydists[k]
        nextcave = deepcopy(cave)
        nextcave[keypos[k][1]][keypos[k][0]] = '@'
        dpos = doorpos[doorkey[k]]
        if dpos is not None:
            nextcave[dpos[1]][dpos[0]] = '.'
        nextcave[startpos[1]][startpos[0]] = '.'
        pathlen += find_keys(nextcave,depth+1,lensofar+pathlen)
        if minpath is None or pathlen < minpath:
            minpath = pathlen
    #print(f"minpath: {minpath}")
    return minpath

minpath = find_keys(deepcopy(cave),0,0)
print(minpath)

exit()
keypos = {}
graph = nx.Graph()
startpos = None
for y in range(1,ysize-1):
    for x in range(1,xsize-1):
        if cave[y][x] in '.@abcdefghijklmnopqrstuvwxyz':
            if cave[y][x] in '@abcdefghijklmnopqrstuvwxyz':
                keypos.update({cave[y][x]:(x,y)})
            if cave[y][x+1] in '.@abcdefghijklmnopqrstuvwxyz':
                graph.add_edge((x,y),(x+1,y))
            if cave[y+1][x] in '.@abcdefghijklmnopqrstuvwxyz':
                graph.add_edge((x,y),(x,y+1))
            if cave[y][x-1] in '.@abcdefghijklmnopqrstuvwxyz':
                graph.add_edge((x,y),(x-1,y))
            if cave[y-1][x] in '.@abcdefghijklmnopqrstuvwxyz':
                graph.add_edge((x,y),(x,y-1))
        if cave[y][x] in '@':
            startpos = (x,y)

#print(graph.edges())
#print(startpos)

print(keypos)



pathdists = nx.single_source_shortest_path_length(graph,startpos)
plot = [[' ' for _ in range(xsize)] for _ in range(ysize)]
for p,d in pathdists.items():
    plot[p[1]][p[0]] = d%10
plot[startpos[1]][startpos[0]] = '@'
for k,p in keypos.items():
    plot[p[1]][p[0]] = k

    
for line in plot:
    print(''.join([str(i) for i in line]))


keydists = {}
for k,p in keypos.items():
    print(k,p)
    try:
        keydists.update({k:nx.shortest_path_length(graph,startpos,p)})
    except:
        pass
print(keydists)
