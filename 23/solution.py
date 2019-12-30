#!/usr/bin/python3 -u

import queue
from collections import deque
import time
from intmachine23 import Machine
import sys
from itertools import permutations
from multiprocessing import Queue


with open(sys.argv[1],'r') as program:
    memory = [int(x) for x in program.readline().strip().split(',')]
verbose = len(sys.argv) > 2 and sys.argv[2]=='verbose'

machines = [None for _ in range(255)]
stdout = Queue()
for i in range(50):
    machines[i] = Machine(memory.copy(),name=f"m{i:02d}",verbose=False)
    machines[i].stdin.put(i)

time.sleep(1)
for i in range(50):
    machines[i].start()
    print(f"started machine {i}")
    
nat = None
queues = [deque() for _ in range(256)]
lasty = None
idle = 0
while True:
    idle += 1
    for i in range(50):
        try:
            val = machines[i].stdout.get(False)
            idle = 0
            #print( f"read: {val: 10d} from machine: {i: 4d}" )
            queues[i].append(val)
        except queue.Empty:
            pass
    for i in range(50):
        if len(queues[i]) > 2:
            d = queues[i].popleft()
            x = queues[i].popleft()
            y = queues[i].popleft()
            if d > 254:
                print( f"setting nat to ({x: 10d},{y: 10d})" )
                nat = (x,y)
            else:
                print( f"sending ({x: 10d},{y: 10d}) to machine: {d: 4d}" )
                machines[d].stdin.put(x)
                machines[d].stdin.put(y)
                
    if idle > 2:
        idle = 0
        x,y = nat
        if y == lasty:
            print(f"nat sent {y} twice in a row")
            break
        else:
            lasty = y
        print( f"nat sending ({x: 10d},{y: 10d}) to machine: {0: 4d}" )
        machines[0].stdin.put(x)
        machines[0].stdin.put(y)
    if idle > 0:
        time.sleep(0.1)

print(nat)

for i in range(50):
    machines[i].terminate()

