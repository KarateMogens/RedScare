red_vertices = set()
from itu.algs4.graphs.graph import *
from itu.algs4.graphs.digraph import *
from itu.algs4.graphs.cycle import *
from itu.algs4.graphs.directed_cycle import *
from itu.algs4.graphs.breadth_first_paths import *
n, m, r = (int(x) for x in input().split())
s, t = input().split()
vertices = []
indexes = {}
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
