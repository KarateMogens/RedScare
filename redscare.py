red_vertices = set()
n, m, r = (int(x) for x in input().split())
s, t = input().split()
vertices = []
edges = []
is_directed = False

for _ in range(n):
    line = input()
    name = line.split()[0]
    vertices.append(name)
    if line[-1] == '*':
        red_vertices.add(name)

for _ in range(m):
    u,edge,v = input().split()
    edges.append((u,v))
    if edge[-1] == '>':
        is_directed = True
