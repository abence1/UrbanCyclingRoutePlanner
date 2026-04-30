import math

class Node:
    def __init__(self, node_id, lat, lon):
        self.node_id = node_id
        self.lat = lat
        self.lon = lon
        self.connections = []
    
class Edge:
    def __init__(self, edge_id, node1, node2):
        self.edge_id = edge_id
        self.node1 = node1
        self.node2 = node2
        self.length = self.calculate_length()

    def calculate_length(self):
        R = 6371000

        phi1 = math.radians(self.node1.lat)
        phi2 = math.radians(self.node2.lat)

        delta_phi = math.radians(self.node2.lat - self.node1.lat) / 2
        delta_lambda = math.radians(self.node2.lon - self.node1.lon) / 2

        a = (math.sin(delta_phi)**2) + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda)**2)

        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R*c
    
class Way:
    def __init__(self, way_id, tags):
        self.way_id = way_id
        self.tags = tags
        self.edges = []

class Network:
    def __init__(self):
        self.nodes = {}
        self.ways = {}


        


