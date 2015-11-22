def main():
    graph = read_graph_from_file("graph01.txt")
    print bfs(graph, graph.vertices[0])
    print dfs(graph, graph.vertices[0])


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

            # For non-directed graphs, an outbound edge is also an inbound one (0 -> 1 == 1 -> 0).
            # Therefore, we reverse the edge and add it to the other vertex.
            reverse_edge = Edge(vertices[end_vertex], vertices[start_vertex])
            vertices[end_vertex].outbound_edges.append(reverse_edge)

            edges.append(edge)
            edges.append(reverse_edge)

        return Graph(vertices, edges)


def bfs(graph, start_vertex):
    result = []

    # Initially, the queue contains only the start vertex
    # and all vertices are assumed to be not visited yet.
    queue = [start_vertex]
    visited = [False for _ in range(0, len(graph.vertices))]

    while len(queue) > 0:
        # Remove a vertex from the queue.
        current_vertex = queue.pop(0)

        # If we've already been here, ignoring this vertex completely.
        # This condition can happen when, for example, this vertex was a neighbor of
        # two other vertices and they both added it to the queue before it was visited.
        if visited[current_vertex.label]:
            continue

        # Otherwise, marking it as visited so that we won't analyze it anymore.
        visited[current_vertex.label] = True

        # Getting all adjacent vertices which haven't been visited yet.
        # It's only a matter of traversing the outbound_edges list and getting end_vertex for each.
        neighbors = [edge.end_vertex
                     for edge in current_vertex.outbound_edges
                     if not visited[edge.end_vertex.label]]

        # If we need to enforce a particular ordering on the neighbors we visit,
        # e.g., visit them in the order of increasing labels (1, 4, 6; not 4, 6, 1),
        # this would be the place to do the sorting.

        # Adding these neighbors to the queue, all at once.
        result.append(current_vertex.label)
        queue.extend(neighbors)

    return result


# See the comments for BFS above.
# Note that the ONLY difference between BFS and DFS is using a queue vs. using a stack!
# In this Python implementation, it's only a matter of calling:
#    list.pop(0) (remove the leftmost item -> queue behavior, hence BFS)
#    list.pop()  (remove the rightmost item -> stack behavior, hence DFS)
def dfs(graph, start_vertex):
    result = []

    stack = [start_vertex]
    visited = [False for _ in range(0, len(graph.vertices))]

    while len(stack) > 0:
        current_vertex = stack.pop()
        if visited[current_vertex.label]:
            continue

        visited[current_vertex.label] = True
        neighbors = [edge.end_vertex
                     for edge in current_vertex.outbound_edges
                     if not visited[edge.end_vertex.label]]

        result.append(current_vertex.label)
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
