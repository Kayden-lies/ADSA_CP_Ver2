import heapq
from geopy.distance import geodesic

def heuristic(G, a, b):
    return geodesic(G.nodes[a]["pos"], G.nodes[b]["pos"]).meters

def run_astar(G, start, end):
    steps = []
    pq = [(0, start)]
    g_score = {n: float("inf") for n in G.nodes}
    prev = {}

    g_score[start] = 0

    while pq:
        _, node = heapq.heappop(pq)

        steps.append({"type": "visit", "node": node})

        if node == end:
            break

        for neighbor in G.neighbors(node):
            tentative = g_score[node] + G[node][neighbor]["weight"]

            if tentative < g_score[neighbor]:
                g_score[neighbor] = tentative
                prev[neighbor] = node

                f = tentative + heuristic(G, neighbor, end)
                heapq.heappush(pq, (f, neighbor))

                steps.append({
                    "type": "relax",
                    "from": node,
                    "to": neighbor,
                    "f_score": f
                })

    path = []
    cur = end
    while cur in prev:
        path.append(cur)
        cur = prev[cur]
    path.append(start)
    path.reverse()

    return path, g_score[end], steps