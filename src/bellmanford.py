import sys
import pydot
from typing import TypeAlias

NodesListType: TypeAlias = list[str]
#[src_node : (dst_node, edge_weight) ]
EdgeListType: TypeAlias = dict[str, list[tuple[str, float]]]


def fill_nodes_list(graph: pydot.Dot, nodes: NodesListType):
    for e in graph.get_edges():
        if str(e.get_source()) not in nodes:
            nodes.append(str(e.get_source()))
        if str(e.get_destination()) not in nodes:
            nodes.append(str(e.get_destination()))


def fill_edge_list(graph: pydot.Dot, edgelist: EdgeListType, is_digraph: bool):
    for e in graph.get_edges():
        peso = float(e.get("weight") or 1.0)  # evita erro se não tiver peso
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


def bellman_ford(nodes: NodesListType, edge_list: EdgeListType, origem: str):
    dist = {n: float("inf") for n in nodes}
    pai = {n: None for n in nodes}
    dist[origem] = 0.0

    for _ in range(len(nodes) - 1):
        atualizado = False
        for u in edge_list:
            for v, peso in edge_list[u]:
                if dist[u] + peso < dist[v]:
                    dist[v] = dist[u] + peso
                    pai[v] = u
                    atualizado = True
        if not atualizado:
            break

    for u in edge_list:
        for v, peso in edge_list[u]:
            if dist[u] + peso < dist[v]:
                print("⚠️ Ciclo de peso negativo detectado!")
                return None, None

    return dist, pai


if __name__ == "__main__":
    arquivo = sys.argv[1]
    graphs = pydot.graph_from_dot_file(arquivo)
    
    graph = graphs[0]
    nodes, edge_list = generate_graph(graph)

    print("Nós:", nodes)
    print("\nLista de adjacência:")
    for u, vizinhos in edge_list.items():
        print(f"  {u}: {vizinhos}")

    while True:
        origem = input("\nDigite o nó de origem: ")
        if origem not in nodes:
            print("Nó de origem inválido!")
            continue
        break

    dist, pai = bellman_ford(nodes, edge_list, origem)
    if dist:
        print("\nDistâncias mínimas a partir de", origem)
        for n in nodes:
            print(f"  {origem} → {n}: {dist[n]}")

        print("\nPais (árvore de caminhos mínimos):")
        for n in nodes:
            print(f"  {n}: {pai[n]}")
