import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.stream.Collectors;

public class Dijkstra {

    public static void main(String[] args) throws FileNotFoundException {
        Graph graph = readGraphFromFile("string_weighted_graph_01.txt");
        DijkstraResult result = getShortestPathsDijkstra(graph, graph.getVertices().get("a"));

        // Print distances and routes.
        for (Vertex vertex: graph.getVertices().values()) {
            int distance = result.getShortestDistanceToVertex(vertex);
            String formattedPath = result.getShortestPathToVertex(vertex).stream()
                    .map(v -> String.valueOf(v.getLabel()))
                    .collect(Collectors.joining(" -> "));

            System.out.printf("%s: %d\t(%s)\n", vertex.getLabel(), distance, formattedPath);
        }
    }

    @SuppressWarnings("Duplicates")
    private static Graph readGraphFromFile(String fileName) throws FileNotFoundException {
        File inputFile = new File(fileName);

        try (Scanner inputFileScanner = new Scanner(inputFile)) {
            // The first two lines define the vertex count and the edge count.
            int vertexCount = inputFileScanner.nextInt();
            int edgeCount = inputFileScanner.nextInt();

            Map<String, Vertex> vertices = new HashMap<>(vertexCount);
            List<Edge> edges = new ArrayList<>(edgeCount);

            // The next 'edgeCount' lines describe the edges: "startVertex endVertex weight".
            for (int e = 0; e < edgeCount; e++) {
                String startVertexLabel = inputFileScanner.next("\\S+");
                String endVertexLabel = inputFileScanner.next("\\S+");
                int weight = inputFileScanner.nextInt();

                if (!vertices.containsKey(startVertexLabel)) {
                    vertices.put(startVertexLabel, new Vertex(startVertexLabel));
                }
                if (!vertices.containsKey(endVertexLabel)) {
                    vertices.put(endVertexLabel, new Vertex(endVertexLabel));
                }

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
        Map<Vertex, Integer> distances = new HashMap<>(graph.getVertices().size());
        Map<Vertex, Vertex> shortestPathPredecessors = new HashMap<>(graph.getVertices().size());

        // Initialization: setting all known shortest distances to infinity,
        // and the start vertex will have the shortest distance to itself equal to 0.
        final int INFINITY = Integer.MAX_VALUE;
        for (Vertex vertex: graph.getVertices().values()) {
            distances.put(vertex, INFINITY);
        }
        distances.put(startVertex, 0);

        // The heap will allow us to quickly pick an unvisited vertex with the least known distance.
        Comparator<Vertex> vertexDistanceComparator = (v1, v2) -> distances.get(v1).compareTo(distances.get(v2));
        PriorityQueue<Vertex> heap = new PriorityQueue<>(vertexDistanceComparator);
        heap.add(startVertex);

        while (heap.size() > 0) {
            // Picking the vertex with the smallest known distance so far.
            Vertex shortestDistanceVertex = heap.remove();

            // For each adjacent vertex v, check if the path from the current vertex would be more efficient
            // than the one we've known before. I.e., if distance[current] + weight(current->v) < distance[v].
            for (Edge edge: shortestDistanceVertex.getOutboundEdges()) {
                Vertex neighborVertex = edge.getEndVertex();
                int alternativeDistance = distances.get(shortestDistanceVertex) + edge.getWeight();

                // If we have indeed found a better path, remembering the new distance and predecessor.
                if (alternativeDistance < distances.get(neighborVertex)) {
                    distances.put(neighborVertex, alternativeDistance);
                    shortestPathPredecessors.put(neighborVertex, shortestDistanceVertex);

                    // Pushing the new vertex to the heap.
                    heap.add(neighborVertex);
                }
            }
        }

        return new DijkstraResult(startVertex, distances, shortestPathPredecessors);
    }
}
