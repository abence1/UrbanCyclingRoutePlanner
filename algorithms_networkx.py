import networkx as nx

from main import network
from visualize import draw_map
from helpers import calculate_distance

def convert_to_networkx():
    graph = nx.DiGraph()

    for node_id, node in network.nodes.items():
        graph.add_node(node_id, pos=(node.lat, node.lon))

    for way_id, way in network.ways.items():
        tags = way.tags if hasattr(way, 'tags') else {}
        for edge in way.edges:
            if tags.get("oneway") == "yes" and tags.get("oneway:bicycle") == "no":
                graph.add_edge(edge.node1.node_id, edge.node2.node_id, weight=edge.length)
                graph.add_edge(edge.node2.node_id, edge.node1.node_id, weight=edge.length)
            elif tags.get("oneway") == "yes":
                graph.add_edge(edge.node1.node_id, edge.node2.node_id, weight=edge.length)
            else:
                graph.add_edge(edge.node1.node_id, edge.node2.node_id, weight=edge.length)
                graph.add_edge(edge.node2.node_id, edge.node1.node_id, weight=edge.length)
    return graph

def dijkstra(graph, start_node, end_node):
    try:
        path = nx.dijkstra_path(graph, source=start_node, target=end_node, weight='weight')
        length = nx.dijkstra_path_length(graph, source=start_node, target=end_node, weight='weight')
        return path, length
    except nx.NetworkXNoPath:
        return None, float('inf')

def astar(graph, start_node, end_node):
    heuristic = lambda start_node, end_node : calculate_distance(start_node, end_node, graph)
    try:
        path = nx.astar_path(graph, source=start_node, target=end_node, heuristic=heuristic, weight='weight')
        length = nx.astar_path_length(graph, source=start_node, target=end_node, heuristic=heuristic, weight='weight')
        return path, length
    except nx.NetworkXNoPath:
        return None, float('inf')
    
graph = convert_to_networkx()

path, length = astar(graph, 176913390, 171524952)

draw_map(network, path)