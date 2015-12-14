from union_find import ArrayUnionFind


def main():
    graph = read_graph_from_file("graph_int_labels_01.txt")
    mst_edges = mst_kruskal(graph)
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


def mst_kruskal(graph):
    result = []

    # Populating the union-find data structure with all vertices.
    # Initially, none of the vertices are connected in the UF.
    uf = ArrayUnionFind(len(graph.vertices))
    for vertex in graph.vertices:
        uf.insert(vertex.label)

    # Sorting all edges by weight.
    sorted_edges = sorted(graph.edges, cmp=lambda a, b: cmp(a.weight, b.weight))
    candidate_edge_index = 0

    # The MST of a connected graph will always have V-1 edges.
    while len(result) < len(graph.vertices) - 1:
        while True:
            # Greedily picking the cheapest edge IF it does not introduce cycles in our MST.
            # If it does, picking the next best edge until we find a suitable one.
            min_edge = sorted_edges[candidate_edge_index]
            candidate_edge_index += 1
            if uf.find(min_edge.start_vertex.label) != uf.find(min_edge.end_vertex.label):
                break

        result.append(min_edge)

        # Connect the start vertex and the end vertex in the UF.
        uf.union(min_edge.start_vertex.label, min_edge.end_vertex.label)

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
