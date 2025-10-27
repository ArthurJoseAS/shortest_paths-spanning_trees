import sys
import pydot
from typing import TypeAlias
import heapq

NodesListType: TypeAlias = list[str]
#[src_node : (dst_node, edge_weight) ]
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


def mst_prim(nodes: NodesListType, weighted_edge_list: EdgeListType) -> EdgeListType:
    s = nodes[0] 
    
    # let b in work_queue, 
    # b[0] = is the weight of the edge
    # b[1] is the source of the edge
    # b[2] is the destination of the edge
    work_queue: list[tuple[float, str ,str]] = []
    mst: EdgeListType = {}
    used_nodes = set()
    for e in weighted_edge_list[s]:
        work_queue.append((e[1], s, e[0]))
    heapq.heapify(work_queue)
    mst[s] = []
    used_nodes.add(s)
    while work_queue:
        last = heapq.heappop(work_queue)
        if last[2] not in used_nodes:
            if mst.get(last[1]) == None:
                mst[last[1]] = []
            mst[last[1]].append((last[2], last[0]))
        used_nodes.add(last[2])
        if not weighted_edge_list.get(last[2]) == None:
            for e in weighted_edge_list[last[2]]:
                if e[0] not in used_nodes:
                    work_queue.append((e[1], last[2], e[0]))
        heapq.heapify(work_queue)
    return mst

def export_graph_from_edgelist(edgelist: EdgeListType) -> pydot.Dot:
    export_graph = pydot.Dot("output_graph", graph_type="graph")
    for (s, edge_weight_list) in edgelist.items():
        for e in edge_weight_list:
            str_expression = list("\"")
            str_expression.append(str(e[1]))
            str_expression.append("\"")
            export_graph.add_edge(pydot.Edge(s, e[0], weight=e[1], label=''.join(str_expression)))
            
    return export_graph


if __name__ == "__main__":
    arquivo = sys.argv[1]
    graph = pydot.graph_from_dot_file(arquivo).pop()
    nodes: NodesListType
    edge_list: EdgeListType
    nodes, edge_list = generate_graph(graph) 
    minimum_spanning_tree = mst_prim(nodes, edge_list)
    exportgraph = export_graph_from_edgelist(minimum_spanning_tree)
    nome_arquivo: str = sys.argv[1][:sys.argv[1].rindex(".")]
    exportgraph.write(nome_arquivo + "mst.dot")
    for (k, v) in minimum_spanning_tree.items():
        print(str(k) + ": " + str(v))
    