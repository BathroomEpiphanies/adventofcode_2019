#!/usr/bin/python3 -u

import sys
import time
import multiprocessing
import numpy as np
import math
import scipy.special


line = sys.stdin.readline().strip()
print(f"read input of length: {len(line)}")
pos = int(line[0:7])
print(f"target pos is: {pos}")

print(f"creating vectors")
nums = [int(x) for i in range(10000) for x in line]
row = [1 if i>=pos else 0 for i in range(len(nums))]
#print(''.join([str(x) for x in row]))

print(len(nums))
print(len(row))

print(f"iterating round:",end='')
for i in range(99):
    print(f" {i}",end='')
    for j in range(pos,len(row)):
        row[j] = (row[j]+row[j-1])%10
print()

#print(''.join([str(x) for x in row]))
#print(''.join([str(x) for x in nums]))

message = ''
for i,p in enumerate(range(pos,pos+8)):
    total = 0
    for j in range(p,len(row)):
        total += row[j-i]*nums[j]
    print(f"message position: {i}, position in data:{p}, message bit: {total%10}")
    message += str(total%10)

print(f"message: {message}")
