import requests
import json

from helpers import calculate_distance
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


network = ds.Network()     

fill_data()

