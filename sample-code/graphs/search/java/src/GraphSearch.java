import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.stream.*;

public class GraphSearch {

    public static void main(String[] args) throws FileNotFoundException {
        Graph graph = readGraphFromFile("graph01.txt");
        List<Vertex> bfsVertices = bfs(graph, graph.getVertices().get(0));
        List<Vertex> dfsVertices = dfs(graph, graph.getVertices().get(0));

        System.out.println("BFS traversal order:");
        System.out.println(bfsVertices.stream()
                .map(v -> String.valueOf(v.getLabel()))
                .collect(Collectors.joining(", ")));
        System.out.println();

        System.out.println("DFS traversal order:");
        System.out.println(dfsVertices.stream()
                .map(v -> String.valueOf(v.getLabel()))
                .collect(Collectors.joining(", ")));
    }

    private static Graph readGraphFromFile(String fileName) throws FileNotFoundException {
        File inputFile = new File(fileName);

        try (Scanner inputFileScanner = new Scanner(inputFile)) {
            // The first two lines define the vertex count and the edge count.
            int vertexCount = inputFileScanner.nextInt();
            int edgeCount = inputFileScanner.nextInt();

            List<Vertex> vertices = new ArrayList<>(vertexCount);
            List<Edge> edges = new ArrayList<>(edgeCount);

            for (int v = 0; v < vertexCount; v++) {
                vertices.add(v, new Vertex(v));
            }

            // The next 'edgeCount' lines describe the edges: "startVertex endVertex".
            for (int e = 0; e < edgeCount; e++) {
                int startVertexLabel = inputFileScanner.nextInt();
                int endVertexLabel = inputFileScanner.nextInt();

                Edge edge = new Edge(vertices.get(startVertexLabel), vertices.get(endVertexLabel));
                edges.add(edge);

                // Adding the edge to the list of outbound edges for the start vertex.
                vertices.get(startVertexLabel).getOutboundEdges().add(edge);

                // For non-directed graphs, an outbound edge is also an inbound one (0 -> 1 == 1 -> 0).
                // Therefore, we reverse the edge and add it to the other vertex.
                Edge reverseEdge = new Edge(vertices.get(endVertexLabel), vertices.get(startVertexLabel));
                edges.add(reverseEdge);
                vertices.get(endVertexLabel).getOutboundEdges().add(reverseEdge);
            }

            return new Graph(vertices, edges);
        }
    }

    private static List<Vertex> bfs(Graph graph, Vertex startVertex) {
        List<Vertex> traversalOrder = new ArrayList<>();

        // Initially, the queue contains only the start vertex
        // and all vertices are assumed to be not visited yet.
        Queue<Vertex> queue = new ArrayDeque<>();
        queue.add(startVertex);

        boolean[] isVisited = new boolean[graph.getVertices().size()];

        while (queue.size() > 0) {
            // Remove a vertex from the queue.
            Vertex currentVertex = queue.remove();

            // If we've already been here, ignoring this vertex completely.
            // This condition can happen when, for example, this vertex was a neighbor of
            // two other vertices and they both added it to the queue before it was visited.
            if (isVisited[currentVertex.getLabel()]) {
                continue;
            }

            // Otherwise, marking it as visited so that we won't analyze it anymore.
            isVisited[currentVertex.getLabel()] = true;

            // Getting all adjacent vertices which haven't been visited yet.
            // It's only a matter of traversing the outboundEdges list and getting endVertex for each.
            List<Vertex> unvisitedNeighbors = new ArrayList<>();
            for (Edge outboundEdge: currentVertex.getOutboundEdges()) {
                if (!isVisited[outboundEdge.getEndVertex().getLabel()]) {
                    unvisitedNeighbors.add(outboundEdge.getEndVertex());
                }
            }

            // If we need to enforce a particular ordering on the neighbors we visit,
            // e.g., visit them in the order of increasing labels (1, 4, 6; not 4, 6, 1),
            // this would be the place to do the sorting.

            // Adding the unvisited neighbors to the queue, all at once.
            queue.addAll(unvisitedNeighbors);

            // Adding the current vertex to the overall result.
            traversalOrder.add(currentVertex);
        }

        return traversalOrder;
    }

    private static List<Vertex> dfs(Graph graph, Vertex startVertex) {
        // See the comments for BFS above.
        // Note that the ONLY difference between BFS and DFS is using a queue vs. using a stack!
        List<Vertex> traversalOrder = new ArrayList<>();

        Stack<Vertex> stack = new Stack<>();
        stack.push(startVertex);
        boolean[] isVisited = new boolean[graph.getVertices().size()];

        while (stack.size() > 0) {
            Vertex currentVertex = stack.pop();

            if (isVisited[currentVertex.getLabel()]) {
                continue;
            }
            isVisited[currentVertex.getLabel()] = true;

            List<Vertex> unvisitedNeighbors = new ArrayList<>();
            for (Edge outboundEdge: currentVertex.getOutboundEdges()) {
                if (!isVisited[outboundEdge.getEndVertex().getLabel()]) {
                    unvisitedNeighbors.add(outboundEdge.getEndVertex());
                }
            }

            stack.addAll(unvisitedNeighbors);
            traversalOrder.add(currentVertex);
        }

        return traversalOrder;
    }
}
