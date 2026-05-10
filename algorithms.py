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
        #print('Starting point not in the dataset. Try another one!')
        return None, float('inf')
    elif goal not in network.nodes:
        #print('Goal point not in the dataset. Try another one!')
        return None, float('inf')

    closed_visited = {}
    open_visited = []
    traveled = {start: 0}

    heapq.heappush(open_visited, (0, start))

    while open_visited:
        current_score, current_id = heapq.heappop(open_visited)
        current_node = network.nodes[current_id]

        if current_id == goal:
            path = []
            curr = current_id
            
            while curr in closed_visited:
                path.append(curr)
                curr = closed_visited[curr]
            path.append(start)
            path.reverse() 

            return path, traveled[goal]

        for edge in current_node.connections:
            neighbor_id = edge.node2.node_id if edge.node1.node_id == current_id else edge.node1.node_id        
            distance_from_start = traveled[current_id] + edge.length
            
            if neighbor_id not in traveled or distance_from_start < traveled[neighbor_id]:
                closed_visited[neighbor_id] = current_id
                traveled[neighbor_id] = distance_from_start
                h_score = calculate_distance(neighbor_id, goal, network)
                f_score = distance_from_start + h_score
                heapq.heappush(open_visited, (f_score, neighbor_id))

    #print("There is no viable path between your starting point and your destination.")
    return None, float('inf')

    