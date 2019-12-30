#!/usr/bin/python3 -u

import queue
from collections import deque
import time
import sys


grid = []
for line in sys.stdin.readlines():
    grid.append([ int(c) for c in line.strip()])
grid = tuple(tuple(c for c in r) for r in grid)

print(type(grid))
for r in grid:
    print(type(r))
    
def iterate(g):
    h = [[0 for _ in row] for row in g]
    for r in range(1,6):
        for c in range(1,6):
            s = sum( [g[r][c+1],g[r-1][c],g[r][c-1],g[r+1][c]] )
            if g[r][c] == 1:
                h[r][c] = 0 if s != 1 else 1
            else:
                h[r][c] = 1 if 0<s and s<3 else 0
    return tuple(tuple(c for c in r) for r in h)

def bio(g):
    b = 0
    p = 1
    for r in range(1,6):
        for c in range(1,6):
            if g[r][c]:
                b += p
            p = p*2
    return b

states = {}
i = 0
while grid not in states:
    print(i)
    for line in grid:
        print( ''.join(str(c) for c in line) )
    print()
    states.update({grid:i})
    grid = iterate(grid)
    i += 1

print(i,"=",states[grid])
for line in grid:
    print( ''.join(str(c) for c in line) )

print(bio(grid))
