#!/usr/bin/python3 -u

import sys
import json
from multiprocessing import Process
from intmachine import Machine



with open(sys.argv[1],'r') as program:
    memory = [int(x) for x in program.readline().strip().split(',')]

machine = Machine(memory.copy(),verbose=False)
machine.start()


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

p = Process(target=feed,args=(machine,))
p.start()



while True:
    line = sys.stdin.readline()
    for c in line:
        machine.stdin.put(ord(c))
        




machine.terminate()

exit()

# Star 1 input
# NOT A J
# NOT B T
# OR T J
# NOT C T
# OR T J
# AND D J
# WALK

# Star 2 input
# NOT A J
# NOT B T
# OR T J
# NOT C T
# OR T J
# AND D J
# NOT E T
# NOT T T
# OR H T
# AND T J
# RUN

