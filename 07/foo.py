#!/usr/bin/python3

from operator import add,mul,lt,eq
from functools import partial
import sys
import re


pointer = 0
memory = [];
stdin = []
output = []
halt = -1

def noop(x,y,z):
    pass
def ex0(o,c,b,a,x,y,z):
    global halt
    print( f"exiting with 0", file=sys.stderr )
    halt = 0


def sto(o,c,b,a,x,y,z):
    global pointer
    memory[x] = int(stdin.pop())
    print( f"stored {memory[x]} in memory[{x}]", file=sys.stderr )
    pointer += 2
def out(o,c,b,a,x,y,z):
    global pointer
    global output
    print( f"outputting {x if a else f'memory[{x}]={memory[x]}'}", file=sys.stderr )
    output.append(memory[x])
    #print(memory[x])
    pointer += 2

def op(o,c,b,a,x,y,z):
    global pointer
    #print( f"a={a} , b={b} , c={c} , x={x} , y={y}, z={z}" , file=sys.stderr )
    print( f"memory[{z}] = {x if a else f'memory[{x}]={memory[x]}'} {o} {y if b else f'memory[{y}]={memory[y]}'}" , file=sys.stderr )
    memory[z] = o( x if a else memory[x], y if b else memory[y])
    pointer += 4

def jmp(o,c,b,a,x,y,z):
    global pointer
    print( f"jump to {y if b else f'memory[{y}]={memory[y]}'} if {x if a else f'memory[{x}]={memory[x]}'} is {o}" , file=sys.stderr )
    if ((x if a else memory[x]) != 0) == o:
        pointer = (y if b else memory[y])
    else:
        pointer += 3


def inget(a,b):
    pass
    
instructions = {
     1: partial(op,add),       # Addition        
     2: partial(op,mul),       # Multiplication  
     3: partial(sto,inget),    # Store           
     4: partial(out,inget),    # Output          
     5: partial(jmp,True),     # Jump on true    
     6: partial(jmp,False),    # Jump on false   
     7: partial(op,lt),        # Less than       
     8: partial(op,eq),        # Equal           
    99: partial(ex0,inget),    # Exit            
}


def run(code,inp):
    global stdin
    global memory
    global pointer
    global output
    global halt

    pointer = 0
    output = []
    halt = -1
    
    stdin=inp
    with open(code , 'r') as program:
        memory = [ int(x) for x in f"{program.readline().strip()},0,0".split(',') ]
        
    print( f"program length: {len(memory)}", file=sys.stderr )
    while halt < 0:
        c = memory[pointer]         // 10000
        b = memory[pointer] % 10000 //  1000
        a = memory[pointer] %  1000 //   100
        o = memory[pointer] %   100
        x = memory[pointer+1]
        y = memory[pointer+2]
        z = memory[pointer+3]
        print( f"{pointer: 5d} {memory[pointer]:05d}", end=' ' , file=sys.stderr )
        partial( instructions[o] , c,b,a )( x,y,z )
    return output[-1]

if __name__ == "__main__":
    run(sys.argv[1] , sys.argv[2].split(','))
    print(output[-1])
