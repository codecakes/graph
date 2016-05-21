from collections import defaultdict, deque

def rec_edge(G, E, Elo, Ehi):
    # populates Adjacent List that contains each vertex conenccted to its immediate vertices
    Emid = (Elo+Ehi)/2
    # O(lgE)
    if Elo<Ehi:
        rec_edge(G, E, Elo, Emid)
        rec_edge(G, E, Emid+1, Ehi)
    else:
        v1,v2 = E[Elo]
        G.addEdge(v1, v2)

def dfs(G, src_node, marked, path_from):
    # path_from = [None] * len(G.V)
    marked = marked or {}
    for connected_node in G[src_node]:
        if marked.get(connected_node, 0) == 0:
            path_from[connected_node] = src_node
            dfs(G, connected_node, marked, path_from)
    marked[src_node] = 1
    return

def bfs(G, src_node, marked, path_from):
    Q = deque([src_node], len(G.V))
    node = None
    while Q:
        node = Q.pop()
        marked[node] = 1
        for connected_node in G[node]:
            if marked.get(connected_node, 0) == 0:
                path_from[connected_node] = node
                Q.appendleft(connected_node)
    return


class Graph(object):

    L = list
    def __init__(self, V=None, E=None):
        self.V = V or []
        self.E = defaultdict(L)
        # populate graph
        if E:
            rec_edge(self, E, 0, len(self.E)-1)

    def __getitem__(self, v):
        return self.E[v]

    def addEdge(self, v, w):
        self[v].append(w)
        self[w].append(v)

    def __iter__(self):
        if self.E:
            for v in self.E:
                yield v
        else:
            return


