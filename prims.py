import random
import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Havel-Hakimi Algorithm to generate graph from degree sequence
def havel_hakimi(deg_sequence):
    deg_sequence = sorted(deg_sequence, reverse=True)
    G = nx.Graph()
    G.add_nodes_from(range(len(deg_sequence)))

    if sum(deg_sequence) % 2 != 0:
        return None

    while deg_sequence and deg_sequence[0] > 0:
        d = deg_sequence[0]
        deg_sequence = deg_sequence[1:]

        if d > len(deg_sequence):
            return None

        for i in range(d):
            deg_sequence[i] -= 1
            if deg_sequence[i] < 0:
                return None
            G.add_edge(len(deg_sequence), i, weight=random.randint(1, 10))

        deg_sequence = sorted([x for x in deg_sequence if x > 0], reverse=True)

    return G

# Prim's Algorithm to find Minimum Spanning Tree (MST)
def prim_mst(G):
    mst_edges = []
    visited = set()
    start_node = list(G.nodes())[0]
    min_heap = [(0, start_node, start_node)]

    while len(visited) < len(G.nodes()):
        if not min_heap:
            break
        weight, u, v = heapq.heappop(min_heap)
        if v in visited:
            continue
        visited.add(v)
        if u != v:
            mst_edges.append((u, v, weight))

        for neighbor in G.neighbors(v):
            if neighbor not in visited:
                edge_weight = G[v][neighbor]['weight']
                heapq.heappush(min_heap, (edge_weight, v, neighbor))

    mst = nx.Graph()
    mst.add_weighted_edges_from(mst_edges)
    return mst, mst_edges

# Function to find fundamental cutsets and circuits
def fundamental_cutsets_circuits(G, mst_edges):
    mst = nx.Graph()
    mst.add_weighted_edges_from(mst_edges)
    
    cutsets = []
    circuits = []
    all_edges = set(G.edges())
    mst_set = set(mst.edges())
    non_mst_edges = all_edges - mst_set

    for u, v, _ in mst_edges:
        mst_copy = mst.copy()
        mst_copy.remove_edge(u, v)
        cutset_edges = list(nx.edge_boundary(G, {u}, mst_copy))
        cutsets.append(cutset_edges)

    for u, v in non_mst_edges:
        mst_copy = mst.copy()
        mst_copy.add_edge(u, v)

        try:
            circuit = list(nx.find_cycle(mst_copy))
            circuits.append(circuit)
        except nx.exception.NetworkXNoCycle:
            continue

    return cutsets, circuits

# Function to draw the graph side by side with cutsets and circuits
def draw_graphs_with_all_cutsets_circuits(G, mst, cutsets, circuits):
    num_cutsets = len(cutsets)
    num_circuits = len(circuits)

    total_subplots = 2 + num_cutsets + num_circuits
    cols = 2
    rows = (total_subplots + 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(12, rows * 4))
    axes = axes.flatten()

    pos = nx.spring_layout(G)

    # Draw Original Graph
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=12, ax=axes[0])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=axes[0])
    axes[0].set_title("Original Graph")

    # Draw Minimum Spanning Tree (MST)
    mst_edge_labels = nx.get_edge_attributes(mst, 'weight')
    nx.draw(mst, pos, with_labels=True, node_color='lightgreen', edge_color='red', node_size=500, font_size=12, ax=axes[1])
    nx.draw_networkx_edge_labels(mst, pos, edge_labels=mst_edge_labels, ax=axes[1])
    axes[1].set_title("Minimum Spanning Tree (MST)")

    # Draw Fundamental Cutsets
    for idx, cutset in enumerate(cutsets):
        cutset_edges = [(u, v) for u, v in cutset]
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=12, ax=axes[2 + idx])
        nx.draw_networkx_edges(G, pos, edgelist=cutset_edges, edge_color='blue', width=2, ax=axes[2 + idx])
        axes[2 + idx].set_title(f"Fundamental Cutset {idx + 1}")

    # Draw Fundamental Circuits
    for idx, circuit in enumerate(circuits):
        circuit_edges = [(u, v) for u, v in circuit]
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=12, ax=axes[2 + num_cutsets + idx])
        nx.draw_networkx_edges(G, pos, edgelist=circuit_edges, edge_color='green', width=2, ax=axes[2 + num_cutsets + idx])
        axes[2 + num_cutsets + idx].set_title(f"Fundamental Circuit {idx + 1}")

    plt.tight_layout()
    plt.show()

# Main function
def main():
    n = int(input("Enter the number of nodes: "))
    deg_sequence = list(map(int, input(f"Enter a graphic sequence of length {n}: ").split()))

    G = havel_hakimi(deg_sequence)
    if G is None:
        print("Invalid degree sequence.")
        return

    if not nx.is_connected(G):
        print("The graph is disconnected.")
        return

    mst, mst_edges = prim_mst(G)
    cutsets, circuits = fundamental_cutsets_circuits(G, mst_edges)

    draw_graphs_with_all_cutsets_circuits(G, mst, cutsets, circuits)

    print("\nFundamental Cutsets")
    for idx, cutset in enumerate(cutsets):
        formatted_cutset = ", ".join([f"({u}, {v})" for u, v in cutset])
        print(f"Cutset {idx + 1}: [{formatted_cutset}]")

    print("\nFundamental Circuits")
    for idx, circuit in enumerate(circuits):
        formatted_circuit = ", ".join([f"({u}, {v})" for u, v in circuit])
        print(f"Circuit {idx + 1}: [{formatted_circuit}]")

if __name__ == "__main__":
    main()
