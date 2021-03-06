def main():
    graph = read_graph_from_file("graph01.txt")
    distances = floyd_warshall(graph)

    for i in graph.vertices:
        print ""
        for j in graph.vertices:
            print "%d -> %d: %d" % (i.label, j.label, distances[i.label][j.label])


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
            vertices[end_vertex].inbound_edges.append(edge)

            # For non-directed graphs, an outbound edge is also an inbound one (0 -> 1 == 1 -> 0).
            # Therefore, we reverse the edge and add it to the other vertex.
            reverse_edge = Edge(vertices[end_vertex], vertices[start_vertex], weight)
            vertices[end_vertex].outbound_edges.append(reverse_edge)
            vertices[start_vertex].inbound_edges.append(reverse_edge)

            edges.append(edge)
            edges.append(reverse_edge)

        return Graph(vertices, edges)


def floyd_warshall(graph):
    INFINITY = 10 ** 15

    # Initializing the subproblems:
    # For each vertex, the shortest distance to itself is 0.
    # If there's a direct link between vertices (u, v), then the shortest path is the weight of the edge (u, v).
    distances = [[(INFINITY if i != j else 0) for j in graph.vertices] for i in graph.vertices]
    for edge in graph.edges:
        distances[edge.start_vertex.label][edge.end_vertex.label] = edge.weight

    # Allowing the shortest path to include only intermediate vertices with labels from 0 to k.
    for k in range(0, len(graph.vertices)):
        # Iterating through all pairs of vertices.
        for i in range(0, len(graph.vertices)):
            for j in range(0, len(graph.vertices)):
                # Could it be better to go through the vertex k instead of the currently known shortest path?
                if distances[i][j] > distances[i][k] + distances[k][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]

    return distances


class Vertex:
    def __init__(self, label):
        self.label = label
        self.inbound_edges = []
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
