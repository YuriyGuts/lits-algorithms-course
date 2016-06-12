def tarjan_dfs(graph):
    # Instead of keeping a boolean visited[] array,
    # our visits will have 3 states.
    NOT_VISITED = 0
    VISITED = 1
    VISITED_AND_RESOLVED = 2

    # Remembering which vertices are already included in the topological order.
    topological_order = []
    topological_order_set = set()

    unvisited_vertices = set(graph.vertices)
    visited_status = [NOT_VISITED for vertex in graph.vertices]

    # A recursive, textbook implementation of Tarjan's DFS.
    def dfs_recursive(vertex):
        # We came across an unresolved dependency.
        # It means there's a cycle in the graph.
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


    # Visit any unvisited vertex until there are no unvisited vertices left.
    while len(unvisited_vertices) > 0:
        dfs_recursive(next(iter(unvisited_vertices)))

    return topological_order
