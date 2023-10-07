from itertools import count
from heapq import heappush, heappop


class Graph:
    def __init__(self, size: int):
        self.adj = [[] for _ in range(size)]
        self.V = size

    def add_edge(self, u, v, w):
        self.adj[v].append((u, w))
        self.adj[u].append((v, w))

    def shortest_path(self, sources, dest):
        dist = {}
        seen = {}

        c = count()
        fringe = []

        for source in sources:
            seen[source] = 0
            heappush(fringe, (0, next(c), source))

        while fringe:
            (d, _, v) = heappop(fringe)
            if v in dist:
                continue
            dist[v] = d
            if v == dest:
                break
            for u, w in self.adj[v]:
                vu_dist = dist[v] + w
                if u not in seen or vu_dist < seen[u]:
                    seen[u] = vu_dist
                    heappush(fringe, (vu_dist, next(c), u))

        return dist


if __name__ == "__main__":
    V = 9
    g = Graph(V)

    g.add_edge(0, 1, 4)
    g.add_edge(0, 7, 8)
    g.add_edge(1, 2, 8)
    g.add_edge(1, 7, 11)
    g.add_edge(2, 3, 7)
    g.add_edge(2, 8, 2)
    g.add_edge(2, 5, 4)
    g.add_edge(3, 4, 9)
    g.add_edge(3, 5, 14)
    g.add_edge(4, 5, 10)
    g.add_edge(5, 6, 2)
    g.add_edge(6, 7, 1)
    g.add_edge(6, 8, 6)
    g.add_edge(7, 8, 7)

    print(g.shortest_path([0], 7))
