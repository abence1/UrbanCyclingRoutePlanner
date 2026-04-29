class Node:
    def __init__(self, node_id, lat, lon):
        self.node_id = node_id
        self.lat = lat
        self.lon = lon
        self.connections = []
    
class Edge:
    def __init__(self, edge_id, node1, node2, tags):
        self.edge_id = edge_id
        self.node1 = node1
        self.node2 = node2
        self.tags = tags
        self.length = self.calculate_length()

    def calculate_length(self):
        pass

class Network:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_way(self, way):
        pass
