import math

import data_structure as ds

def calculate_distance(node1_id, node2_id, graph):
        R = 6371000
        if hasattr(graph.nodes[node1_id], "lat"):
            node1 = graph.nodes[node1_id]
            node2 = graph.nodes[node2_id]

            lat1, lon1 = node1.lat, node1.lon
            lat2, lon2 = node2.lat, node2.lon
            
        else:
            node1 = graph.nodes[node1_id]
            node2 = graph.nodes[node2_id]

            lat1, lon1 = node1['pos']
            lat2, lon2 = node2['pos']

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)

        delta_phi = math.radians(lat2 - lat1) / 2
        delta_lambda = math.radians(lon2 - lon1) / 2

        a = (math.sin(delta_phi)**2) + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda)**2)

        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R*c

def closest_node_calculation(network, lat, lon):
    network.nodes[-1] = ds.Node(-1, lat, lon)
    closest_node = None
    closest_distance = float("inf")
    for i in network.nodes:
        if i != -1:
            distance = calculate_distance(-1, i, network)
            if distance < closest_distance:
                closest_distance = distance
                closest_node = i 
    return closest_node