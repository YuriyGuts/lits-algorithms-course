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
        # This condition can happen when, for example, this vertex was
        # a neighbor of two other vertices and they both added it
        # to the queue before it was visited.
        if visited[current_vertex.label]:
            continue

        # Otherwise, marking it as visited so that we won't analyze it anymore.
        visited[current_vertex.label] = True

        # Getting all adjacent vertices which haven't been visited yet.
        # It's only a matter of traversing the outbound_edges list
        # and getting end_vertex for each.
        neighbors = [
            edge.end_vertex
            for edge in current_vertex.outbound_edges
            if not visited[edge.end_vertex.label]
        ]

        # If we need to enforce a particular ordering on the neighbors we visit,
        # e.g., visit them in the order of increasing labels
        # (1, 4, 6; not 4, 6, 1), this would be the place to do the sorting.

        # Adding these neighbors to the queue, all at once.
        result.append(current_vertex.label)
        queue.extend(neighbors)

    return result
