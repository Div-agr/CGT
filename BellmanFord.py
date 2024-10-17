import random
import networkx as nx
import matplotlib.pyplot as plt

# Bellman-Ford algorithm function
def bellman_ford(G, source):
    distance = {node: float('inf') for node in G.nodes()}
    distance[source] = 0
    predecessor = {node: None for node in G.nodes()}

    # Relaxation step for all edges |V|-1 times
    for _ in range(len(G.nodes()) - 1):
        for u, v, data in G.edges(data=True):
            weight = data['weight']
            if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                predecessor[v] = u
            if distance[v] != float('inf') and distance[v] + weight < distance[u]:
                distance[u] = distance[v] + weight
                predecessor[u] = v

    # Check for negative weight cycles
    for u, v, data in G.edges(data=True):
        weight = data['weight']
        if distance[u] != float('inf') and distance[u] + weight < distance[v]:
            print("Graph contains a negative weight cycle.")
            return None, None

    return distance, predecessor

# Function to draw the graph with shortest paths
def draw_graph(G, distances, predecessor, source):
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=12)

    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Highlight source node
    nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='lightgreen', node_size=700)

    # Draw shortest path
    for target in G.nodes():
        if target != source and distances[target] < float('inf'):
            path = []
            while target is not None:
                path.append(target)
                target = predecessor[target]
            path.reverse()
            # Draw path
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='orange', width=2)

    plt.title(f"Graph with Shortest Paths from Node {source}")
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

    source = int(input("Enter the source vertex (0 to {0}): ".format(n - 1)))

    distances, predecessor = bellman_ford(G, source)
    
    if distances is not None:
        print("\nShortest distances from node {}:".format(source))
        for node, distance in distances.items():
            print(f"Node {node}: {distance}")

        draw_graph(G, distances, predecessor, source)

if __name__ == "__main__":
    main()
