import folium
import matplotlib.pyplot as plt
from ipyleaflet import Map, Marker
from ipywidgets import Button, Output, VBox

from helpers import closest_node_calculation
from algorithms_networkx import dijkstra_networkx

def draw_route(network, path):
    map = folium.Map(location=[network.nodes[path[0]].lat, network.nodes[path[0]].lon], zoom_start=15)

    coord1 = (network.nodes[path[0]].lat, network.nodes[path[0]].lon)
    coord2 = (network.nodes[path[-1]].lat, network.nodes[path[-1]].lon)

    folium.Marker(
        location=coord1,
        popup="Start",
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(map)

    folium.Marker(
        location=coord2,
        popup="end",
        icon=folium.Icon(color="red", icon="flag")
    ).add_to(map)

    points = [
        coord1
    ]

    for i in path:
        points.append((network.nodes[i].lat, network.nodes[i].lon))

    points.append(coord2)
    folium.PolyLine(
        locations=points,
        color = "blue",
        weight=5,
        opacity=0.7
    ).add_to(map)

    map.save("route.html")

def draw_points(network, points):
    map = folium.Map(location=[network.nodes[points[0]].lat, network.nodes[points[0]].lon], zoom_start=15)
    for i in range(len(points)):
        folium.Marker(
            location=(network.nodes[points[i]].lat, network.nodes[points[i]].lon),
            popup="Central point",
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(map) 
    
    map.save("centrality.html")

def interactive_map(network, graph):
    first_node = next(iter(network.nodes.values()))
    m = Map(center=(first_node.lat, first_node.lon), zoom=13)
    button = Button(description="Find route", button_style="success", disabled=True)
    out = Output()

    coords = []
    def handle_click(**kwargs):
        if kwargs.get('type') == 'click':
            active_markers = [layer for layer in m.layers if isinstance(layer, Marker)]
            latlon = kwargs.get('coordinates')

            if len(active_markers) < 2:
                marker = Marker(location=latlon)
                m.add_layer(marker)
            else:
                m.remove_layer(active_markers[0])
                marker = Marker(location=latlon)
                m.add_layer(marker)

            active_markers = len([layer for layer in m.layers if isinstance(layer, Marker)])
            button.disabled = (active_markers != 2)
    def handle_button_click(b):
        with out:
            out.clear_output()
            markers = [layer for layer in m.layers if isinstance(layer, Marker)]
            start_coords = markers[0].location
            end_coords = markers[1].location
            start_node = closest_node_calculation(network, start_coords[0], start_coords[1])
            end_node = closest_node_calculation(network, end_coords[0], end_coords[1])
            
            path, dist = dijkstra_networkx(graph, start_node, end_node)
            draw_route(network, path)

    button.on_click(handle_button_click)        
    m.on_interaction(handle_click)

    return VBox([m, button, out])

def runtime_graph(results):
    nodes = [r["nodes"] for r in results]
    labels = [r["area"] for r in results]

    plt.figure(figsize=(10, 6))

    plt.plot(nodes, [r["dijkstra"] for r in results], marker='o', label="Dijkstra algorithm")
    plt.plot(nodes, [r["a_star"] for r in results], marker='o', label="A* algorithm")
    plt.plot(nodes, [r["networkx_dijkstra"] for r in results], marker='o', label="NetworkX - Dijkstra")
    plt.plot(nodes, [r["networkx_astar"] for r in results], marker='o', label="NetworkX - A*")

    plt.xticks(nodes, labels, rotation=45)
    plt.xlabel("Graph size (nodes)")
    plt.ylabel("Average runtime (seconds)")
    plt.title("Algorithm Runtime vs Graph Size")
    plt.legend()
    plt.show()

def explored_graph(results):
    nodes = [r["nodes"] for r in results]
    labels = [r["area"] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(nodes, [r["exp_dijkstra"] for r in results], marker='o', label="Dijkstra")
    plt.plot(nodes, [r["exp_astar"] for r in results], marker='o', label="A* algorithm")
    plt.xlabel("Graph size (nodes)")
    plt.ylabel("Nodes explored")
    plt.title("Nodes Explored vs Graph Size")
    plt.xticks(nodes, labels, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()