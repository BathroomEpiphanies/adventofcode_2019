#!/usr/bin/python3

import re
import sys
import json

moons = []
for line in (x.strip() for x in sys.stdin.readlines()):
    match = re.findall('=([-\d]+)',line)
    x,y,z = [int(i) for i in match]
    #print(x,y,z)

    moons.append([[x,y,z],[0,0,0],[0]])


vector = [
     -6, -5,  -8   ,   0,0,0 ,
      0, -3, -13   ,   0,0,0 ,
    -15, 10, -11   ,   0,0,0 ,
     -3, -8,   3   ,   0,0,0 ,
]

matrix = [
    

print(moons)
states={}



time=0
loops = 10
loop=0
while True:
    loop += 1
    #energy = sum([m[2][0] for m in moons])
    #print(f"time: {time}: energy {energy}")
    state = tuple([tuple(x) for x in moons[0][0:2]])
    #print(state)
    if state in states:
        print(state)
        print(moons)
        print(f"time: {time}, came back to time {states[state]}")
        if loop>loops:
            break
    states.update({state:time})
    #states.add(state)
    #print(json.dumps(moons,indent=2))
    for i in range(0,len(moons)):
        for j in range(i+1,len(moons)):
            m1,m2 = moons[i],moons[j]
            if   m2[0][0]>m1[0][0]:
                 m1[1][0] +=  1
                 m2[1][0] += -1
            elif m2[0][0]<m1[0][0]:
                 m1[1][0] += -1
                 m2[1][0] +=  1
            if   m2[0][1]>m1[0][1]:
                 m1[1][1] +=  1
                 m2[1][1] += -1
            elif m2[0][1]<m1[0][1]:
                 m1[1][1] += -1
                 m2[1][1] +=  1
            if   m2[0][2]>m1[0][2]:
                 m1[1][2] +=  1
                 m2[1][2] += -1
            elif m2[0][2]<m1[0][2]:
                 m1[1][2] += -1
                 m2[1][2] +=  1
    for m in moons:
        m[0][0] += m[1][0]
        m[0][1] += m[1][1]
        m[0][2] += m[1][2]
        #m[2][0]  = (abs(m[0][0])+abs(m[0][1])+abs(m[0][2]))*(abs(m[1][0])+abs(m[1][1])+abs(m[1][2]))
    time += 1

    
