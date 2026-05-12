import time 
import random
from algorithms import dijkstra, a_star
from algorithms_networkx import dijkstra_networkx, astar_networkx, convert_to_networkx
from data_handler import fill_data

def benchmark_algorithms(network, nx_graph, num_samples=30):
    dijkstra_times = []
    astar_times = []
    dnetworkx_times = []
    anetworkx_times = []
    dijkstra_explored = []
    astar_explored = []

    all_node_ids = list(network.nodes.keys())
    samples_collected = 0

    while samples_collected < num_samples:
        start = random.choice(all_node_ids)
        end = random.choice(all_node_ids)

        if start == end:
            continue

        # Dijkstra
        t0 = time.perf_counter()
        path, dist, exp = dijkstra(start, end, network)
        t1 = time.perf_counter()
        if path is None:
            continue
        dijkstra_times.append(t1 - t0)
        dijkstra_explored.append(exp)

        # A*
        t0 = time.perf_counter()
        path, dist, exp = a_star(start, end, network)
        t1 = time.perf_counter()
        astar_times.append(t1 - t0)
        astar_explored.append(exp)

        # NetworkX Dijkstra
        t0 = time.perf_counter()
        dijkstra_networkx(nx_graph, start, end)
        t1 = time.perf_counter()
        dnetworkx_times.append(t1 - t0)

        # NetworkX A_star
        t0 = time.perf_counter()
        astar_networkx(nx_graph, start, end)
        t1 = time.perf_counter()
        anetworkx_times.append(t1 - t0)

        samples_collected += 1


    return (
        sum(dijkstra_times) / len(dijkstra_times) if dijkstra_times else 0,
        sum(astar_times) / len(astar_times) if astar_times else 0,
        sum(dnetworkx_times) / len(dnetworkx_times) if dnetworkx_times else 0,
        sum(anetworkx_times) / len(anetworkx_times) if anetworkx_times else 0,
        sum(dijkstra_explored) / len(dijkstra_explored) if dijkstra_explored else 0,
        sum(astar_explored) / len(astar_explored) if astar_explored else 0
    )

def run_benchmark(areas, num_samples):
    results = []

    for area in areas:
        network = fill_data(area)

        if network == "error":
            print("Error fetching data")
            continue
        
        nx_graph = convert_to_networkx(network)

        node_count = len(network.nodes)
        edge_count = len(network.ways)

        print(f"Benchmarking {node_count} nodes:")
        
        avg_d, avg_a, avg_dnx, avg_anx, exp_dijkstra, exp_astar = benchmark_algorithms(network, nx_graph, num_samples)
        
        results.append({
            "area": area,
            "nodes": node_count,
            "dijkstra": avg_d,
            "a_star": avg_a,
            "networkx_dijkstra": avg_dnx,
            "networkx_astar": avg_anx,
            "exp_dijkstra": exp_dijkstra,
            "exp_astar": exp_astar
        })
        
        print(f"Result: Dijkstra: {round(avg_d, 5)}  A*: {round(avg_a, 5)}  NetworkX - Dijkstra: {round(avg_dnx, 5)} NetworkX - A*: {round(avg_anx, 5)}")
        return results