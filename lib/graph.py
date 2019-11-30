import json


#
# graph:
#
# {
#   id1: {
#     edges: {
#       jd1:{},
#       jd2:{},
#       ...
#     }
#   },
#   id2: {
#     edges: {
#       jd1:{},
#       jd2:{},
#       ...
#     }
#   }
#   ...
# }
#

from collections import defaultdict
class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
            return ret


class Graph:
    
    def __init__(self):
        super().__init__()
        self.graph = {}
        self.timestamp = 0
        self.dot_layout = 'neato'
        self.dot_node_labels = keydefaultdict(lambda node:node)
        self.dot_node_colors = keydefaultdict(lambda _:'white')
        self.dot_edge_labels = keydefaultdict(lambda edge:self.graph[edge[0]]['edges'][edge[1]]['w'])
        self.dot_edge_colors = keydefaultdict(lambda _:'black')
    
    def __str__(self):
        return "\n".join( [f"{node}: {data}" for node,data in self.graph.items()] )
    
    def dot(self,dot_file):
        print( self.dot_edge_labels )
        with open(dot_file,'w') as output:
            print(f'strict digraph {{',file=output)
            print(f'graph [layout={self.dot_layout}];',file=output)
            for node in self.graph:
                print(f'{node} [style="filled", fillcolor="{self.dot_node_colors[node]}"];',file=output)
            doubles = set()
            for node1 in self.graph:
                for node2 in self.graph[node1]['edges']:
                    label = self.dot_edge_labels[(node1,node2)]
                    print(node1,node2,label)
                    if node1 in self.graph[node2]['edges'] and self.dot_edge_labels[(node2,node1)]==label:
                        if (node1,node2) in doubles:
                            continue
                        else:
                            print(f'{node1} -> {node2} [ label="{label}", dir="none"];',file=output)
                            doubles.add( (node2,node1) )
                    else:
                        print(f'{node1} -> {node2} [ label="{label}"];',file=output)

            print(f'}}', file=output )
        
        
    
    def add_node(self,a):
        if a not in self.graph:
            self.graph.update( {a:{'edges':{}}} )
        self.timestamp += 1
    
    def add_edge(self,a,b,**kwargs):
        self.add_node(a)
        self.add_node(b)
        if 'w' not in kwargs:
            kwargs.update({'w':1})
        self.graph[a]['edges'].update( {b:{**kwargs}} )
        self.graph[b]['edges'].update( {a:{**kwargs}} )
        self.timestamp += 1
    
    def del_node(self,a):
        for node in self.graph:
            del(graph[node]['edges'][a])
        del(graph[a])
        self.timestamp += 1
    
    def del_edge(self,a,b):
        del(graph[a]['edges'][b])
        del(graph[b]['edges'][a])
        self.timestamp += 1
    

    def dijkstra(self,source):
        if 'dijkstra_timestamp' not in self.graph[source] or \
           self.graph[source]['dijkstra_timestamp'] < self.timestamp:
            self._dijkstra(source)
        return self.graph[source]['dijkstra']
        
    def _dijkstra(self,source):
        from queue import PriorityQueue
        visited = {}
        queue = PriorityQueue()
        queue.put( (0,source,None) )
        while not queue.empty():
            distance,current,parent = queue.get()
            if current in visited:
                continue
            visited.update( {current:{'distance':distance,'parent':parent}} )
            for node,data in self.graph[current]['edges'].items():
                if node not in visited:
                    queue.put( (distance+data['w'],node,current) )
        self.graph[source]['dijkstra'] = visited
        self.graph[source]['dijkstra_timestamp'] = self.timestamp

    def distance(self,source,dest):
        distances = self.dijkstra(source)
        return distances[dest]['distance']
        
    def distances(self,source):
        dijkstra = self.dijkstra(source)
        return {node:dijkstra[node]['distance'] for node in dijkstra}
        
    def shortest_path(self,source,dest):
        visited = self.dijkstra(source)
        path = []
        current = dest
        while current is not None:
            path.append(current)
            current = visited[current]['parent']
        return list(reversed(path))
        
    
        







    
def main():
    graph = Graph()
    graph.add_node('a')
    graph.add_node('b')
    graph.add_edge('a','b')
    graph.add_edge('a','c')
    print(graph)
    pass

if __name__ == '__main__':
    main()
    
