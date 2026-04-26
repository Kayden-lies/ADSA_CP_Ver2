import networkx as nx

def is_similar(p1, p2, threshold=0.7):
    common = len(set(p1) & set(p2))
    return common / max(len(p1), len(p2)) > threshold


def run_k_shortest(G, start, end, k=5):
    paths = nx.shortest_simple_paths(G, start, end, weight="weight")

    result = []

    for p in paths:
        # Skip similar routes
        if any(is_similar(p, r["path"]) for r in result):
            continue

        dist = sum(G[p[i]][p[i+1]]["weight"] for i in range(len(p)-1))

        result.append({
            "path": p,
            "distance": round(dist, 2)
        })

        if len(result) == k:
            break

    return result