#!/usr/bin/python3 -u

import sys
from intmachine import Machine

with open(sys.argv[1],'r') as program:
    memory = [int(x) for x in program.readline().strip().split(',')]
    

#summa = 0
#for y in range(50):
#    for x in range(50):
#        machine = Machine(memory.copy(),verbose=False)
#        machine.start()
#        machine.stdin.put(x)
#        machine.stdin.put(y)
#        out = machine.stdout.get()
#        summa += out
#        print(out,end='')
#        machine.terminate()
#    print()
#print(summa)
#exit()

def row_info(y,xmin,xmax):
    summa = 0
    x = xmin-1
    print(y,end='  ')
    while x < xmax:
        machine = Machine(memory.copy(),verbose=False)
        machine.start()
        machine.stdin.put(x)
        machine.stdin.put(y)
        out = machine.stdout.get()
        machine.terminate()
        summa += out
        print(out,end='')
        if out == 1:
            xmin = x
            x += 1
            break
        x += 1
    
    while x < xmax:
        machine = Machine(memory.copy(),verbose=False)
        machine.start()
        machine.stdin.put(x)
        machine.stdin.put(y)
        out = machine.stdout.get()
        machine.terminate()
        summa += out
        print(out,end='')
        if out != 1:
            xmax = x-1
            x += 1
            break
        x += 1
    print()
    return xmin,xmax,summa

#for y in range(50):
#    row_info(y,1,100)
#exit()


size = 100
y2 = 2160
y1 = y2 - size + 1

xstart = y2//10 * 7

y1x1,y1x2,_ = row_info(y1,xstart,10000)
y2x1,y2x2,_ = row_info(y2,xstart,10000)
while y1x2 - y2x1 < size - 1:
    y1x1,y1x2,_ = row_info(y1,y1x1,10000)
    y2x1,y2x2,_ = row_info(y2,y2x1,10000)
    print(y1,y2,y1x1,y1x2,y2x1,y2x2,"diff",y1x2-y2x1,"output",y2x1*10000+y1)
    y2 += 1
    y1 = y2 - size + 1
exit()


size = 3
y2 = 20
y1 = y2 - size + 1

xstart = 0

y1x1,y1x2,_ = row_info(y1,xstart,10000)
y2x1,y2x2,_ = row_info(y2,xstart,10000)
while y1x2 - y2x1 < size - 1:
    y1x1,y1x2,_ = row_info(y1,1,10000)
    y2x1,y2x2,_ = row_info(y2,1,10000)
    print(y1,y2,y1x1,y1x2,y2x1,y2x2,"diff",y1x2-y2x1,"output",y2x1*10000+y1)
    y2 += 1
    y1 = y2 - size + 1



#y = 1100
#xmin = 700
#xmax = 700
#while True:
#    summa = 0
#    x = xmin
#    print(y,end='  ')
#    while True:
#        machine = Machine(memory.copy(),verbose=False)
#        machine.start()
#        machine.stdin.put(x)
#        machine.stdin.put(y)
#        out = machine.stdout.get()
#        summa += out
#        print(out,end='')
#        if out == 1:
#            xmin = x
#            break
#        x += 1
#    while True:
#        machine = Machine(memory.copy(),verbose=False)
#        machine.start()
#        machine.stdin.put(x)
#        machine.stdin.put(y)
#        out = machine.stdout.get()
#        summa += out
#        print(out,end='')
#        if out != 1:
#            xmax = x
#            break
#        x += 1
#
#    if summa >= 100:
#        break
#    y += 1
#
#    print("   ",summa)
#
#print(y,summa)

#high
#17382074
