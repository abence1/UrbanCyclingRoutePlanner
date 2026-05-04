import heapq

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