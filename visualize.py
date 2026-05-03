import folium

def draw_map(network, path):
    map = folium.Map(location=[47.483, 19.052], zoom_start=15)

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