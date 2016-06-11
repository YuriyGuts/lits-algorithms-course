def dijkstra(graph, start_vertex):
    # Initialization: setting all known shortest distances to infinity,
    # and the start vertex will have the shortest distance to itself equal to 0.
    INFINITY = 10 ** 10
    distances = [INFINITY for vertex in graph.vertices]
    distances[start_vertex.label] = 0

    # Visiting every vertex in the graph...
    visit_list = [vertex for vertex in graph.vertices]

    while len(visit_list) > 0:
        shortest_distance_vertex = visit_list[0]
        shortest_distance_index = 0

        # Finding the unvisited vertex with the least known distance:
        for (index, vertex) in enumerate(visit_list):
            if distances[vertex.label] < distances[shortest_distance_index]:
                shortest_distance_vertex = vertex
                shortest_distance_index = index

        visit_list.pop(shortest_distance_index)

        # For each adjacent vertex v, check if the path from the current vertex
        # would be more efficient than the one we've known before.
        # I.e., if distance[current] + weight(current->v) < distance[v].
        for edge in shortest_distance_vertex.outbound_edges:
            neighbor_label = edge.end_vertex.label
            alt_distance = distances[shortest_distance_vertex.label] + edge.weight

            # If we have indeed found a better path, remembering the new distance.
            if alt_distance < distances[neighbor_label]:
                distances[neighbor_label] = alt_distance

    return distances
