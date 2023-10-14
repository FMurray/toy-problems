def topo_sort(g):
    # build graph
    adj = {k: [] for k, v in g}
    for u, v in g:
        adj[u].append(v)
        if v not in adj:
            adj[v] = []

    def dfs(v, visited, res, path):
        print(v, path)
        if visited[v] == -1:
            return False
        if visited[v] == 1:
            return True
        visited[v] = -1

        for e in adj[v]:
            if not dfs(e, visited, res, path + [e]):
                return False

        visited[v] = 1
        res.append(v)
        return True

    res = []
    visited = {v: 0 for v in adj.keys()}
    for n in adj.keys():
        if not dfs(n, visited, res, [n]):
            return []

    return res


if __name__ == "__main__":
    g = [(2, 4), (3, 4), (4, 5), (1, 5)]

    # assert topo_sort(g) == ["2 -> 3 -> 4 ->"]
    print(topo_sort(g))
