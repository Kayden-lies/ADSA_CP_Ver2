def run_bellman_ford(G, start, end):
    steps = []
    dist = {n: float("inf") for n in G.nodes}
    prev = {}

    dist[start] = 0

    for _ in range(len(G.nodes) - 1):
        for u, v, data in G.edges(data=True):
            w = data["weight"]

            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

                steps.append({
                    "type": "relax",
                    "from": u,
                    "to": v,
                    "distance": dist[v]
                })

    path = []
    cur = end
    while cur in prev:
        path.append(cur)
        cur = prev[cur]
    path.append(start)
    path.reverse()

    return path, dist[end], steps