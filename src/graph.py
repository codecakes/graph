from collections import defaultdict, deque

def rec_edge(G, E, Elo, Ehi):
    # populates Adjacent List that contains each vertex connected to its immediate vertices
    Emid = (Elo+Ehi)/2
    # O(lgE)
    if Elo<Ehi:
        rec_edge(G, E, Elo, Emid)
        rec_edge(G, E, Emid+1, Ehi)
    else:
        v1,v2 = E[Elo]
        G.addEdge(v1, v2)

# dfs decorator
def dfs_connected(fn, attrStore = None):
    cid = attrStore['cid']
    vid = attrStore['vid']
    def closure(*args):
        G, src_node, marked, path_from, _ = args
        cid[src_node] = vid
        # dfs(G, src_node, marked, path_from)
        fn(G, src_node, marked, path_from)
    return closure

def dfs(G, src_node, marked, path_from):
    '''depth first search on a graph'''
    # path_from = [None] * len(G.V)
    marked = marked or {}
    for connected_node in G[src_node]:
        if marked.get(connected_node, 0) == 0:
            path_from[connected_node] = src_node
            dfs(G, connected_node, marked, path_from)
    marked[src_node] = 1
    return

def dfsFn(G, src_node, marked, path_from, attrStore):
    # like @dfs_connected but do it manually
    dfs = dfs_connected(dfs, attrStore)
    dfs(G, src_node, marked, path_from)

def connected_component(G):
    '''
    @params
        - G: the Graph instance
    @returns
        - cid: List of connected component ids
        - path_from: Vertiex index redirecting to where the edge came from
    '''
    marked = defaultdict(int)
    # stores where it is coming from
    path_from = [None] * len(G.V)
    # stores the original vertex of a singly connected graph component to which vertex/node v_i belongs to in v_i index
    cid = [None] * len(G.V)
    attrStore = {}
    attrStore['cid'] = cid
    for v in G:
        if not marked[v]:
            attrStore['vid'] = v
            cid[v] = v
            dfsFn(G, v, marked, path_from, attrStore)
    return cid, path_from

def is_connected_component(G,v,w):
    return (G.cid[v] == G.cid[w]) or has_edge(G, v, w)


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

# if there is an edge from v to w or is w in the list of nodes connected to v
def has_edge(G, v, w): return (w in G[v]) and (v in G[w])

class Graph(object):

    L = list
    def __init__(self, V=None, E=None):
        self.V = V or []
        self.E = defaultdict(L)
        self.cid = None
        self.connected_path_from = None
        # populate graph
        if E:
            rec_edge(self, E, 0, len(self.E)-1)
            self.cid, self.connected_path_from = connected_component(self)


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


