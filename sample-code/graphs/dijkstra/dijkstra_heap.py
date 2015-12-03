import heapq


def main():
    # An advanced version of Dijkstra's shortest path algorithm that uses heaps to speed up its lookups.
    # Also, to make things more universal, we use string labels here instead of just integers.
    graph = read_graph_from_file("string_weighted_graph_01.txt")
    start_vertex = graph.vertices["a"]
    distances, predecessors = dijkstra(graph, start_vertex)

    # Print distances and routes.
    for label, distance in sorted(distances.iteritems()):
        path = reconstruct_shortest_path(predecessors, start_vertex, label)
        formatted_path = " -> ".join([str(label) for label in path])
        print "{label}: {distance}\t({formatted_path})".format(**locals())


def read_graph_from_file(filename):
    with open(filename, "r") as input_file:
        # The first two lines define the vertex count and the edge count.
        vertex_count = int(input_file.readline())
        edge_count = int(input_file.readline())

        vertices = {}
        edges = []

        # The next 'edge_count' lines describe the edges: "start_vertex end_vertex weight".
        for i in range(0, edge_count):
            start_vertex, end_vertex, weight = [param for param in input_file.readline().split()]
            weight = int(weight)

            if start_vertex not in vertices:
                vertices[start_vertex] = Vertex(label=start_vertex)
            if end_vertex not in vertices:
                vertices[end_vertex] = Vertex(label=end_vertex)

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
    INFINITY = 10 ** 15
    distances = {vertex: INFINITY for vertex in graph.vertices}
    distances[start_vertex.label] = 0

    path_predecessors = {start_vertex.label: None}
    heap = [[start_vertex.label, 0]]

    while len(heap) > 0:
        # Picking the vertex with the smallest known distance so far.
        while True:
            shortest_distance_label, distance = heapq.heappop(heap)
            shortest_distance_vertex = graph.vertices[shortest_distance_label]
            if distance != INFINITY:
                break

        # For each adjacent vertex v, check if the path from the current vertex would be more efficient
        # than the one we've known before. I.e., if distance[current] + weight(current->v) < distance[v].
        for edge in shortest_distance_vertex.outbound_edges:
            neighbor_vertex = edge.end_vertex
            alternative_distance = distances[shortest_distance_vertex.label] + edge.weight
            if alternative_distance < distances[neighbor_vertex.label]:
                # If we have indeed found a better path, remembering the new distance and predecessor.
                distances[neighbor_vertex.label] = alternative_distance
                path_predecessors[neighbor_vertex.label] = shortest_distance_vertex.label
                # Pushing the new distance to the heap.
                heapq.heappush(heap, [neighbor_vertex.label, alternative_distance])

    return distances, path_predecessors


def reconstruct_shortest_path(predecessors, start_vertex, end_vertex):
    path = [end_vertex]
    predecessor = predecessors[end_vertex]

    while predecessor != start_vertex and predecessor is not None:
        path.insert(0, predecessor)
        predecessor = predecessors[predecessor]

    return path


class Vertex:
    def __init__(self, label):
        self.label = label
        self.outbound_edges = []

    def __str__(self):
        return "Label: %s    Edges: %s" % (self.label, ', '.join([str(edge) for edge in self.outbound_edges]))


class Edge:
    def __init__(self, start_vertex, end_vertex, weight):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.weight = weight

    def __str__(self):
        return "%s ---%d---> %s" % (self.start_vertex.label, self.weight, self.end_vertex.label)


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


if __name__ == "__main__":
    main()
