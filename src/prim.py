import sys
import pydot

def fill_nodes_list(graph: pydot.Dot, nodes: list[str]):
    for e in graph.get_edges():
        if str(e.get_source()) not in nodes:
            nodes.append(str(e.get_source()))
        if str(e.get_destination()) not in nodes:
            nodes.append(str(e.get_destination()))
        

def fill_edge_list(graph: pydot.Dot, nodes: dict[str, int], edgelist: dict[str, list[tuple[str, float]]],
                   is_digraph: bool):
    for e in graph.get_edges():
        if edgelist.get(e.get_source()):
            edgelist[e.get_source()].append((e.get_destination(), float(e.get("weight"))))
        else:
            edgelist[e.get_source()] = [(e.get_destination(), float(e.get("weight")))]
        if not is_digraph:
            if edgelist.get(e.get_destination()):
                edgelist[e.get_destination()].append((e.get_source(), float(e.get("weight"))))
            else:
                edgelist[e.get_destination()] = [(e.get_source(), float(e.get("weight")))]
            

def generate_graph(graph: pydot.Dot) -> tuple[list, dict]:
    ret_nodes: list[str] = []
    ret_edge_list: dict[str, list[tuple[str, float]]] = {}
    is_digraph = False
    if graph.get_type() == "digraph":
        is_digraph = True
    fill_nodes_list(graph, ret_nodes)
    ret_nodes.sort()
    fill_edge_list(graph, ret_nodes, ret_edge_list, is_digraph)

    return ret_nodes, ret_edge_list




if __name__ == "__main__":
    arquivo = sys.argv[1]
    graph = pydot.graph_from_dot_file(arquivo).pop()
    nodes: list[str]
    #edge_list["a"] returns a the adjacency list of the node "a" with the weight for each given edge
    edge_list: dict[str, list[tuple[str, float]]]
    nodes, edge_list = generate_graph(graph) 
    print(nodes)
    for (k, v) in edge_list.items():
        print(str(k) + ": " + str(v))
    # vertices, matriz = ler_grafo_dot(arquivo)
    
    # # for v in vertices:
    # #     export_graph.add_node(pydot.Node(v))
    
    # # dist_list = [None]*len(vertices)
    # # resultado = bfs(vertices, matriz)
    # # print("Ordem da BFS:", " -> ".join(resultado))
    # # print("\nMatriz de Adjacência:")
    
    # for i in range(len(vertices)):
    #     print(str(vertices[i]) + ": " + str(matriz[i]) + "  Distancia: "  + str(dist_list[i]))
    # nome_arquivo: str = sys.argv[1][:sys.argv[1].rindex(".")]
    # export_graph.write(nome_arquivo + "bfstree.dot")