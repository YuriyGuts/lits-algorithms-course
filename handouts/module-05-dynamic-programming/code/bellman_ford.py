def bellman_ford(graph, start_vertex):
    # Initialization of sub-problems:
    # For the start vertex, the shortest path with edge budget = 0 will be 0.
    # Other vertices will be unreachable given an edge budget of 0.
    INFINITY = 10 ** 9
    distances = [INFINITY for vertex in graph.vertices]
    distances[start_vertex.label] = 0
    predecessors = [None for vertex in graph.vertices]

    for edge_budget in range(1, len(graph.vertices) + 1):
        # For detecting negative cycles,
        # we'll remember if Case 2 wins at least for one vertex.
        at_least_one_path_relaxed = False

        for vertex in graph.vertices:
            # Case 1: follow the path known before.
            case1_distance = distances[vertex.label]
            # Case 2: try reaching the current vertex through its inbound neighbors
            # that are reachable in 'edge_budget - 1' steps.
            case2_distance = INFINITY
            better_predecessor = None

            # This code could be more compact if we didn't want to
            # return the actual paths in addition to distances.
            # Otherwise, we have to remember the inbound vertex
            # that led us to the relaxed path.
            for inbound_edge in vertex.inbound_edges:
                candidate_distance = distances[inbound_edge.start_vertex.label] \
                    + inbound_edge.weight
                    
                if candidate_distance < case2_distance:
                    case2_distance = candidate_distance
                    better_predecessor = inbound_edge.start_vertex

            if case2_distance < case1_distance:
                at_least_one_path_relaxed = True
                predecessors[vertex.label] = better_predecessor.label

            distances[vertex.label] = min(case1_distance, case2_distance)

        # If we don't have negative-cost cycles, nothing should
        # change if we run one extra iteration of Bellman-Ford.
        # If some path has been relaxed even further, it means
        # we've got a negative cycle and should raise an error.
        if edge_budget == len(graph.vertices) and at_least_one_path_relaxed:
            raise NegativeCostCycleException

    shortest_path_distances = [distances[vertex.label] for vertex in graph.vertices]
    return shortest_path_distances, predecessors
