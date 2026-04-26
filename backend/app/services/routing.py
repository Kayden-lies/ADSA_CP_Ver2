from app.graph.builder import build_graph
from app.graph.data import NODES

from app.algorithms.dijkstra import run_dijkstra
from app.algorithms.astar import run_astar
from app.algorithms.bellman_ford import run_bellman_ford
from app.algorithms.floyd_warshall import run_floyd_warshall
from app.algorithms.k_shortest import run_k_shortest

G = build_graph()

def route(start, end, algo):

    if algo == "dijkstra":
        path, dist, steps = run_dijkstra(G, start, end)

    elif algo == "astar":
        path, dist, steps = run_astar(G, start, end)

    elif algo == "bellman":
        path, dist, steps = run_bellman_ford(G, start, end)

    elif algo == "floyd":
        dist_matrix, steps = run_floyd_warshall(G)
        return {"matrix": dist_matrix, "steps": steps}

    elif algo == "kshortest":
        return {"routes": run_k_shortest(G, start, end)}

    else:
        return {"error": "Invalid algorithm"}

    return {
        "path": path,
        "coordinates": [NODES[n] for n in path],
        "distance": round(dist, 2),
        "steps": steps
    }