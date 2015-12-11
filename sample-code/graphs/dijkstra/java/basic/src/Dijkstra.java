import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.stream.Collectors;

public class Dijkstra {

    public static void main(String[] args) throws FileNotFoundException {
        Graph graph = readGraphFromFile("weighted_graph_01.txt");
        DijkstraResult result = getShortestPathsDijkstra(graph, graph.getVertices().get(0));

        // Print distances and routes.
        for (Vertex vertex: graph.getVertices()) {
            int distance = result.getShortestDistanceToVertex(vertex);
            String formattedPath = result.getShortestPathToVertex(vertex).stream()
                    .map(v -> String.valueOf(v.getLabel()))
                    .collect(Collectors.joining(" -> "));

            System.out.printf("%d: %d\t(%s)\n", vertex.getLabel(), distance, formattedPath);
        }
    }

    @SuppressWarnings("Duplicates")
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

            // The next 'edgeCount' lines describe the edges: "startVertex endVertex weight".
            for (int e = 0; e < edgeCount; e++) {
                int startVertexLabel = inputFileScanner.nextInt();
                int endVertexLabel = inputFileScanner.nextInt();
                int weight = inputFileScanner.nextInt();

                Edge edge = new Edge(vertices.get(startVertexLabel), vertices.get(endVertexLabel), weight);
                edges.add(edge);

                // Adding the edge to the list of outbound edges for the start vertex.
                vertices.get(startVertexLabel).getOutboundEdges().add(edge);

                // For non-directed graphs, an outbound edge is also an inbound one (0 -> 1 == 1 -> 0).
                // Therefore, we reverse the edge and add it to the other vertex.
                Edge reverseEdge = new Edge(vertices.get(endVertexLabel), vertices.get(startVertexLabel), weight);
                edges.add(reverseEdge);
                vertices.get(endVertexLabel).getOutboundEdges().add(reverseEdge);
            }

            return new Graph(vertices, edges);
        }
    }

    public static DijkstraResult getShortestPathsDijkstra(Graph graph, Vertex startVertex) {
        int[] distances = new int[graph.getVertices().size()];
        Vertex[] shortestPathPredecessors = new Vertex[graph.getVertices().size()];

        // Initialization: setting all known shortest distances to infinity,
        // and the start vertex will have the shortest distance to itself equal to 0.
        final int INFINITY = Integer.MAX_VALUE;
        for (Vertex vertex: graph.getVertices()) {
            distances[vertex.getLabel()] = INFINITY;
        }
        distances[startVertex.getLabel()] = 0;

        // Visiting every vertex in the graph...
        ArrayList<Vertex> visitList = new ArrayList<>(graph.getVertices().size());
        for (Vertex vertex: graph.getVertices()) {
            visitList.add(vertex);
        }

        while (visitList.size() > 0) {
            // ...but selecting the vertex with the shortest known distance every time.
            //
            // We can avoid doing the linear-time lookup every time by using a Fibonacci Heap instead,
            // thus reducing the complexity from O(V ^ 2) to O(E + V log V).
            Vertex shortestDistanceVertex = visitList.get(0);
            int shortestDistanceIndex = 0;

            for (int i = 0; i < graph.getVertices().size(); i++) {
                if (distances[i] < distances[shortestDistanceIndex]) {
                    shortestDistanceVertex = graph.getVertices().get(i);
                    shortestDistanceIndex = i;
                }
            }

            visitList.remove(shortestDistanceIndex);

            // For each adjacent vertex v, check if the path from the current vertex would be more efficient
            // than the one we've known before. I.e., if distance[current] + weight(current->v) < distance[v].
            for (Edge edge: shortestDistanceVertex.getOutboundEdges()) {
                Vertex neighborVertex = edge.getEndVertex();
                int alternativeDistance = distances[shortestDistanceVertex.getLabel()] + edge.getWeight();

                // If we have indeed found a better path, remembering the new distance and predecessor.
                if (alternativeDistance < distances[neighborVertex.getLabel()]) {
                    distances[neighborVertex.getLabel()] = alternativeDistance;
                    shortestPathPredecessors[neighborVertex.getLabel()] = shortestDistanceVertex;
                }
            }
        }

        return new DijkstraResult(startVertex, distances, shortestPathPredecessors);
    }
}
