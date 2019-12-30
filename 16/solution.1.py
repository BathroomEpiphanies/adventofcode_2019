#!/usr/bin/python3

import sys
import numpy as np
import math

#orig = sys.stdin.readline().strip()
orig="12345678"
#line="80871224585914546619083218645595"
#line="19617804207202209144916044189917"
#line="69317163492948606335995924319873"

line=orig*int(sys.argv[1])
#print(len(line))

patterns=[]
for i in range(1,1+len(line)):
    k = math.ceil((len(line)+1)/i/4)
    #print(i,k)
    r = []
    r.extend([ 0 for j in range(i)])
    r.extend([ 1 for j in range(i)])
    r.extend([ 0 for j in range(i)])
    r.extend([-1 for j in range(i)])
    q = []
    for j in range(k):
        q.extend(r)
    patterns.append(q[1:len(line)+1])

for row in patterns:
    for n in row:
        print(f"{n:3d}",end='')
    print()


def mod(l):
    for i in range(len(l)):
        if l[i] < 0 and l[i]%10 != 0:
            l[i] = 10 - l[i]%10
        else:
            l[i] = l[i]%10
            
mes = np.array([int(x) for x in line])
mat = np.array(patterns)
#print(mes)
#print(mat)


for i in range(101):
    #print(i,''.join(mes.list()))
    print(f"{i: 4d}",end=' ')
    for n in mes:
        print(f"{n}",end='')
    print()
    mes = np.matmul(mat,mes)
    mod(mes)


#print(f"{int(sys.argv[1]): 4d}{' '*(10-int(sys.argv[1]))*len(orig)}",end=' ')
#for n in mes:
#    print(f"{n}",end='')
#print()
