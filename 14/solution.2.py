#!/usr/bin/python3

from math import ceil
import sys
import re
import json
import matplotlib.pyplot as plt
#from networkx.drawing.nx_agraph import graphviz_layout

import networkx as nx


substances = {
    'ORE': {
        'gives':'ORE',
        'storage':1000000000000,
        'cost': 1,
        'output':1,
        'takes': {},
    }
}


for line in (x.strip() for x in sys.stdin.readlines()):
    matches = re.findall('\d+ \w+',line)
    out = matches[-1].split(' ')
    reaction = {
        'gives':out[1],
        'storage':0,
        'output':int(out[0]),
        'takes':{}
    }
    for match in matches[:-1]:
        inp = match.split(' ')
        reaction['takes'].update({inp[1]:int(inp[0])})
    substances.update({out[1]:reaction})

#print(json.dumps(substances,indent=2))

def produce(subst,amount):
    global substances
    #if subst == 'ORE':
    #    substances[subst]['storage'] -= amount
    #    return True

    have = substances[subst]['storage']
    need = amount - have
    order = ceil(need/substances[subst]['output'])
    if order > 0:
        success = subst != 'ORE'
        for input,cost in substances[subst]['takes'].items():
            success = success and produce(input,order*cost)
        if success:
            substances[subst]['storage'] += order*substances[subst]['output']
            substances[subst]['storage'] -= amount
            return True
        else:
            return False
    else:
        substances[subst]['storage'] -= amount
        return True




copy = json.loads(json.dumps(substances))
low = 0
high = 1000000000000
while low<high-1:
    substances = json.loads(json.dumps(copy))
    middle = (high+low)//2
    print(f"testing for {middle}",end=' ')
    if produce('FUEL',middle):
        low = middle
        print(f"success")
    else:
        high = middle
        print(f"fail")
