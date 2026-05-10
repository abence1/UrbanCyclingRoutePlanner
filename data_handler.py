import requests

import data_structure as ds
from helpers import calculate_distance

url = "https://overpass-api.de/api/interpreter"

headers = {
    'User-Agent': 'UrbanCyclingRoutePlanner',
    'Accept': 'application/json'
}


def api_call(area):
    query = load_query(area)
    response = requests.post(url, data={'data': query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error {response.status_code}: {response.text}" }

def fill_data(area):
    network = ds.Network()
    data = api_call(area)

    if data.get("error") == None:
        elements = data.get("elements", [])
    else:
        return "error"

    edge_id = 1

    for element in elements:
        if element.get("type") == "node":
            node = ds.Node(element.get("id"), element.get("lat"), element.get("lon"))
            network.nodes[element.get("id")] = node

        if element.get("type") == "way":
            way_nodes = element.get("nodes", [])
            way = ds.Way(element.get("id"), element.get("tags"))

            for i in range(len(way_nodes) - 1):

                edge = ds.Edge(edge_id, network.nodes[way_nodes[i]], network.nodes[way_nodes[i + 1]], calculate_distance(way_nodes[i], way_nodes[i + 1], network))
                
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
    return network

def load_query(area):
    with open("query.txt", "r") as f:
        query = f.read()
    return query.replace("{area}", area)
