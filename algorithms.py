import heapq
from helpers import calculate_distance

def dijkstra(source_node, target_node, network):
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


def a_star(start, goal, network):
    
    if start not in network.nodes:
        print('Starting point not in the dataset. Try another one!')
        return None
    
    elif start not in network.nodes:
        print('Starting point not in the dataset. Try another one!')
        return None

    start = network.nodes[start]
    goal = network.nodes[goal]
    open_list = [(calculate_distance(start, goal, network), start)]
    count = 0
    distances = {start: 0}
    previous = {}
    dropped_nodes = set()

    while len(open_list) > 0:
        current_f, _, current_id = heapq.heappop(open_list)

        if current_id == goal:
            path = []
            while current_id in previous:
                path.append(current_id)
                current_id = previous[current_id]
            path.append(start)
            return path[::-1]

        if current_id in dropped_nodes:
            continue
            
        dropped_nodes.add(current_id)
        current_node = network.nodes[current_id]

        for edge in current_node.connections:
            neighbor_node = edge.node2 if edge.node1.node_id == current_id else edge.node1
            neighbor_id = neighbor_node.node_id
            
            if neighbor_id in dropped_nodes:
                continue

            tentative_g = distances[current_id] + edge.length

            if neighbor_id not in distances or tentative_g < distances[neighbor_id]:
                previous[neighbor_id] = current_id
                distances[neighbor_id] = tentative_g
                f_score = tentative_g + calculate_distance(neighbor_node, goal, network)
                count += 1
                heapq.heappush(open_list, (f_score, count, neighbor_id))

        return None
    

    
