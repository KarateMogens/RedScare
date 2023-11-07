from itu.algs4.graphs.graph import *
from itu.algs4.graphs.digraph import *
from itu.algs4.graphs.cycle import *
from itu.algs4.graphs.directed_cycle import *
from itu.algs4.graphs.breadth_first_paths import *


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




