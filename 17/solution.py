#!/usr/bin/python3

import time
import sys
import os
from multiprocessing import Process
from intmachine import Machine

with open(sys.argv[1],'r') as program:
    memory = [int(x) for x in program.readline().strip().split(',')]
    
machine = Machine(memory.copy(),verbose=False)
machine.start()

tiles = {
    35: '#',
    46: '·',
    79: 'O',
}

scaffold = []
row = []
while True:
    tile = machine.stdout.get()
    if tile is None:
        break
    #print(chr(tile),end='')
    if tile == 10:
        scaffold.append(row)
        row = []
    else:
        row.append(chr(tile))
scaffold = scaffold[:-1]

alignment = 0
for y in range(1,len(scaffold)-1):
    for x in range(1,len(scaffold[y])-1):
        if scaffold[y  ][x  ] == '#' and \
           scaffold[y  ][x+1] == '#' and \
           scaffold[y-1][x  ] == '#' and \
           scaffold[y  ][x-1] == '#' and \
           scaffold[y+1][x  ] == '#':
            alignment += x*y
            scaffold[y][x] = 'O'

#for row in scaffold:
#    print(''.join(row))

print(f"alignment: {alignment}")



#machine = Machine(memory.copy(),verbose=True)
machine = Machine(memory.copy(),verbose=False)
machine.memory[0] = 2
machine.start()
#while True:
#    print(chr(machine.stdout.get()),end='')

def feed(machine):
    last = 0
    y = -6
    while True:
        time.sleep(0.1)
        os.system('clear')
        #print("hej")
        while y<len(scaffold)+1:
            tile = machine.stdout.get()
            if tile is None:
                return
            last = tile
            #print(f"tile ]{tile}[")
            if tile == 10:
                y += 1
            if tile<1000:
                print(chr(tile),end='')
            else:
                print(f"dust collected: {last}")
                return
        y = 0

p = Process(target=feed,args=(machine,))
p.start()

#machine.stdin.put(ord('y'))
#machine.stdin.put(10)

comma = ord(',')
#print(type(comma))
#print(f"comma ]{comma}[")

program = [
    "A,A,B,C,A,C,B,C,A,B\n",
    "L,4,L,10,L,6\n",
    "L,6,L,4,R,8,R,8\n",
    "L,6,R,8,L,10,L,8,L,8\n",
    "y\n"
]
for line in program:
    for c in line:
        machine.stdin.put(ord(c))

machine.join()


#while True:
    #line = sys.stdin.readline()
    #for c in line:
    #    machine.stdin.put(ord(c))
