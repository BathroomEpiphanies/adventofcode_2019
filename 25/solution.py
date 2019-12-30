#!/usr/bin/python3 -u

import time
from intmachine import Machine
import sys
from multiprocessing import Queue
from multiprocessing import Process


with open(sys.argv[1],'r') as program:
    memory = [int(x) for x in program.readline().strip().split(',')]
verbose = len(sys.argv) > 2 and sys.argv[2]=='verbose'


def feed(machine):
    last = 0
    y = -6
    while True:
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
            print(f"hull damage: {last}")
            return


machine = Machine(memory.copy(),verbose=False)
p = Process(target=feed,args=(machine,))
p.start()
machine.start()


solution = [
    "south",
    "take mouse",
    "north",
    "west",
    "north",
    "west",
    "south",
    "take hypercube",
    "north",
    "east",
    "north",
    "west",
    "take semiconductor",
    "east",
    "south",
    "south",
    "west",
    "take antenna",
    "west",
    "south",
    "south",
    "south"
]

while True:
    line = sys.stdin.readline()
    for c in line:
        machine.stdin.put(ord(c))

for line in solution:
    for c in line:
        machine.stdin.put(ord(c))
    machine.stdin.put(ord('\n'))

machine.join()
machine.terminate()

