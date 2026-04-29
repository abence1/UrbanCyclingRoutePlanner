import requests
import json

url = "https://overpass-api.de/api/interpreter"

headers = {
    'User-Agent': 'UrbanCyclingRoutePlanner',
    'Accept': 'application/json'
}

query = """
[out:json][timeout:60];
area["name"="VII. kerület"]->.searchArea;
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

response = requests.post(url, data={'data': query}, headers=headers)

if response.status_code == 200:
    data = response.json()
    elements = data.get("elements", [])
    for i in elements:
        if i.get("type") == "way":
            tags = i.get("tags", {})
            print(tags.get("name", "Unnamed Road"))
    ways_only = [e for e in data.get("elements", []) if e.get("type") == "way"]
    print(ways_only)
else:
    print(f"Error {response.status_code}: {response.text}")