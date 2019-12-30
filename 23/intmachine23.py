#!/usr/bin/python3 -u

import queue

import multiprocessing
import sys

class Machine(multiprocessing.Process):

    def verbose_message(self,message):
        if self.verbose:
            print( f"{self.name} {self.pointer: 5d} {self.memory[self.pointer]:05d} {message}", file=sys.stderr )
    
    def __init__(self, memory=['99'], verbose=False, name='', stdin=None, stdout=None, stderr=None):
        super().__init__()
        self.pointer = 0
        self.relative = 0
        self.halt = False
        self.memory = memory
        self.verbose = verbose
        self.name = name
        self.stdin = multiprocessing.Queue() if stdin is None else stdin
        self.stdout = multiprocessing.Queue() if stdout is None else stdout
        self.stderr = multiprocessing.Queue() if stderr is None else stderr
        self.out = multiprocessing.Queue()
        self.final = None
        #print(f"program {self.name} length: {len(self.memory)}, stdin={self.stdin}, stdout={self.stdout}" , file=sys.stderr)

    def memget(self,pos):
        while pos >= len(self.memory):
            self.memory.extend([0]*len(self.memory))
            self.verbose_message(f"extending memory to length {len(self.memory)}")
        return self.memory[pos]
    def memset(self,pos,n):
        while pos >= len(self.memory):
            self.memory.extend([0]*len(self.memory))
            self.verbose_message(f"extending memory to length {len(self.memory)}")
        self.memory[pos] = n

    
    def halt(self,c,b,a,x,y,z):
        self.verbose_message( f"Halting" )
        self.out.put(self.final)
        self.stdout.put(None)
        self.halt = True
    
    def sto(self,c,b,a,x,y,z):
        X = (x if a==0 else x+self.relative)
        try:
            self.memset(X,int(self.stdin.get(False)))
        #except Exception as e:
        except queue.Empty:
            self.memset(X,-1)
        #print( f"{self.name}: memory[{x}] = {self.memget(x)}" )
        self.verbose_message( f"memory[{x}] = {self.memget(x)}" )
        self.pointer += 2
    def out(self,c,b,a,x,y,z):
        X = (self.memget(x) if a==0 else (x if a==1 else self.memget(x+self.relative)))
        #print( f"{self.name}: output = {x}" )
        self.verbose_message( f"print({X})" )
        self.stdout.put(X,True)
        self.final = X
        self.pointer += 2
    
    def add(self,c,b,a,x,y,z):
        X = (self.memget(x) if a==0 else (x if a==1 else self.memget(x+self.relative)))
        Y = (self.memget(y) if b==0 else (y if b==1 else self.memget(y+self.relative)))
        Z = (z if c==0 else z+self.relative)
        self.memset( Z , X+Y )
        self.verbose_message( f"memory[{z}] = {X}+{Y} = {X+Y}" )
        self.pointer += 4
    def mul(self,c,b,a,x,y,z):
        X = (self.memget(x) if a==0 else (x if a==1 else self.memget(x+self.relative)))
        Y = (self.memget(y) if b==0 else (y if b==1 else self.memget(y+self.relative)))
        Z = (z if c==0 else z+self.relative)
        self.memset( Z , X*Y )
        self.verbose_message( f"memory[{z}] = {X}*{Y} = {X*Y}" )
        self.pointer += 4

    def lt (self,c,b,a,x,y,z):
        X = (self.memget(x) if a==0 else (x if a==1 else self.memget(x+self.relative)))
        Y = (self.memget(y) if b==0 else (y if b==1 else self.memget(y+self.relative)))
        Z = (z if c==0 else z+self.relative)
        self.memset( Z , 1 if X<Y else 0 )
        self.verbose_message( f"memory[{z}] = {X}<{Y} = {self.memget(z)}" )
        self.pointer += 4
    def eq (self,c,b,a,x,y,z):
        X = (self.memget(x) if a==0 else (x if a==1 else self.memget(x+self.relative)))
        Y = (self.memget(y) if b==0 else (y if b==1 else self.memget(y+self.relative)))
        Z = (z if c==0 else z+self.relative)
        self.memset( Z , 1 if X==Y else 0 )
        self.verbose_message( f"memory[{z}] = {X}=={Y} = {self.memget(z)}" )
        self.pointer += 4
    
    def jtr(self,c,b,a,x,y,z):
        X = (self.memget(x) if a==0 else (x if a==1 else self.memget(x+self.relative)))
        Y = (self.memget(y) if b==0 else (y if b==1 else self.memget(y+self.relative)))
        self.verbose_message( f"jumping to {Y}" if X!=0 else f"skipping jump" )
        self.pointer = Y if X!=0 else self.pointer+3
    def jfa(self,c,b,a,x,y,z):
        X = (self.memget(x) if a==0 else (x if a==1 else self.memget(x+self.relative)))
        Y = (self.memget(y) if b==0 else (y if b==1 else self.memget(y+self.relative)))
        self.verbose_message( f"jumping to {Y}" if X==0 else f"skipping jump" )
        self.pointer = Y if X==0 else self.pointer+3
    
    def rel(self,c,b,a,x,y,z):
        X = (self.memget(x) if a==0 else (x if a==1 else self.memget(x+self.relative)))
        self.relative += X
        self.verbose_message( f"relative base += {X}, is now {self.relative}" )
        self.pointer += 2
    
    def inget(self,a,b):
        pass
    
    instructions = {
         1: add,       # Addition
         2: mul,       # Multiplication
         3: sto,       # Store
         4: out,       # Output
         5: jtr,       # Jump on true
         6: jfa,       # Jump on false
         7: lt,        # Less than
         8: eq,        # Equal
         9: rel,       # Relative base
        99: halt       # Exit
    }

    def run(self):
        while not self.halt:
            c = self.memget(self.pointer)         // 10000
            b = self.memget(self.pointer) % 10000 //  1000
            a = self.memget(self.pointer) %  1000 //   100
            o = self.memget(self.pointer) %   100
            x = self.memget(self.pointer+1)
            y = self.memget(self.pointer+2)
            z = self.memget(self.pointer+3)
            #print(f"m={self.memory[self.pointer]} c={c} b={b} a={a} o={o} x={x} y={y} z={z}")
            self.instructions[o]( self,c,b,a,x,y,z )
