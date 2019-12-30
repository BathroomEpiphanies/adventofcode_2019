#!/usr/bin/python3

import networkx as nx
import sys
from intmachine import Machine

dirs = {
    'n': {'c':1, 'v':( 0, 1), 'r':'s'},
    's': {'c':2, 'v':( 0,-1), 'r':'n'},
    'w': {'c':3, 'v':(-1, 0), 'r':'e'},
    'e': {'c':4, 'v':( 1, 0), 'r':'w'}
}



    

def add(a,b):
    return (a[0]+b[0],a[1]+b[1])

with open(sys.argv[1],'r') as program:
    memory = [int(x) for x in program.readline().strip().split(',')]
machine = Machine(memory.copy(),verbose=False)
machine.start()

graph = nx.Graph()

oxpos = None
section = {}
def mappa(pos):
    global oxpos
    curr = section[pos]
    for d,v in dirs.items():
        if d not in curr['tested']:
            nxt = add(pos,v['v'])
            if nxt not in section:
                machine.stdin.put(v['c'])
                res = machine.stdout.get()
                item = {
                    nxt:{
                        'tested':set(['n','s','w','e']) if res==0 else set(),
                        'type':'#' if res == 0 else 'O' if res == 2 else '·',
                        'ancestor':v['r']
                    }
                }
                section.update(item)
                #if res != 0:
                #    graph.add_edge(pos,nxt)
                if res == 2:
                    oxpos = nxt
                if res != 0:
                    mappa(nxt)
            curr['tested'].add(d)
            if section[nxt]['type'] != '#':
                graph.add_edge(pos,nxt)

    if curr['ancestor'] is None:
        return
    else:
        machine.stdin.put(dirs[curr['ancestor']]['c'])
        machine.stdout.get()
        pos = add(pos,dirs[curr['ancestor']]['v'])


pos = (0,0)
item = {
    pos:{
        'tested':set(),
        'type':'^',
        'ancestor':None
    }
}
section.update(item)

try:
    mappa(pos)
except KeyboardInterrupt:
    pass

machine.terminate()    

xvals = sorted([position[0] for position in section.keys()])
yvals = sorted([position[1] for position in section.keys()])
xmin,xmax = xvals[0],xvals[-1]
ymin,ymax = yvals[0],yvals[-1]

output = [[' ' for i in range(xmin,xmax+1)] for j in range(ymin,ymax+1)]
for position in section:
    output[position[1]-ymin][position[0]-xmin] = section[position]['type']
    
for row in reversed(output):
    print(''.join(row))

#print(graph.edges())

print(f"Oxygen location: {oxpos}")
path = next( nx.shortest_simple_paths(graph,(0,0),oxpos) )
print(f"Shortest path to oxygen: {len(path)-1}")

dists = nx.single_source_shortest_path_length(graph,oxpos)
print(f"Time to refill oxygen: {max(dists.values())}")
