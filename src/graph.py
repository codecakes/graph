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
class dfsDecorate(object):

    def __init__(self, attr, cid):
        self.attr = attr
        self.cid = cid
        self.f = None
        self.src_node = self.attr['vid']

    def __call__(self, f):
        self.f = f
        def wrap(*args):
            G, src_node, marked, path_from = args
            self.cid[src_node] = self.src_node
            self.f(*args)
        return wrap

# see dfsDecorate above
# def dfs_connected(fn, attrStore = None):
#     cid = attrStore['cid']
#     vid = attrStore['vid']
#     def closure(*args):
#         G, src_node, marked, path_from, _ = args
#         cid[src_node] = vid
#         # dfs(G, src_node, marked, path_from)
#         fn(G, src_node, marked, path_from)
#     return closure

# TODO: Convert this into a class like https://stackoverflow.com/questions/37393287/optionally-use-decorators
class dfsClass(object):

    def __init__(self, attr, decoBool):
        self.attr = attr
        self.cid = attr['cid']
        self.decoBool = decoBool

    def __call__(self, *args):
        if self.decoBool:
            fn = dfsDecorate(self.attr, self.cid)
            fn = fn(self.dfs)
            return fn(*args)
        else:
            return fn(*args)

    def dfs(self, G, src_node, marked, path_from):
        '''depth first search on a graph'''
        # path_from = [None] * len(G.V)
        # marked = marked or {}
        for connected_node in G[src_node]:
            if marked.get(connected_node, 0) == 0:
                path_from[connected_node] = src_node
                # dfs(G, connected_node, marked, path_from)
                dfs = dfsClass(self.attr, self.decoBool)
                dfs(G, connected_node, marked, path_from)
        marked[src_node] = 1
        return

def dfsFn(G, src_node, marked, path_from, attrStore, decoBool=True):
    dfs = dfsClass(attrStore, decoBool)
    # like @dfs_connected but do it manually
    # dfs = dfs_connected(dfs, attrStore)
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
    ln = len(G.V)
    # stores incoming edge. from index value(vertex, where it is coming from) to index(target vertex)
    path_from = [None] * ln
    # stores the original vertex of a singly connected graph component to which vertex/node v_i belongs to in v_i index
    cid = [None] * ln
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

L = list

class Graph(object):

    def __init__(self, V=None, E=None):
        self.V = V or []
        self.E = defaultdict(L)
        self.cid = None
        self.connected_path_from = None
        self.edges = E


    def populate_graph(self):
        if self.edges:
            rec_edge(self, self.edges, 0, len(self.edges)-1)

    def find_connected_path(self):
        if self.edges:
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


class DiGraph(Graph):

    def addEdge(self, srcNode, targetNode):
        self[srcNode].append(targetNode)
