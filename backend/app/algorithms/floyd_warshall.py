def run_floyd_warshall(G):
    nodes = list(G.nodes)
    n = len(nodes)

    dist = {i: {j: float("inf") for j in nodes} for i in nodes}

    for node in nodes:
        dist[node][node] = 0

    for u, v, data in G.edges(data=True):
        dist[u][v] = data["weight"]
        dist[v][u] = data["weight"]

    steps = []

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

                    steps.append({
                        "type": "update",
                        "via": k,
                        "from": i,
                        "to": j,
                        "distance": dist[i][j]
                    })

    return dist, steps