def main():
    for graph_filename in ["graph01.txt", "graph02.txt"]:
        print "Solving {0}:".format(graph_filename)
        graph = read_graph_from_file(graph_filename)

        try:
            distances, predecessors = bellman_ford(graph, graph.vertices[0])
            print "Distances: ", distances
            print "Path predecessor vertices: ", predecessors
            print

        except NegativeCostCycleException:
            print "Cannot compute shortest paths: the graph has a negative-cost cycle."


def read_graph_from_file(filename):
    with open(filename, "r") as input_file:
        # The first two lines define the vertex count and the edge count.
        vertex_count = int(input_file.readline())
        edge_count = int(input_file.readline())

        vertices = [Vertex(index) for index in range(0, vertex_count)]
        edges = []

        # The next 'edge_count' lines describe the edges: "start_vertex end_vertex weight".
        for i in range(0, edge_count):
            edge_params = [int(index) for index in input_file.readline().split()]

            # Adding the edge to the list of outbound edges for the start vertex.
            edge = Edge(vertices[edge_params[0]], vertices[edge_params[1]], edge_params[2])
            vertices[edge_params[0]].outbound_edges.append(edge)
            vertices[edge_params[1]].inbound_edges.append(edge)

            # For non-directed graphs, an outbound edge is also an inbound one (0 -> 1 == 1 -> 0).
            # Therefore, we reverse the edge and add it to the other vertex.
            reverse_edge = Edge(vertices[edge_params[1]], vertices[edge_params[0]], edge_params[2])
            vertices[edge_params[1]].outbound_edges.append(reverse_edge)
            vertices[edge_params[0]].inbound_edges.append(reverse_edge)

            edges.append(edge)
            edges.append(reverse_edge)

        return Graph(vertices, edges)


def bellman_ford(graph, start_vertex):
    # Initialization of sub-problems:
    # For the start vertex, the shortest path with edge budget = 0 will be 0.
    # Other vertices will be unreachable given an edge budget of 0.
    INFINITY = 10 ** 9
    distances = [INFINITY for vertex in graph.vertices]
    distances[start_vertex.label] = 0
    predecessors = [None for vertex in graph.vertices]

    for edge_budget in range(1, len(graph.vertices) + 1):
        # For detecting negative cycles, we'll remember if Case 2 wins at least for one vertex.
        at_least_one_path_relaxed = False

        for vertex in graph.vertices:
            case1_distance = distances[vertex.label]
            case2_distance = INFINITY
            better_predecessor = None

            # This code could be more compact if we didn't want to return the actual paths in addition to distances.
            # Otherwise, we have to remember the inbound vertex that led us to the relaxed path.
            for inbound_edge in vertex.inbound_edges:
                candidate_distance = distances[inbound_edge.start_vertex.label] + inbound_edge.weight
                if candidate_distance < case2_distance:
                    case2_distance = candidate_distance
                    better_predecessor = inbound_edge.start_vertex

            if case2_distance < case1_distance:
                at_least_one_path_relaxed = True
                predecessors[vertex.label] = better_predecessor.label

            distances[vertex.label] = min(case1_distance, case2_distance)

        # If we don't have negative-cost cycles, nothing should change if we run one extra iteration of Bellman-Ford.
        # If some path has been relaxed even further, it means we've got a negative cycle and should raise an error.
        if edge_budget == len(graph.vertices) and at_least_one_path_relaxed:
            raise NegativeCostCycleException

    shortest_path_distances = [distances[vertex.label] for vertex in graph.vertices]
    return shortest_path_distances, predecessors


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


class NegativeCostCycleException(Exception):
    pass


if __name__ == "__main__":
    main()
