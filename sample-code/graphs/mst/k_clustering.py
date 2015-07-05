import math
from union_find import ArrayUnionFind


def main():
    graph = read_graph_from_file("points01.txt")
    clusters = k_clustering(graph, 3)
    for cluster in clusters:
        print cluster


def read_graph_from_file(filename):
    with open(filename, "r") as input_file:
        # The first two lines define the vertex count and the edge count.
        vertex_count = int(input_file.readline())
        vertices = []
        edges = []

        # Reading all (X, Y) coordinates from file and storing them as vertices.
        for i in range(0, vertex_count):
            x, y = [float(coord) for coord in input_file.readline().split()]
            vertices.append(Vertex(i, x, y))

        # Precomputing the distances between each pair of points and storing the distances as edges.
        for i in range(0, vertex_count):
            for j in range(1, vertex_count):
                if i != j:
                    distance = euclidean_distance(vertices[i], vertices[j])
                    edge = Edge(vertices[i], vertices[j], distance)
                    reverse_edge = Edge(vertices[j], vertices[i], distance)

                    vertices[i].outbound_edges.append(edge)
                    vertices[j].outbound_edges.append(reverse_edge)

                    edges.append(edge)
                    edges.append(reverse_edge)

        return Graph(vertices, edges)


def k_clustering(graph, k):
    # Running the usual Kruskal's MST algorithm, with one modification: we stop when there's exactly K clusters.
    # In our case, it means we'll stop when there's K connected components in the Union-Find.

    # Populating the union-find data structure with all vertices.
    # Initially, none of the vertices are connected in the UF.
    uf = ArrayUnionFind(len(graph.vertices))
    for vertex in graph.vertices:
        uf.insert(vertex.label)

    # Sorting all edges by weight.
    sorted_edges = sorted(graph.edges, cmp=lambda a, b: cmp(a.weight, b.weight))
    candidate_edge_index = 0

    while uf.group_count() > k:
        while True:
            # Greedily picking the cheapest edge IF it does not introduce cycles in our MST.
            # If it does, picking the next best edge until we find a suitable one.
            min_edge = sorted_edges[candidate_edge_index]
            candidate_edge_index += 1
            if uf.find(min_edge.start_vertex.label) != uf.find(min_edge.end_vertex.label):
                break

        # Connect the start vertex and the end vertex in the UF.
        uf.union(min_edge.start_vertex.label, min_edge.end_vertex.label)

    # Returning the list of clusters indicating which vertices belong to each cluster.
    clusters = [[item.value for item in group.items] for group in uf.groups]
    return clusters


def euclidean_distance(vertex1, vertex2):
    return math.sqrt((vertex1.x - vertex2.x) ** 2 + (vertex1.y - vertex2.y) ** 2)


class Vertex:
    def __init__(self, label, x, y):
        self.label = label
        self.outbound_edges = []
        self.x = x
        self.y = y

    def __str__(self):
        return "Label: %d    Edges: %s" % (self.label, ', '.join([str(edge) for edge in self.outbound_edges]))


class Edge:
    def __init__(self, start_vertex, end_vertex, weight):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.weight = weight

    def __str__(self):
        return "%d ---%f---> %d" % (self.start_vertex.label, self.weight, self.end_vertex.label)


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


if __name__ == "__main__":
    main()
