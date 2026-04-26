import networkx as nx
from geopy.distance import geodesic
from .data import NODES, EDGES

def build_graph():
    G = nx.Graph()

    for node, coord in NODES.items():
        G.add_node(node, pos=coord)

    for u, v in EDGES:
        dist = geodesic(NODES[u], NODES[v]).meters
        G.add_edge(u, v, weight=dist)

    return G