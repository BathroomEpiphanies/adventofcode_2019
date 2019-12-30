#!/usr/bin/python3

import re
import sys
import json
from itertools import combinations

def add(a,b):
    return [ x+y for x,y in zip(a,b) ]
def sub(a,b):
    return [ x-y for x,y in zip(a,b) ]

def acc(a,b):
    for c in [0,1,2]:
        if   b[0][c]>a[0][c]:
            a[1][c] +=  1
            b[1][c] += -1
        elif b[0][c]<a[0][c]:
            a[1][c] += -1
            b[1][c] +=  1

def norm2(l):
    return sum([abs(c) for c in l])
def ene(m):
    return norm2(m[0])*norm2(m[1])

def hash(moons):
    return tuple([tuple([m[0][2],m[1][2]]) for m in moons])
    #return tuple([tuple(moons[1][0]),tuple(moons[1][1])])
    #return tuple(moons[0][0])
    #return tuple([tuple(x) for x in moons[0]])
    #return tuple([tuple(sub(m[1],moons[0][1])) for m in moons])
    #return tuple([tuple(sub(m[0],moons[0][0])) for m in moons])
    #return tuple( [tuple([tuple(x) for x in m]) for m in moons] )


moons = []
for line in (x.strip() for x in sys.stdin.readlines()):
    match = re.findall('=([-\d]+)',line)
    x,y,z = [int(i) for i in match]
    moons.append([[x,y,z],[0,0,0]])

print(moons)
time = 0
states = {}
print(hash(moons))

while True:
    state = hash(moons)
    #print(state)
    if state in states:
        print(f"hejhopp {time:8d}, {states[state]:8d}, {time-states[state]:8d}")
        #print(moons)
        #break
    states.update({state:time})

    for m1,m2 in combinations(moons,2):
        acc(m1,m2)
    for m in moons:
        m[0] = add(m[0],m[1])
    time += 1
    if time%1000000 == 0:
        print(time)
    
