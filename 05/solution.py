#!/usr/bin/python3

import sys
from intmachine import Machine

with open(sys.argv[1],'r') as program:
    memory = [int(x) for x in program.readline().strip().split(',')]

machine = Machine(memory.copy())
machine.stdin.put(1)
machine.start()
machine.join()
print(machine.out.get())

machine = Machine(memory.copy())
machine.stdin.put(5)
machine.start()
machine.join()
print(machine.out.get())
