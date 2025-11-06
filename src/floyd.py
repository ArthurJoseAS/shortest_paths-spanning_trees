import sys
import pydot
from typing import TypeAlias

NodesListType: TypeAlias = list[str]
EdgeListType: TypeAlias = dict[str, list[tuple[str, float]]]

def fill_nodes_list(graph: pydot.Dot, nodes: NodesListType):
    for e in graph.get_edges():
        if str(e.get_source()) not in nodes:
            nodes.append(str(e.get_source()))
        if str(e.get_destination()) not in nodes:
            nodes.append(str(e.get_destination()))


def fill_edge_list(graph: pydot.Dot, edgelist: EdgeListType, is_digraph: bool):
    for e in graph.get_edges():
        peso = float(e.get("weight") or 1.0)
        src = str(e.get_source())
        dst = str(e.get_destination())

        edgelist.setdefault(src, []).append((dst, peso))
        if not is_digraph:
            edgelist.setdefault(dst, []).append((src, peso))


def generate_graph(graph: pydot.Dot) -> tuple[NodesListType, EdgeListType]:
    ret_nodes: NodesListType = []
    ret_edge_list: EdgeListType = {}
    is_digraph = graph.get_type() == "digraph"

    fill_nodes_list(graph, ret_nodes)
    ret_nodes.sort()
    fill_edge_list(graph, ret_edge_list, is_digraph)

    return ret_nodes, ret_edge_list


def floyd_warshall(nodes: NodesListType, edge_list: EdgeListType):
    n = len(nodes)
    index = {nodes[i]: i for i in range(n)}  

    dist = [[float("inf")] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0

    for u in edge_list:
        for v, peso in edge_list[u]:
            i, j = index[u], index[v]
            dist[i][j] = peso

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    for i in range(n):
        if dist[i][i] < 0:
            print("Ciclo de peso negativo detectado!")
            return None

    print("\nMatriz de distâncias mínimas:")
    print("   ", end="")
    for node in nodes:
        print(f"{node:>8}", end="")
    print()

    for i, u in enumerate(nodes):
        print(f"{u:>3}", end=" ")
        for j in range(n):
            val = dist[i][j]
            if val == float("inf"):
                print(f"{'inf':>8}", end="")
            else:
                print(f"{val:8.2f}", end="")
        print()

    return dist


if __name__ == "__main__":

    arquivo = sys.argv[1]
    graphs = pydot.graph_from_dot_file(arquivo)

    graph = graphs[0]
    nodes, edge_list = generate_graph(graph)

    print("Nós:", nodes)
    print("\nExecutando Floyd–Warshall...")
    floyd_warshall(nodes, edge_list)
