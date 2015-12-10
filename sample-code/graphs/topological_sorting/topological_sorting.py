import random


def main():
    graph = read_graph_from_file("graph01.txt")
    try:
        for vertex in get_topological_order(graph):
            print vertex.label,
    except NotDirectedAcyclicGraphError:
        print "The graph is not a directed acyclic graph (DAG)."


def read_graph_from_file(filename):
    with open(filename, "r") as input_file:
        # The first two lines define the vertex count and the edge count.
        vertex_count = int(input_file.readline())
        edge_count = int(input_file.readline())

        vertices = [Vertex(index) for index in range(0, vertex_count)]
        edges = []

        # The next 'edge_count' lines describe the edges: "start_vertex end_vertex".
        for i in range(0, edge_count):
            start_vertex, end_vertex = [int(index) for index in input_file.readline().split()]

            # Adding the edge to the list of outbound edges for the start vertex.
            edge = Edge(vertices[start_vertex], vertices[end_vertex])
            vertices[start_vertex].outbound_edges.append(edge)
            edges.append(edge)

        return Graph(vertices, edges)


def get_topological_order(graph):
    return tarjan_dfs(graph, randomize_result=True)


def tarjan_dfs(graph, randomize_result=False):
    # Instead of keeping a boolean visited[] array, our visits will have 3 states.
    NOT_VISITED = 0
    VISITED = 1
    VISITED_AND_RESOLVED = 2

    topological_order = []
    visited_status = [NOT_VISITED for vertex in graph.vertices]

    # A recursive implementation of DFS.
    def visit(vertex):
        # We came across an unresolved dependency. It means there's a cycle in the graph.
        if visited_status[vertex.label] == VISITED:
            raise NotDirectedAcyclicGraphError

        if visited_status[vertex.label] == NOT_VISITED:
            visited_status[vertex.label] = VISITED

            # Getting all dependencies of the current vertex.
            neighbors = [edge.end_vertex for edge in vertex.outbound_edges]

            if randomize_result:
                random.shuffle(neighbors)

            # Trying to recursively satisfy each dependency.
            for neighbor in neighbors:
                visit(neighbor)

            # Marking this vertex as resolved and adding it to the order.
            visited_status[vertex.label] = VISITED_AND_RESOLVED
            topological_order.append(vertex)

    # Visit any unvisited vertex until there are no unvisited vertices left.
    while True:
        unvisited_vertices = [
            vertex
            for vertex in graph.vertices
            if visited_status[vertex.label] == NOT_VISITED
        ]

        if len(unvisited_vertices) == 0:
            return topological_order
        else:
            if randomize_result:
                random.shuffle(unvisited_vertices)
            visit(unvisited_vertices[0])


class NotDirectedAcyclicGraphError:
    def __init__(self):
        pass


class Vertex:
    def __init__(self, label):
        self.label = label
        self.outbound_edges = []

    def __str__(self):
        return "Label: %d    Edges: %s" % (self.label, ', '.join([str(edge) for edge in self.outbound_edges]))


class Edge:
    def __init__(self, start_vertex, end_vertex):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex

    def __str__(self):
        return "%d -> %d" % (self.start_vertex.label, self.end_vertex.label)


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


if __name__ == "__main__":
    main()
