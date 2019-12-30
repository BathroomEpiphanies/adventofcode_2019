#!/usr/bin/python3

import sys


def fuel_needed( mass ):
    total = 0
    increment = mass//3-2
    while increment > 0:
        total += increment
        increment = increment//3-2
    return total



# dec_01 star1
#print( sum( [ x//3-2 for x in sys.stdin.readlines() ] ) )

# dec_01 star2
print(sum((fuel_needed(int(x)) for x in sys.stdin.readlines())))
