import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate

NODE_SIZE = 2000
INFINITY_CAPACITY = float('inf')

def build_graph():
    """
    Builds the directed graph with capacities based on the given logistics network.

    Returns:
        nx.DiGraph: Directed graph representing the logistics network.
    """
    G = nx.DiGraph()

    edges = [
        ("Terminal 1", "Warehouse 1", 25),
        ("Terminal 1", "Warehouse 2", 20),
        ("Terminal 1", "Warehouse 3", 15),
        ("Terminal 2", "Warehouse 3", 15),
        ("Terminal 2", "Warehouse 4", 30),
        ("Terminal 2", "Warehouse 2", 10),
        ("Warehouse 1", "Shop 1", 15),
        ("Warehouse 1", "Shop 2", 10),
        ("Warehouse 1", "Shop 3", 20),
        ("Warehouse 2", "Shop 4", 15),
        ("Warehouse 2", "Shop 5", 10),
        ("Warehouse 2", "Shop 6", 25),
        ("Warehouse 3", "Shop 7", 20),
        ("Warehouse 3", "Shop 8", 15),
        ("Warehouse 3", "Shop 9", 10),
        ("Warehouse 4", "Shop 10", 20),
        ("Warehouse 4", "Shop 11", 10),
        ("Warehouse 4", "Shop 12", 15),
        ("Warehouse 4", "Shop 13", 5),
        ("Warehouse 4", "Shop 14", 10),
    ]

    for source_node, destination_node, capacity in edges:
        G.add_edge(source_node, destination_node, capacity=capacity)

    return G


def calculate_max_flow(G, source, sink):
    """
    Calculates the maximum flow from source to sink using the Edmonds-Karp algorithm.

    Args:
        G (nx.DiGraph): Directed graph.
        source (str): Source node.
        sink (str): Sink node.

    Returns:
        tuple: Maximum flow value and flow dictionary.
    """
    if G.number_of_nodes() == 0:
        raise ValueError("The graph is empty.")
    if source not in G or sink not in G:
        raise ValueError(f"Source '{source}' or sink '{sink}' is not in the graph.")

    return nx.maximum_flow(G, source, sink)


def flow_analysis(flow_dict):
    """
    Analyzes the flow between terminals and shops and formats the results.

    Args:
        flow_dict (dict): Dictionary of flows.

    Returns:
        list: List of formatted flow results.
    """
    flow_results = []
    for terminal, destinations in flow_dict.items():
        for shop, flow in destinations.items():
            if flow > 0:
                flow_results.append([terminal, shop, flow])
    return flow_results


def visualize_graph(G):
    """
    Visualizes the logistics network graph with fixed node positions.
    """
    pos = {
        "Terminal 1": (0, 3),
        "Terminal 2": (0, 1),
        "Warehouse 1": (1, 4),
        "Warehouse 2": (1, 3),
        "Warehouse 3": (1, 2),
        "Warehouse 4": (1, 1),
        "Shop 1": (2, 5),
        "Shop 2": (2, 4.5),
        "Shop 3": (2, 4),
        "Shop 4": (2, 3.5),
        "Shop 5": (2, 3),
        "Shop 6": (2, 2.5),
        "Shop 7": (2, 2),
        "Shop 8": (2, 1.5),
        "Shop 9": (2, 1),
        "Shop 10": (2, 0.5),
        "Shop 11": (2, 0),
        "Shop 12": (2, -0.5),
        "Shop 13": (2, -1),
        "Shop 14": (2, -1.5),
    }

    capacities = nx.get_edge_attributes(G, "capacity")
    plt.figure(figsize=(12, 8))
    nx.draw(
        G, pos, with_labels=True, node_color="lightblue", font_weight="bold",
        node_size=NODE_SIZE, edge_color="gray", width=2
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=capacities, font_size=10)
    plt.show()


def print_edges_with_capacities(G):
    """
    Prints all edges in the graph with their capacities.
    """
    print("Edges in the graph with capacities:")
    for u, v, data in G.edges(data=True):
        print(f"{u} -> {v}, capacity: {data['capacity']}")


def main():
    G = build_graph()

    print_edges_with_capacities(G)
    visualize_graph(G)

    G.add_node("Super Source")
    G.add_node("Super Sink")

    G.add_edge("Super Source", "Terminal 1", capacity=INFINITY_CAPACITY)
    G.add_edge("Super Source", "Terminal 2", capacity=INFINITY_CAPACITY)

    for shop in [f"Shop {i}" for i in range(1, 15)]:
        G.add_edge(shop, "Super Sink", capacity=INFINITY_CAPACITY)

    max_flow_value, flow_dict = calculate_max_flow(G, "Super Source", "Super Sink")

    flow_results = flow_analysis(flow_dict)

    print(f"\nMaximum Flow in the Logistics Network: {max_flow_value} units\n")
    print("Flow Analysis Table:")
    print(tabulate(flow_results, headers=["Terminal", "Shop", "Flow"], tablefmt="grid"))


if __name__ == "__main__":
    main()
