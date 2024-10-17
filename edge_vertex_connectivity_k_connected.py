import random
import networkx as nx
import matplotlib.pyplot as plt

def havel_hakimi(deg_sequence):
    deg_sequence = sorted(deg_sequence, reverse=True)  # Sort in non-increasing order
    G = nx.Graph()

    # Check if the sum of degrees is even
    if sum(deg_sequence) % 2 != 0:
        print("The degree sequence is not valid. Sum of degrees must be even.")
        return None

    # Add nodes to the graph
    G.add_nodes_from(range(len(deg_sequence)))

    # Havel-Hakimi process
    while deg_sequence and deg_sequence[0] > 0:
        d = deg_sequence[0]  # Degree of the first node (largest degree)
        deg_sequence = deg_sequence[1:]  # Remove the first node

        # Check if there are enough nodes to connect to
        if d > len(deg_sequence):
            print("The degree sequence is invalid. Not enough nodes to satisfy the degree.")
            return None

        # Reduce the degree of the next 'd' nodes
        for i in range(d):
            deg_sequence[i] -= 1
            if deg_sequence[i] < 0:
                print("The degree sequence is invalid. Negative degree found.")
                return None
            # Add edges
            G.add_edge(len(deg_sequence), i, weight=random.randint(1, 10))

        # Remove all zero degrees and sort the sequence again
        deg_sequence = sorted([x for x in deg_sequence if x > 0], reverse=True)

    return G

def edge_connectivity(G):
    return nx.edge_connectivity(G)

def vertex_connectivity(G):
    return nx.node_connectivity(G)

def k_connected(G):
    return vertex_connectivity(G)

def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=12)
    plt.title("Graph Visualization")
    plt.show()

def main():
    # Step 1: Input degree sequence
    n = int(input("Enter the number of nodes: "))
    deg_sequence = list(map(int, input(f"Enter a graphic sequence of length {n} (must sum to even): ").split()))

    # Step 2: Generate graph from the degree sequence
    G = havel_hakimi(deg_sequence)
    if G is None:
        print("Invalid degree sequence.")
        return

    # Step 3: Calculate edge connectivity
    edge_conn = edge_connectivity(G)
    print(f"Edge Connectivity: {edge_conn}")

    # Step 4: Calculate vertex connectivity
    vertex_conn = vertex_connectivity(G)
    print(f"Vertex Connectivity: {vertex_conn}")

    # Step 5: Determine k-connectedness
    k = k_connected(G)
    print(f"The graph is {k}-connected.")

    # Step 6: Draw the graph
    draw_graph(G)

if __name__ == "__main__":
    main()
