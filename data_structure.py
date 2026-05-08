class Node:
    def __init__(self, node_id, lat, lon):
        self.node_id = node_id
        self.lat = lat
        self.lon = lon
        self.connections = []
    
class Edge:
    def __init__(self, edge_id, node1, node2, length):
        self.edge_id = edge_id
        self.node1 = node1
        self.node2 = node2
        self.length = length

class Way:
    def __init__(self, way_id, tags):
        self.way_id = way_id
        self.tags = tags
        self.edges = []

class Network:
    def __init__(self):
        self.nodes = {}
        self.ways = {}
