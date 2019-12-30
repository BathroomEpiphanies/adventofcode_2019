#!/usr/bin/python3

import sys
import re
import json
import matplotlib.pyplot as plt
#from networkx.drawing.nx_agraph import graphviz_layout

import networkx as nx

reacts = nx.DiGraph()
labels = {}
edge_labels = {}
for line in (x.strip() for x in sys.stdin.readlines()):
    print()
    matches = re.findall('\d+ \w+',line)
    print(matches)
    out = matches[-1].split(' ')
    print("out",out)
    for match in matches[:-1]:
        print("match",match)
        inp = match.split(' ')
        print("inp",inp)
        reacts.add_edge(out[1],inp[1],weight=inp[0])
        labels.update({out[1]:out[1]})
        labels.update({inp[1]:inp[1]})
        edge_labels.update({(out[1],inp[1]):inp[0]})



print(reacts.edges())
#pos = nx.spring_layout(graphviz_layout(reacts))
pos = nx.spring_layout(reacts)

nx.draw(reacts,pos,labels=labels)
nx.draw_networkx_edge_labels(reacts,pos,edge_labels=edge_labels)
plt.show()
