# Implementation by Nikolaj Munk Binder Jensen (nimj@itu.dk)

from collections import deque

class FlowEdge:
    def __init__(self, source, target, weight):
        self.source = source
        self.target = target
        self.weight = weight
    
    def __repr__(self):
        return f'{self.source}->{self.target}: {self.weight}'

class NetworkFlow:
    def __init__(self):
        self.adj = {}
        self.edges = set()
        self.flow = {}
    
    def add_edge(self, source, target, weight):
        # create "real" edge
        if source not in self.adj:
            self.adj[source] = []
        edge = FlowEdge(source, target, weight)
        # create reverse edge
        if target not in self.adj:
            self.adj[target] = []
        edge_reverse = FlowEdge(target, source,  0)

        # link edges
        edge.reverse = edge_reverse
        edge_reverse.reverse = edge

        # add to collections
        self.adj[source].append(edge)
        self.edges.add(edge)
        self.adj[target].append(edge_reverse)

        # initialize with zero flow
        self.flow[edge] = 0
        self.flow[edge_reverse] = 0

        return edge
    
    def get_flow(self, edge):
        return self.flow[edge]
    
    def get_edges(self, vert):
        return self.adj[vert]
    
    def residual(self, edge):
        return edge.weight - self.flow[edge]
    
    def find_path(self, s, t, path, visited, threshold=1):
        q = deque()
        q.append(s)
        p = {}
        visited.add(s)
        while q:
            node = q.popleft()
            if node == t:
                mypath = [p[t]]
                while mypath[-1].source != s:
                    mypath.append(p[mypath[-1].source])
                mypath.reverse()
                return mypath
            for edge in self.get_edges(node):
                if edge.target in visited: continue
                residual = self.residual(edge)
                if residual >= threshold:
                    visited.add(edge.target)
                    p[edge.target] = edge
                    q.append(edge.target)
        return None
    
    def augment(self, path):
        b = min(self.residual(edge) for edge in path)
        for edge in path:
            self.flow[edge] += b
            self.flow[edge.reverse] -= b
    
    def max_flow(self, s, t):
        # set scaling parameter
        capacity_max = max(edge.weight for edge in self.get_edges(s))
        delta = 1 if capacity_max == 0 else 2**(capacity_max//2).bit_length()
        while delta >= 1:
            while P:= self.find_path(s,t,[],set(),delta):
                self.augment(P)
            delta /= 2
        return sum(self.get_flow(edge) for edge in self.get_edges(s))
    
    def get_active_edges(self, source = None):
        coll = self.edges if source is None else self.get_edges(source)
        return [edge for edge in coll if self.flow[edge] > 0]
    
    def reset(self):
        for edge in self.flow.keys():
            self.flow[edge] = 0
