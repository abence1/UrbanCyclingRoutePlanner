import requests
import heapq

import data_structure as ds

url = "https://overpass-api.de/api/interpreter"

headers = {
    'User-Agent': 'UrbanCyclingRoutePlanner',
    'Accept': 'application/json'
}

query = """
[out:json][timeout:60];
area["name"="Budapest"]->.searchArea;
(
    way["cycleway"]["cycleway"!="no"](area.searchArea);
    way["cycleway:right"]["cycleway:right"!="no"](area.searchArea);
    way["cycleway:left"]["cycleway:left"!="no"](area.searchArea);
    way["cycleway:both"]["cycleway:both"!="no"](area.searchArea);

    way["highway"="cycleway"](area.searchArea);
    way["bicycle"="designated"](area.searchArea);

    way["oneway:bicycle"="no"](area.searchArea);
    way["cycleway"="opposite"](area.searchArea);
    way["cycleway"="opposite_lane"](area.searchArea);

    way["cycleway"="share_busway"](area.searchArea);
    way["cycleway:right"="share_busway"](area.searchArea);

    way["bicycle_road"]["bicycle_road"!="no"](area.searchArea);
    way["cyclestreet"]["cyclestreet"!="no"](area.searchArea);

    way["highway"~"path|footway|pedestrian"]["bicycle"~"yes|designated"](area.searchArea);
);
(._; >;);
out body;
"""

def api_call():
    response = requests.post(url, data={'data': query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error {response.status_code}: {response.text}" }

def fill_data():
    data = api_call()

    if data.get("error") == None:
        elements = data.get("elements", [])
    else:
        return data.get("error")

    edge_id = 1

    for element in elements:
        if element.get("type") == "node":
            node = ds.Node(element.get("id"), element.get("lat"), element.get("lon"))
            network.nodes[element.get("id")] = node

        if element.get("type") == "way":
            way_nodes = element.get("nodes", [])
            way = ds.Way(element.get("id"), element.get("tags"))

            for i in range(len(way_nodes) - 1):

                edge = ds.Edge(edge_id, network.nodes[way_nodes[i]], network.nodes[way_nodes[i + 1]])
                
                if element.get("tags", {}).get("oneway") == "yes" and element.get("tags", {}).get("oneway:bicycle") == "no":
                    network.nodes[way_nodes[i]].connections.append(edge)
                    network.nodes[way_nodes[i + 1]].connections.append(edge)
                elif element.get("tags", {}).get("oneway") == "yes":
                    network.nodes[way_nodes[i]].connections.append(edge)
                else:
                    network.nodes[way_nodes[i]].connections.append(edge)
                    network.nodes[way_nodes[i + 1]].connections.append(edge)

                edge_id += 1
                way.edges.append(edge)

            network.ways[element.get("id")] = way


network = ds.Network()
fill_data()

def dijkstra(source_node, target_node):
    distances = {}
    previous = {}

    for i in network.nodes:
        distances[i] = float("inf")

    distances[source_node] = 0
    previous[source_node] = None
    heap = [(0, source_node)]
    visited = set()

    while heap:
        current_dist, current_node = heapq.heappop(heap)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == target_node:
            break

        for edge in network.nodes[current_node].connections:
            if edge.node1.node_id != current_node:
                next_node = edge.node1
            else:
                next_node = edge.node2

            new_dist = current_dist + edge.length

            if new_dist < distances[next_node.node_id]:
                distances[next_node.node_id] = new_dist
                previous[next_node.node_id] = current_node
                heapq.heappush(heap, (new_dist, next_node.node_id))

    if target_node not in previous:
        return None, float("inf")

    path = []
    current = target_node

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[target_node]

source = network.nodes.get(12700325860)
target = network.nodes.get(1613332399)

path, dist = dijkstra(source.node_id, target.node_id)

if path is None:
    print('Target is unreachable.')
else:
    print(path, dist)