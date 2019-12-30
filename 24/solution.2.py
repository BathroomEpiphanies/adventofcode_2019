#!/usr/bin/python3 -u

from copy import deepcopy
import queue
from collections import defaultdict
import time
import sys

def empty():
    return {(r,c):0 for c in range(5) for r in range(5)}

def pspace(space):
    bugs = 0
    for l in sorted(space):
        bugs += sum(space[l].values())
        out = [['.' for _ in range(5)] for _ in range(5)]
        for p,b in space[l].items():
            if b == 1:
                out[p[0]][p[1]] = '#'
        out[2][2] = 'o'
        print("layer: ",l)
        for line in out:
            print(''.join(line))
        print()
    print("bugs: ",bugs)

    

neighs = {
    (0,0):((0,1,0),(1,0,0)                 , (2,1,-1),(1,2,-1)),
    (0,1):((0,2,0),(1,1,0),(0,0,0)         , (1,2,-1)),
    (0,2):((0,3,0),(1,2,0),(0,1,0)         , (1,2,-1)),
    (0,3):((0,4,0),(1,3,0),(0,2,0)         , (1,2,-1)),
    (0,4):((1,4,0),(0,3,0)                 , (2,3,-1),(1,2,-1)),
    (1,0):((0,0,0),(1,1,0),(2,0,0)         , (2,1,-1)),
    (1,1):((2,1,0),(1,0,0),(0,1,0),(1,2,0)),
    (1,2):((1,1,0),(0,2,0),(1,3,0)         , (0,0,+1),(0,1,+1),(0,2,+1),(0,3,+1),(0,4,+1)),
    (1,3):((2,3,0),(1,2,0),(0,3,0),(1,4,0)),
    (1,4):((2,4,0),(1,3,0),(0,4,0)         , (2,3,-1)),
    (2,0):((3,0,0),(2,1,0),(1,0,0)         , (2,1,-1)),
    (2,1):((3,1,0),(2,0,0),(1,1,0)         , (0,0,+1),(1,0,+1),(2,0,+1),(3,0,+1),(4,0,+1)),

    (2,3):((1,3,0),(2,4,0),(3,3,0)         , (0,4,+1),(1,4,+1),(2,4,+1),(3,4,+1),(4,4,+1)),
    (2,4):((3,4,0),(2,3,0),(1,4,0)         , (2,3,-1)),
    (3,0):((2,0,0),(3,1,0),(4,0,0)         , (2,1,-1)),
    (3,1):((4,1,0),(3,0,0),(2,1,0),(3,2,0)),
    (3,2):((3,3,0),(4,2,0),(3,1,0)         , (4,0,+1),(4,1,+1),(4,2,+1),(4,3,+1),(4,4,+1)),
    (3,3):((4,3,0),(3,2,0),(2,3,0),(3,4,0)),
    (3,4):((4,4,0),(3,3,0),(2,4,0)         , (2,3,-1)),
    (4,0):((4,1,0),(3,0,0)                 , (3,2,-1),(2,1,-1)),
    (4,1):((4,0,0),(3,1,0),(4,2,0)         , (3,2,-1)),
    (4,2):((4,1,0),(3,2,0),(4,3,0)         , (3,2,-1)),
    (4,3):((4,2,0),(3,3,0),(4,4,0)         , (3,2,-1)),
    (4,4):((4,3,0),(3,4,0)                 , (2,3,-1),(3,2,-1)),
}

#print(sum(len(n) for n in neighs))
#exit()

def iterate(g):
    h = defaultdict(empty)
    g[min(g)-1]
    g[max(g)+1]
    for l in list(g):
        for p,b in g[l].items():
            if p == (2,2):
                continue
            s = sum( g[l+d][(x,y)] for (x,y,d) in neighs[p] )
            if g[l][p] == 1:
                h[l][p] = 0 if s!= 1 else 1
            else:
                h[l][p] = 1 if 0<s and s<3 else 0
    for l in sorted(h):
        if sum(h[l].values()) == 0:
            del(h[l])
        else:
            break
    for l in reversed(sorted(h)):
        if sum(h[l].values()) == 0:
            del(h[l])
        else:
            break
    return h

    
space = defaultdict(empty)
rows = [line.strip() for line in sys.stdin.readlines()]
space.update( {0:{(r,c):int(b) for r,row in enumerate(rows) for c,b in enumerate(row)}} )

i = 0
while i<int(sys.argv[1]):
    #print(f"####### iteration {i} #######")
    #pspace(space)
    space = iterate(space)
    i += 1

print(f"####### iteration {i} #######")
pspace(space)
