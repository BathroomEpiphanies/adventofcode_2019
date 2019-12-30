#!/usr/bin/python3 -u

import sys
import re

from modular import zint
from matrix import matrix

partials = [line.strip() for line in sys.stdin.readlines()]

p = 119315717514047
N = -101741582076661
Zp = zint(p)
shuffle = matrix( ((Zp(1),Zp(0)),(Zp(0),Zp(1))) )
for tokens in (partial.split(' ') for partial in partials):
    if tokens[0] == 'cut':
        n = int(tokens[-1])
        shuffle = matrix(((1,-n),(0,1))) @ shuffle
    elif tokens[2] == 'increment':
        n = int(tokens[-1])
        shuffle = matrix(((n,0),(0,1))) @ shuffle
    elif tokens[3] == 'stack':
        shuffle = matrix(((-1,-1),(0,1))) @ shuffle
a1 = matrix(((2020,),(1,)))
aN = shuffle**N @ a1
print(f"star 2:\n{aN}")

exit()


partials = [line.strip() for line in sys.stdin.readlines()]


def sta():
    return matrix( ((-1,-1),(0,1)) )
def cut(n):
    return matrix( (( 1,-n),(0,1)) )
def inc(n):
    return matrix( (( n, 0),(0,1)) )



zp = zint(10007)
shuffle = matrix( ((zp(1),zp(0)),(zp(0),zp(1))) )
for line in partials:
    if re.search('stack',line):
        shuffle = sta() @ shuffle
    elif re.search('cut',line):
        n = int(line.split(' ')[-1])
        shuffle = cut(n) @ shuffle
    elif re.search('increment',line):
        n = int(line.split(' ')[-1])
        shuffle = inc(n) @ shuffle
print(shuffle,'\n')
p = matrix( ((zp(2019),),(zp(1),)) )
print(p,'\n')
p = shuffle @ p
print(p)
print(f"star 1: {int(p.matrix[0][0])}")


zp = zint(119315717514047)
N = 101741582076661
shuffle = matrix( ((zp(1),zp(0)),(zp(0),zp(1))) )
for line in partials:
    if re.search('stack',line):
        shuffle = sta() @ shuffle
    elif re.search('cut',line):
        n = int(line.split(' ')[-1])
        shuffle = cut(n) @ shuffle
    elif re.search('increment',line):
        n = int(line.split(' ')[-1])
        shuffle = inc(n) @ shuffle
print(shuffle,'\n')
shuffle = shuffle**-101741582076661
print(shuffle,'\n')
p = matrix( ((zp(2020),),(zp(1),)) )
print(p,'\n')
p = shuffle @ p
print(f"star 2: {int(p.matrix[0][0])}")
