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
import flow.NetworkFlow as nf


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

def problem_some(V, E, R, s, t):
    if s in R or t in R:
        return True # TODO only if there is a path from s to t
    if is_directed:
        graph = Digraph(n)
        for u, v in E:
            graph.add_edge(indexes[u], indexes[v])
        cycle = DirectedCycle(graph)
        if cycle.has_cycle():
            return "?!" # NP-hard in general on directed graphs
        bfs_source = BreadthFirstPaths(G, indexes[s])
        for r in R:
            bfs_r = BreadthFirstPaths(G, indexes[r])
            if bfs_source.has_path_to(indexes[r]) and bfs_r.has_path_to(indexes[t]):
                return True
        return False

    flow_network, flow_sink = some_convert_to_directed_flow(E, s)
    for r in R:
        r_out = indexes[r] * 2 + 1
        if(flow_network.max_flow(r_out, flow_sink) == 2):
            return True
        flow_network.reset()
    return False

def some_convert_to_directed_flow(E, s):
    # By convention, the in-vertex v is at index 2v, and the
    # out-vertex is at index 2v+1.
    # The sink of the flow network is at the last index
    graph = nf.NetworkFlow()
    for u,v in E:
        graph.add_edge(indexes[u]*2+1, indexes[v]*2, 1)
        graph.add_edge(indexes[v]*2+1, indexes[u]*2, 1)

    # Add the edges in->out 
    for v in range(n):
        graph.add_edge(2 * v, 2 * v + 1, 1)

    flow_sink = n * 2
    graph.add_edge(indexes[s], flow_sink, 1)
    graph.add_edge(indexes[s], flow_sink, 1)

    return graph, flow_sink
