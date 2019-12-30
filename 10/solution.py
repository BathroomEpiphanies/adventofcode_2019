#!/usr/bin/python3



import sys
import json
from math import gcd, atan2, pi
from collections import OrderedDict

def sub(a,b):
    return (a[0]-b[0],a[1]-b[1])

def div(a,k):
    return (a[0]//k,a[1]//k)

def norm2(a):
    return a[0]*a[0]+a[1]*a[1]
    
def unify(a):
    g = gcd(a[0],a[1])
    #print( a, g )
    if g > 1:
        return div(a,g)
    else:
        return a

asteroids = []
for y,line in enumerate(sys.stdin.readlines()):
    for x,position in enumerate(line):
        if position == '#':
            asteroids.append((x,y))

#print(asteroids)
visible_count = []

for origin in asteroids:
    vectors = [sub(origin,asteroid) for asteroid in asteroids if asteroid!=origin]
    directions = [unify(v) for v in vectors]
    visible_count.append( {'position':origin,'count':len(set(directions))} )

visible_count.sort(key=lambda x: -x['count'])    
print(visible_count[0])
print()


origin = (x,y) = visible_count[0]['position']
asteroids.remove(origin)
vectors = [sub(origin,asteroid) for asteroid in asteroids]
directions = [ unify(s) for s in vectors ]

field = dict()

for vector,direction,asteroid in zip(vectors,directions,asteroids):
    if direction not in field:
        field[direction] = {}
        tmp = (270+180/pi*atan2(vector[1],vector[0]))
        field[direction]['angle'] = tmp if tmp < 360 else tmp-360
        field[direction]['norm'] = direction
        field[direction]['list'] = []
    field[direction]['list'].append( {'dist':norm2(vector), 'position':asteroid } ) 

for key,value in field.items():
    value['list'].sort(key=lambda x: x['dist'])
# Sort reversed for safe popping
field = sorted(field.values(),key=lambda x: -x['angle'])

count = 0
while field:
    for index,direction in zip(reversed(range(len(field))),reversed(field)):
        count += 1
        print(f"{count: 3d} {direction['angle']: 7.2f} {direction['list'].pop(0)}")
        if not direction['list']:
            field.pop(index)
