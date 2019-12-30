#!/usr/bin/python3

import time
import os
import sys
import re
#from colections import DefaultDict
import json
import multiprocessing
from intmachine import Machine


tiles = {
    0: ' ',
    1: '#',
    2: 'o',
    3: '=',
    4: '·',
}

ballx = 0
bally = 0
paddx = 0

def init_field():
    blockcount = 0
    global ballx
    global bally
    global paddx
    temp = {}
    while True:
        x = machine.stdout.get()
        y = machine.stdout.get()
        t = machine.stdout.get()
        #print(x,y,t)
        if x == -1:
            score = t
            break
        if t == 2:
            blockcount += 1
        if t == 3:
            paddx = x
        if t == 4:
            ballx = x
            bally = y
        temp.update({(x,y):tiles[t]})
    xvals = [ p[0] for p in temp ]
    yvals = [ p[1] for p in temp ]
    xmin,xmax = xvals[0],xvals[-1]
    ymin,ymax = yvals[0],yvals[-1]
    field = [['·' for i in range(xmin,xmax+1)] for j in range(ymin,ymax+1)]
    for p,t in temp.items():
        field[p[1]-ymin][p[0]-xmin] = t
    print(f"blockcount: {blockcount}")
    return field
        
    
    
with open(sys.argv[1],'r') as program:
    memory = [int(x) for x in program.readline().strip().split(',')]
    
machine = Machine(memory.copy(),verbose=False)
machine.memory[0]=2
machine.start()

field = init_field()
score = 0
queue = multiprocessing.Queue()

def draw_field():
    global field
    os.system('clear')
    print(f"Score: {score}")
    for row in field:
        print(''.join(row))
    time.sleep(0.01)
def update_field():
    global machine
    global score
    global paddx
    global ballx
    global bally
    while True:
        x = machine.stdout.get()
        if x is None:
            draw_field()
            return None
        y = machine.stdout.get()
        t = machine.stdout.get()
        if x == -1:
            score = t
        else:
            field[y][x] = tiles[t]
        if t == 3:
            paddx = x
        if t == 4:
            ballx = x
            bally = y
            draw_field()
            return True



draw_field()
machine.stdin.put(-1)
update_field()
machine.stdin.put( 0)
update_field()
while True:
    #line = next(sys.stdin)
    if ballx < paddx:
        machine.stdin.put(-1)
    else:
        machine.stdin.put( 1)
    if None is update_field():
        break

machine.terminate()



    
        
