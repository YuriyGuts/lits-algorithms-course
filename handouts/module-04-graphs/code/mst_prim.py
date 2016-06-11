def mst_prim(graph):
    result = []
    heap = []
    already_belongs_to_mst = {label: False for label in graph.vertices}

    # Including an arbitrary vertex in the MST.
    # It's safe to do so, because an MST must contain all vertices by definition.
    random_label = graph.vertices.iterkeys().next()
    already_belongs_to_mst[random_label] = True
    for edge in graph.vertices[random_label].outbound_edges:
        heapq.heappush(heap, (edge.weight, edge))

    # The MST of a connected graph will always have V-1 edges.
    while len(result) < len(graph.vertices) - 1:
        # Trying to extend our current MST with one more vertex.
        # Selecting the cheapest edge with one end in the MST
        # and the other not in the MST.
        min_edge = None
        while True:
            min_weight, min_edge = heapq.heappop(heap)
            if already_belongs_to_mst[min_edge.start_vertex.label] \
                != already_belongs_to_mst[min_edge.end_vertex.label]:
                break

        vertex_to_add = min_edge.end_vertex \
            if not already_belongs_to_mst[min_edge.end_vertex.label] \
            else min_edge.start_vertex

        # Adding this edge to the MST and marking
        # the vertices at both ends as consumed.
        result.append(min_edge)
        for edge in vertex_to_add.outbound_edges:
            heapq.heappush(heap, (edge.weight, edge))

        already_belongs_to_mst[vertex_to_add.label] = True

    # Return the list of edges that belong to the MST.
    return result
