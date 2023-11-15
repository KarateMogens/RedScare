from itu.algs4.graphs.graph import *
from itu.algs4.graphs.digraph import *
from itu.algs4.graphs.edge_weighted_digraph import *
from itu.algs4.graphs.dijkstra_sp import *
from itu.algs4.graphs.directed_edge import *
from itu.algs4.graphs.cycle import *
from itu.algs4.graphs.directed_cycle import *
from itu.algs4.graphs.edge_weighted_directed_cycle import *
from itu.algs4.graphs.breadth_first_paths import *
from itu.algs4.graphs.bellman_ford_sp import *
from itu.algs4.graphs.acyclic_lp import *


n, m, r = (int(x) for x in input().split())
s, t = input().split()
vertices = []
indexes = {}
red_vertices = set()
edges = []
is_directed = False

for i in range(n):
    line = input()
    name = line.split()[0]
    vertices.append(name)
    indexes[name] = i
    if line[-1] == '*':
        red_vertices.add(name)

for _ in range(m):
    u,edge,v = input().split()
    edges.append((u,v))
    if edge[-1] == '>':
        is_directed = True

def problem_none(V, E, R, s, t):
    graph = Digraph(n)
    
    for u,v in E:
        if v not in R or v == t:
            graph.add_edge(indexes[u], indexes[v])
        if not is_directed and (u not in R or u == t):
            graph.add_edge(indexes[v], indexes[u])
    
    path = BreadthFirstPaths(graph, indexes[s])
    if path.has_path_to(indexes[t]):
        return path.dist_to(indexes[t])
    return -1

def problem_alternate(V, E, R, s, t):

    graph = Digraph(n)

    for u,v in E:
        if (u not in R and v not in R) or (u in R and v in R):
            continue
        graph.add_edge(indexes[u],indexes[v])
        if not is_directed:
            graph.add_edge(indexes[v],indexes[u])
           
    path = BreadthFirstPaths(graph, indexes[s])
    if path.has_path_to(indexes[t]):
        return True
    return False

def problem_few(V, E, R, s, t):
    graph = EdgeWeightedDigraph(n)

    for u,v in E:
        weight = 1 if v in R else 0
        edge = DirectedEdge(indexes[u],indexes[v],weight)
        graph.add_edge(edge)
    
    sp = DijkstraSP(graph, indexes[s])
    if sp.has_path_to(indexes[t]):
        print(sp.path_to(indexes[t]))
        return int(sp.dist_to(indexes[t])) + (1 if s in R else 0)
    return -1

def problem_many(V, E, R, s, t):
    if not is_directed:
        graph = Graph(n)
        for u,v in E:
            graph.add_edge(indexes[u], indexes[v])
        cycle = Cycle(graph)
        if cycle.has_cycle():
            return '?!' # NP-hard on undirected non-trees
        bfs = BreadthFirstPaths(graph, indexes[s])
        if bfs.has_path_to(indexes[t]):
            p = bfs.path_to(indexes[t])
            return sum(V[v] in R for v in bfs.path_to(indexes[t]))
        return -1
    graph = EdgeWeightedDigraph(n)
    for u,v in E:
        edge = DirectedEdge(indexes[u], indexes[v], -1 if v in R else float('inf'))
        graph.add_edge(edge)
    dc = EdgeWeightedDirectedCycle(graph)
    if dc.has_cycle():
        return '?!' # NP-hard on directed graphs with a cycle
    
    sp = BellmanFordSP(graph, indexes[s])
    if sp.has_path_to(indexes[t]):
        return -int(sp.dist_to(indexes[t])) + (1 if s in R else 0)
    return -1
