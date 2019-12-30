#!/usr/bin/python3

import sys

lower,upper = map(int, sys.stdin.readline().split('-'))
count = 0
for i in range(lower,upper+1):
    s = str(i)
    t = True
    u = False
    r = 1
    for j in range(1,6):
        if s[j] < s[j-1]:
            t = False
            break
        elif s[j] == s[j-1]:
            r += 1
        else:
            if r == 2:
                u = True
            r = 1
    if r == 2:
        u = True
    if t and u:
        print(i)
        count += 1

print(count)
