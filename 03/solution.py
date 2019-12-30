#!/usr/bin/python3

import json
import sys

segments1 = [b for b in sys.stdin.readline().split(',')]
segments2 = [b for b in sys.stdin.readline().split(',')]

def norm1(a):
    return abs(a[0]) + abs(a[1])

def generate_wire(segments):
    deltas = {
        'R': ( 1, 0),
        'U': ( 0, 1),
        'L': (-1, 0),
        'D': ( 0,-1),
    }
    wire = {}
    pos = (0,0)
    total = 0
    wire.update( {pos:total} )
    for segment in segments:
        delta = deltas[segment[0]]
        for i in range( int(segment[1:]) ):
            total += 1
            pos = ( pos[0]+delta[0] , pos[1]+delta[1] )
            if pos not in wire:
                wire.update( {pos:total} )
    return wire

wire1 = generate_wire( segments1 )
wire2 = generate_wire( segments2 )

intersections = []
for intersection in wire1.keys() & wire2.keys():
    intersections.append( { 'pos' : intersection , 'man' : norm1(intersection) , 'sum' : wire1[intersection] + wire2[intersection] } )




intersections.sort( key = lambda x: x['man'] )
print()
print("intersections" , intersections)
print( f"star1: { json.dumps(intersections[1]) }" )
intersections.sort( key = lambda x: x['sum'] )
print()
print("intersections" , intersections)
print( f"star2: { json.dumps(intersections[1]) }" )
