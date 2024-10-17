import random
import networkx as nx
import matplotlib.pyplot as plt

# Check if the graph is Eulerian
def is_eulerian(G):
    odd_degree_count = 0
    for node in G.nodes():
        if G.degree(node) % 2 != 0:
            odd_degree_count += 1

    if odd_degree_count == 0:
        return "circuit"  # Euler circuit
    elif odd_degree_count == 2:
        return "path"  # Euler path
    else:
        return None  # Not Eulerian

# Fleury's Algorithm to find Eulerian path/circuit
def fleury(G, start):
    if is_eulerian(G) is None:
        return []

    current_node = start
    euler_path = []

    while G.edges():
        for next_node in list(G.neighbors(current_node)):
            # Check if removing the edge would disconnect the graph
            if (G.degree(current_node) == 1) or (not nx.has_path(G, next_node, current_node)):
                euler_path.append((current_node, next_node))
                G.remove_edge(current_node, next_node)
                current_node = next_node
                break
            else:
                euler_path.append((current_node, next_node))
                G.remove_edge(current_node, next_node)
                current_node = next_node
                break

    return euler_path

# Function to draw the graph with Euler path
def draw_graph_with_path(G, euler_path):
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=12)

    # Highlight edges in the Euler path
    nx.draw_networkx_edges(G, pos, edgelist=euler_path, edge_color='orange', width=2)
    
    plt.title("Graph with Euler Path/Circuit")
    plt.show()

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

    eulerian_type = is_eulerian(G)
    if eulerian_type is None:
        print("The graph is not Eulerian.")
        return
    elif eulerian_type == "circuit":
        print("The graph has an Euler Circuit.")
        start_node = random.choice(list(G.nodes()))
    else:
        print("The graph has an Euler Path.")
        odd_degree_nodes = [node for node in G.nodes() if G.degree(node) % 2 != 0]
        start_node = odd_degree_nodes[0] if odd_degree_nodes else random.choice(list(G.nodes()))

    euler_path = fleury(G.copy(), start_node)
    
    if euler_path:
        print("\nEuler Path/Circuit found:")
        print(" -> ".join(str(edge) for edge in euler_path))
        draw_graph_with_path(G, euler_path)
    else:
        print("No Euler Path/Circuit found.")

if __name__ == "__main__":
    main()
