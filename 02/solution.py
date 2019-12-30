#!/usr/bin/python3

from intcode import Machine

with open('input.in', 'r') as program:
    original = [ int(x) for x in f"{program.readline().strip()},0,0".split(',') ]


memory = original.copy()
memory[1] = 12
memory[2] = 2
machine = Machine(memory, verbose=True)
machine.run()
print(machine.memory[0])

for noun in range(100):
    for verb in range(100):
        memory  = original.copy()
        memory[1] = noun
        memory[2] = verb
        machine = Machine(memory, verbose=False)
        machine.run()
        if machine.memory[0]==19690720:
            print(noun,verb,machine.memory[0])
