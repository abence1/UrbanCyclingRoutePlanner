import networkx as nx
import math

from helpers import calculate_distance

def convert_to_networkx(network):
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

def dijkstra_networkx(graph, start_node, end_node):
    try:
        length, path = nx.single_source_dijkstra(graph, source=start_node, target=end_node, weight='weight')
        return path, length
    except nx.NetworkXNoPath:
        return None, float('inf')

def astar_networkx(graph, start_node, end_node):
    heuristic = lambda start_node, end_node : calculate_distance(start_node, end_node, graph)
    try:
        path = nx.astar_path(graph, source=start_node, target=end_node, heuristic=heuristic, weight='weight')
        length = nx.path_weight(graph, path, weight='weight')
        return path, length
    except nx.NetworkXNoPath:
        return None, float('inf')

def betweenness_centrality(graph, n):
    central_points = {}
    for i in range(n):
        betweenness = nx.betweenness_centrality(graph, k = math.floor(math.sqrt(len(graph.nodes))))
        top_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
        if top_nodes[0][0] not in central_points:
            central_points[top_nodes[0][0]] = 1
        else:
            central_points[top_nodes[0][0]] += 1
    return central_points
    
