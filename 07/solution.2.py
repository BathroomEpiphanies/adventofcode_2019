#!/usr/bin/python3

from intmachine import Machine
import sys
from itertools import permutations

with open(sys.argv[1],'r') as program:
    memory = [int(x) for x in program.readline().strip().split(',')]
verbose = len(sys.argv) > 2 and sys.argv[2]=='verbose'

max_val = 0
for permutation in permutations([5,6,7,8,9]):

    m0 = Machine(memory.copy(),verbose=verbose,name='m0')
    m1 = Machine(memory.copy(),verbose=verbose,name='m1',stdin=m0.stdout)
    m2 = Machine(memory.copy(),verbose=verbose,name='m2',stdin=m1.stdout)
    m3 = Machine(memory.copy(),verbose=verbose,name='m3',stdin=m2.stdout)
    m4 = Machine(memory.copy(),verbose=verbose,name='m4',stdin=m3.stdout, stdout=m0.stdin)
    machines = [m0,m1,m2,m3,m4]
    
    for m,p in zip(machines,permutation):
        m.stdin.put(p)
        m.start()

    machines[0].stdin.put(0)
    machines[4].join()

    val = machines[4].out.get()
    if val > max_val:
        max_val = val
        print(permutation,val)

    for m in machines:
        m.terminate()
