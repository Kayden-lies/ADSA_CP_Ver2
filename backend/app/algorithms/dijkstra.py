import heapq

def run_dijkstra(G, start, end):
    steps = []
    pq = [(0, start)]
    dist = {n: float("inf") for n in G.nodes}
    prev = {}

    dist[start] = 0

    while pq:
        d, node = heapq.heappop(pq)

        steps.append({"type": "visit", "node": node})

        if node == end:
            break

        for neighbor in G.neighbors(node):
            w = G[node][neighbor]["weight"]
            new_d = d + w

            if new_d < dist[neighbor]:
                dist[neighbor] = new_d
                prev[neighbor] = node
                heapq.heappush(pq, (new_d, neighbor))

                steps.append({
                    "type": "relax",
                    "from": node,
                    "to": neighbor,
                    "distance": new_d
                })

    path = []
    cur = end
    while cur in prev:
        path.append(cur)
        cur = prev[cur]
    path.append(start)
    path.reverse()

    return path, dist[end], steps