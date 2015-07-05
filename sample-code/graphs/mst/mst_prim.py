def main():
    graph = read_graph_from_file("graph01.txt")
    mst_edges = mst_prim(graph)
    for edge in mst_edges:
        print edge


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


def mst_prim(graph):
    result = []
    already_belongs_to_mst = [False for _ in graph.vertices]

    # Including an arbitrary vertex in the MST (the first one, in our case).
    already_belongs_to_mst[0] = True

    # The MST of a connected graph will always have V-1 edges.
    while len(result) < len(graph.vertices) - 1:
        # Trying to extend our current MST with one more vertex.
        # Selecting the cheapest edge with one end in the MST and the other not in the MST.
        candidate_edges = [edge
                           for edge in graph.edges
                           if already_belongs_to_mst[edge.start_vertex.label] ^ already_belongs_to_mst[edge.end_vertex.label]]

        min_edge = min(candidate_edges, key=lambda e: e.weight)

        # Adding this edge to the MST and marking the vertices at both ends as consumed.
        result.append(min_edge)

        already_belongs_to_mst[min_edge.start_vertex.label] = True
        already_belongs_to_mst[min_edge.end_vertex.label] = True

    # Return the list of edges that belong to the MST.
    return result


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
