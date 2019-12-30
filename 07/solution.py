#!/usr/bin/python3

import re
import sys
import itertools
import subprocess

from foo import run
best = 0
for permutation in itertools.permutations(range(0,5)):
    output = 0
    for i in permutation:
        output = run( sys.argv[1] , [output,i] )
        #print( output )
    if output > best:
        best = output
        print( permutation , best )
print( best )
    
max_val = 0
for permutation in itertools.permutations(range(5,10)):
    p0 = subprocess.Popen(
        [ "../05/solution.4.py","p0",sys.argv[1],f"{permutation[0]}",f"0" ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    p1 = subprocess.Popen(
        [ "../05/solution.4.py","p1",sys.argv[1],f"{permutation[1]}" ],
        stdin=p0.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    p2 = subprocess.Popen(
        [ "../05/solution.4.py","p2",sys.argv[1],f"{permutation[2]}" ],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    p3 = subprocess.Popen(
        [ "../05/solution.4.py","p3",sys.argv[1],f"{permutation[3]}" ],
        stdin=p2.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    p4 = subprocess.Popen(
        [ "../05/solution.4.py","p4",sys.argv[1],f"{permutation[4]}" ],
        stdin=p3.stdout,
        stdout=p0.stdin,
        stderr=subprocess.PIPE,
        #stdout=subprocess.PIPE
    )

    out,err = p4.communicate()

    #print("here",err,"there")

    value = int( re.findall('value=(\d+)',err.decode())[-1] )
    if value > max_val:
        max_val = value
        print( permutation , value )

    


    #for line in next(p4.stdout):
    #    print("line",line)
    #    #p0.communicate(input=line)
    #    p0.stdin.write(line)
    #    #p0.stdin.write(os.newline())
    #    
    #    #print( f"{line}\n" , file = p0.stdin )

