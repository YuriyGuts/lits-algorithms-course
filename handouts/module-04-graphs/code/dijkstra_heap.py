import heapq

def dijkstra(graph, start_vertex):
    # Initialization: setting all known shortest distances to infinity,
    # and the start vertex will have the shortest distance to itself equal to 0.
    INFINITY = 10 ** 15
    distances = [INFINITY] * len(graph.vertices)
    distances[start_vertex.label] = 0

    # The heap will allow us to quickly pick an unvisited vertex
    # with the least known distance.
    # The implementation of heapq requires us to store (key, value) tuples
    # so we'll store (distance, vertex) tuples.
    heap = []
    heapq.heappush(heap, (0, start_vertex.label))

    while len(heap) > 0:
        # Picking the vertex with the smallest known distance so far.
        distance, shortest_distance_label = heapq.heappop(heap)
        shortest_distance_vertex = graph.vertices[shortest_distance_label]

        # For each adjacent vertex v, check if the path from the
        # current vertex would be more efficient than the one we've known before.
        # I.e., if distance[current] + weight(current->v) < distance[v].
        for edge in shortest_distance_vertex.outbound_edges:
            neighbor_label = edge.end_vertex
            alt_distance = distances[shortest_distance_vertex.label] + edge.weight

            # If we have indeed found a better path,
            # remembering the new distance and predecessor.
            if alt_distance < distances[neighbor_label]:
                distances[neighbor_label] = alt_distance

                # Pushing the new distance to the heap.
                heapq.heappush(heap, (alt_distance, neighbor_label))

    return distances
