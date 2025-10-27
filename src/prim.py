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
        

def fill_edge_list(graph: pydot.Dot, edgelist: EdgeListType,
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
    ret_nodes: NodesListType = []
    ret_edge_list: EdgeListType = {}
    is_digraph = False
    if graph.get_type() == "digraph":
        is_digraph = True
    fill_nodes_list(graph, ret_nodes)
    ret_nodes.sort()
    fill_edge_list(graph, ret_edge_list, is_digraph)

    return ret_nodes, ret_edge_list


# def mst_prim(nodes: NodesListType, weighted_edge_list: EdgeListType)
if __name__ == "__main__":
    arquivo = sys.argv[1]
    graph = pydot.graph_from_dot_file(arquivo).pop()
    nodes: NodesListType
    #edge_list["a"] returns a the adjacency list of the node "a" with the weight for each given edge
    edge_list: EdgeListType
    nodes, edge_list = generate_graph(graph) 
    print(nodes)
    for (k, v) in edge_list.items():
        print(str(k) + ": " + str(v))