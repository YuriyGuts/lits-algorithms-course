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
    return tarjan_dfs(graph, use_recursion=True)


def tarjan_dfs(graph, use_recursion=True):
    # Instead of keeping a boolean visited[] array, our visits will have 3 states.
    NOT_VISITED = 0
    VISITED = 1
    VISITED_AND_RESOLVED = 2

    topological_order = []
    topological_order_set = set()

    unvisited_vertices = set(graph.vertices)
    visited_status = [NOT_VISITED for vertex in graph.vertices]

    # A recursive, textbook implementation of Tarjan's DFS.
    def dfs_recursive(vertex):
        # We came across an unresolved dependency. It means there's a cycle in the graph.
        if visited_status[vertex.label] == VISITED:
            raise NotDirectedAcyclicGraphError

        if visited_status[vertex.label] == NOT_VISITED:
            unvisited_vertices.remove(vertex)
            visited_status[vertex.label] = VISITED

            # Getting all dependencies of the current vertex.
            neighbors = [edge.end_vertex for edge in vertex.outbound_edges]

            # Trying to recursively satisfy each dependency.
            for neighbor in neighbors:
                dfs_recursive(neighbor)

            # Marking this vertex as resolved and adding it to the order.
            visited_status[vertex.label] = VISITED_AND_RESOLVED
            topological_order.append(vertex)

    # An alternative stack-based implementation of DFS.
    # Particularly useful for Python due to its recursion limit.
    def dfs_stack(start_vertex):
        stack = [start_vertex]

        while len(stack) > 0:
            vertex = stack.pop()

            visited_status[vertex.label] = VISITED
            if vertex in unvisited_vertices:
                unvisited_vertices.remove(vertex)

            unvisited_neighbors = []
            for neighbor in [edge.end_vertex for edge in vertex.outbound_edges]:
                # We came across an unresolved dependency. It means there's a cycle in the graph.
                if visited_status[neighbor.label] == VISITED:
                    raise NotDirectedAcyclicGraphError
                # Getting all unexplored dependencies of the current vertex.
                if visited_status[neighbor.label] == NOT_VISITED:
                    unvisited_neighbors.append(neighbor)

            # If there are no more dependencies to explore, it means we've satisfied all of them
            # and we can add this vertex to the result of topological ordering.
            if len(unvisited_neighbors) == 0:
                visited_status[vertex.label] = VISITED_AND_RESOLVED
                # Avoid duplicates in the output.
                if vertex not in topological_order_set:
                    topological_order.append(vertex)
                    topological_order_set.add(vertex)
            else:
                # If there's something left to explore,
                # leaving the vertex in the stack along with all its neighbors.
                stack.append(vertex)
                stack.extend(unvisited_neighbors)

    # Using the stack-based implementation if the corresponding parameter was set.
    dfs_implementation = dfs_recursive if use_recursion else dfs_stack

    # Visit any unvisited vertex until there are no unvisited vertices left.
    while len(unvisited_vertices) > 0:
        dfs_implementation(next(iter(unvisited_vertices)))

    return topological_order


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
