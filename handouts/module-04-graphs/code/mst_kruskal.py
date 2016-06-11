def mst_kruskal(graph):
    result = []

    # Populating the union-find data structure with all vertices.
    # Initially, none of the vertices are connected in the UF.
    uf = UnionFind(len(graph.vertices))
    for vertex in graph.vertices:
        uf.insert(vertex.label)

    # Sorting all edges by weight.
    sorted_edges = sorted(graph.edges, key=lambda e: e.weight)
    candidate_edge_index = 0

    # The MST of a connected graph will always have V-1 edges.
    while len(result) < len(graph.vertices) - 1:
        while True:
            # Greedily picking the cheapest edge IF it does not
            # introduce cycles in our MST. If it does, picking
            # the next best edge until we find a suitable one.
            min_edge = sorted_edges[candidate_edge_index]
            candidate_edge_index += 1
            if uf.find(min_edge.start_vertex.label) != \
               uf.find(min_edge.end_vertex.label):
                break

        result.append(min_edge)

        # Connect the start vertex and the end vertex in the UF.
        uf.union(min_edge.start_vertex.label, min_edge.end_vertex.label)

    # Return the list of edges that belong to the MST.
    return result
