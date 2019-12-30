#!/usr/bin/python3

import sys
from intmachine import Machine
from collections import defaultdict


turner = {
    ( 1, 0): {0:( 0, 1),1:( 0,-1)},
    ( 0, 1): {0:(-1, 0),1:( 1, 0)},
    (-1, 0): {0:( 0,-1),1:( 0, 1)},
    ( 0,-1): {0:( 1, 0),1:(-1, 0)}
}



with open(sys.argv[1],'r') as program:
    memory = [int(x) for x in program.readline().strip().split(',')]
verbose = len(sys.argv) > 2 and sys.argv[2]=='verbose'


for initial in [0,1]:
    steps = 0
    robot = Machine(memory.copy(),verbose=verbose)
    hull = defaultdict(lambda:0)
    position = (0,0)
    direction  = (0,1)
    hull[position] = initial
    
    robot.start()
    while True:
        steps += 1
        robot.stdin.put(hull[position])
        #robot.stdin.put(1)
        color = robot.stdout.get()
        if color is None:
            break
        turn = robot.stdout.get()
        hull[position] = color
        direction = turner[direction][turn]
        position = position[0]+direction[0],position[1]+direction[1]
    robot.terminate()
    
    xvals = sorted([position[0] for position in hull.keys()])
    yvals = sorted([position[1] for position in hull.keys()])
    xmin,xmax = xvals[0],xvals[-1]
    ymin,ymax = yvals[0],yvals[-1]
    
    output = [[' ' for i in range(xmin,xmax+1)] for j in range(ymin,ymax+1)]
    for position in hull:
        output[position[1]-ymin][position[0]-xmin] = '·' if hull[position] == 0 else '#'
    
    for row in reversed(output):
        print(''.join(row))
    print(f"robot painted {len(hull)} panels over {steps} steps")
