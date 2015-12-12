import java.util.*;

public class TarjanTopologicalSorter {

    // Instead of keeping a boolean visited[] array, our visits will have 3 states.
    private enum VisitedStatus {
        NotVisited,
        Visited,
        VisitedAndResolved
    }

    private boolean useRecursion;

    private List<Vertex> order;

    private Set<Vertex> orderSet;

    private Set<Vertex> unvisitedVertices;

    private List<VisitedStatus> visitedStatus;

    public TarjanTopologicalSorter() {
        this(true);
    }

    public TarjanTopologicalSorter(boolean useRecursion) {
        this.useRecursion = useRecursion;
    }

    public List<Vertex> getTopologicalOrder(Graph graph) {
        order = new ArrayList<>();
        orderSet = new HashSet<>(graph.getVertices().size());
        unvisitedVertices = new HashSet<>(graph.getVertices().size());
        visitedStatus = new ArrayList<>(graph.getVertices().size());

        for (Vertex vertex: graph.getVertices()) {
            unvisitedVertices.add(vertex);
            visitedStatus.add(VisitedStatus.NotVisited);
        }

        // Visit any unvisited vertex until there are no unvisited vertices left.
        while (unvisitedVertices.size() > 0) {
            Vertex unvisitedVertex = unvisitedVertices.stream().findFirst().get();

            // Using the stack-based implementation if the corresponding parameter was set.
            if (useRecursion) {
                dfsRecursive(unvisitedVertex);
            } else {
                dfsStack(unvisitedVertex);
            }
        }

        return order;
    }

    // A recursive, textbook implementation of Tarjan's DFS.
    private void dfsRecursive(Vertex vertex) {
        // We came across an unresolved dependency. It means there's a cycle in the graph.
        if (visitedStatus.get(vertex.getLabel()) == VisitedStatus.Visited) {
            throw new NotDirectedAcyclicGraphException();
        }

        if (visitedStatus.get(vertex.getLabel()) == VisitedStatus.NotVisited) {
            visitedStatus.set(vertex.getLabel(), VisitedStatus.Visited);
            unvisitedVertices.remove(vertex);

            // Getting all dependencies of the current vertex.
            List<Vertex> neighbors = new ArrayList<>();
            for (Edge edge: vertex.getOutboundEdges()) {
                neighbors.add(edge.getEndVertex());
            }

            for (Vertex neighbor: neighbors) {
                dfsRecursive(neighbor);
            }

            visitedStatus.set(vertex.getLabel(), VisitedStatus.VisitedAndResolved);
            order.add(vertex);
        }
    }

    // An alternative stack-based implementation of DFS.
    // Particularly useful for large graphs or small thread stack sizes.
    private void dfsStack(Vertex startVertex) {
        Stack<Vertex> stack = new Stack<>();
        stack.push(startVertex);

        while (!stack.empty()) {
            Vertex vertex = stack.pop();
            visitedStatus.set(vertex.getLabel(), VisitedStatus.Visited);
            if (unvisitedVertices.contains(vertex)) {
                unvisitedVertices.remove(vertex);
            }

            List<Vertex> unvisitedNeighbors = new ArrayList<>();
            for (Edge outboundEdge: vertex.getOutboundEdges()) {
                Vertex neighbor = outboundEdge.getEndVertex();

                // We came across an unresolved dependency. It means there's a cycle in the graph.
                if (visitedStatus.get(neighbor.getLabel()) == VisitedStatus.Visited) {
                    throw new NotDirectedAcyclicGraphException();
                }
                // Getting all unexplored dependencies of the current vertex.
                if (visitedStatus.get(neighbor.getLabel()) == VisitedStatus.NotVisited) {
                    unvisitedNeighbors.add(neighbor);
                }
            }

            // If there are no more dependencies to explore, it means we've satisfied all of them
            // and we can add this vertex to the result of topological ordering.
            if (unvisitedNeighbors.isEmpty()) {
                visitedStatus.set(vertex.getLabel(), VisitedStatus.VisitedAndResolved);
                if (!orderSet.contains(vertex)) {
                    order.add(vertex);
                    orderSet.add(vertex);
                }
            } else {
                // If there's something left to explore,
                // leaving the vertex in the stack along with all its neighbors.
                stack.push(vertex);
                stack.addAll(unvisitedNeighbors);
            }
        }
    }
}
