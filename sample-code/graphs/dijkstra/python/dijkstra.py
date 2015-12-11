def main():
    graph = read_graph_from_file("weighted_graph_01.txt")
    start_vertex = graph.vertices[0]
    distances, predecessors = dijkstra(graph, start_vertex)

    # Print distances and routes.
    for index, distance in enumerate(distances):
        path = reconstruct_shortest_path(predecessors, start_vertex, index)
        formatted_path = " -> ".join([str(label) for label in path])
        print "{index}: {distance}\t({formatted_path})".format(**locals())


def read_graph_from_file(filename):
    with open(filename, "r") as input_file:
        # The first two lines define the vertex count and the edge count.
        vertex_count = int(input_file.readline())
        edge_count = int(input_file.readline())

        vertices = [Vertex(index) for index in range(0, vertex_count)]
        edges = []

        # The next 'edge_count' lines describe the edges: "start_vertex end_vertex weight".
        for i in range(0, edge_count):
            start_vertex, end_vertex, weight = [int(param) for param in input_file.readline().split()]

            # Adding the edge to the list of outbound edges for the start vertex.
            edge = Edge(vertices[start_vertex], vertices[end_vertex], weight)
            vertices[start_vertex].outbound_edges.append(edge)

            # For non-directed graphs, an outbound edge is also an inbound one (0 -> 1 == 1 -> 0).
            # Therefore, we reverse the edge and add it to the other vertex.
            reverse_edge = Edge(vertices[end_vertex], vertices[start_vertex], weight)
            vertices[end_vertex].outbound_edges.append(reverse_edge)

            edges.append(edge)
            edges.append(reverse_edge)

        return Graph(vertices, edges)


def dijkstra(graph, start_vertex):
    # Initialization: setting all known shortest distances to infinity,
    # and the start vertex will have the shortest distance to itself equal to 0.
    INFINITY = 10 ** 10
    distances = [INFINITY for _ in graph.vertices]
    distances[start_vertex.label] = 0
    path_predecessors = [None for _ in graph.vertices]

    # Visiting every vertex in the graph...
    visit_list = [vertex for vertex in graph.vertices]

    while len(visit_list) > 0:
        # ...but selecting the vertex with the shortest known distance every time.
        #
        # We can avoid doing the linear-time lookup every time by using a Fibonacci Heap instead,
        # thus reducing the complexity from O(V ^ 2) to O(E + V log V).
        shortest_distance_vertex = visit_list[0]
        shortest_distance_index = 0

        for (index, vertex) in enumerate(visit_list):
            if distances[vertex.label] < distances[shortest_distance_index]:
                shortest_distance_vertex = vertex
                shortest_distance_index = index

        visit_list.pop(shortest_distance_index)

        # For each adjacent vertex v, check if the path from the current vertex would be more efficient
        # than the one we've known before. I.e., if distance[current] + weight(current->v) < distance[v].
        for edge in shortest_distance_vertex.outbound_edges:
            neighbor_vertex = edge.end_vertex
            alternative_distance = distances[shortest_distance_vertex.label] + edge.weight

            # If we have indeed found a better path, remembering the new distance and predecessor.
            if alternative_distance < distances[neighbor_vertex.label]:
                distances[neighbor_vertex.label] = alternative_distance
                path_predecessors[neighbor_vertex.label] = shortest_distance_vertex.label

    # We can avoid the shortest_path_predecessor array completely, but we'll return it in case there's
    # a need to output the actual PATH instead of just the shortest distances.
    return distances, path_predecessors


def reconstruct_shortest_path(predecessors, start_vertex, end_vertex):
    path = [end_vertex]
    predecessor = predecessors[end_vertex]

    while predecessor is not None:
        path.insert(0, predecessor)
        predecessor = predecessors[predecessor]

    return path


class Vertex:
    def __init__(self, label):
        self.label = label
        self.outbound_edges = []

    def __str__(self):
        return "Label: %d    Edges: %s" % (self.label, ', '.join([str(edge) for edge in self.outbound_edges]))


class Edge:
    def __init__(self, start_vertex, end_vertex, weight):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.weight = weight

    def __str__(self):
        return "%d ---%d---> %d" % (self.start_vertex.label, self.weight, self.end_vertex.label)


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


if __name__ == "__main__":
    main()
