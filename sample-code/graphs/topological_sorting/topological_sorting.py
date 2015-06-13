def main():
    graph = read_graph_from_file("graph01.txt")
    print get_topological_order(graph)


def read_graph_from_file(filename):
    with open(filename, "r") as input_file:
        # The first two lines define the vertex count and the edge count.
        vertex_count = int(input_file.readline())
        edge_count = int(input_file.readline())

        vertices = [Vertex(index) for index in range(0, vertex_count)]
        edges = []

        # The next 'edge_count' lines describe the edges: "start_vertex end_vertex".
        for i in range(0, edge_count):
            edge_indices = [int(index) for index in input_file.readline().split()]

            # Adding the edge to the list of outbound edges for the start vertex.
            edge = Edge(vertices[edge_indices[0]], vertices[edge_indices[1]])
            vertices[edge_indices[0]].outbound_edges.append(edge)
            edges.append(edge)

        return Graph(vertices, edges)


def get_topological_order(graph):
    # Find all vertices that don't have inbound edges, then run
    # the (almost) usual DFS with those vertices initially in the stack.
    return dfs(graph, get_vertices_without_inbound_edges(graph))


def get_vertices_without_inbound_edges(graph):
    have_inbounds = {vertex: False for vertex in graph.vertices}
    for edge in graph.edges:
        have_inbounds[edge.end_vertex] = True
    return [vertex for vertex in have_inbounds.keys() if not have_inbounds[vertex]]


def dfs(graph, start_vertices):
    result = []

    stack = []
    stack.extend(start_vertices)
    visited = [False for _ in graph.vertices]

    while len(stack) > 0:
        # Read the last vertex from the stack, but don't remove it.
        current_vertex = stack[-1]

        visited[current_vertex.label] = True
        neighbors = [edge.end_vertex
                     for edge in current_vertex.outbound_edges
                     if not visited[edge.end_vertex.label]]

        # If all neighbors have already been discovered (or don't exist at all),
        # push the current vertex to the results of the topological sorting.
        if len(neighbors) == 0:
            result.append(current_vertex.label)
            stack.pop()

        stack.extend(neighbors)

    return result


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
