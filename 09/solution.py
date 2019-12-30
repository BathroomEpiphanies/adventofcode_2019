#!/usr/bin/python3

import sys
from intcode import Machine

with open(sys.argv[1],'r') as program:
    original = [ int(x) for x in f"{program.readline().strip()},0,0".split(',') ]

memory = original.copy()
machine = Machine( memory , verbose=True , name='' , initial=[1] )
machine.run()

memory = original.copy()
machine = Machine( memory , verbose=True , name='' , initial=[2] )
machine.run()
