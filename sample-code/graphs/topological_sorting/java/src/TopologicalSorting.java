import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.stream.Collectors;

public class TopologicalSorting {

    public static void main(String[] args) throws FileNotFoundException {
        Graph graph = readGraphFromFile("graph01.txt");
        List<Vertex> orderedVertices = getTopologicalOrder(graph);
        String orderFormatted = orderedVertices.stream()
                .map(v -> String.valueOf(v.getLabel()))
                .collect(Collectors.joining(", "));
        System.out.println(orderFormatted);
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

            // The next 'edgeCount' lines describe the edges: "startVertex endVertex".
            for (int e = 0; e < edgeCount; e++) {
                int startVertexLabel = inputFileScanner.nextInt();
                int endVertexLabel = inputFileScanner.nextInt();

                Edge edge = new Edge(vertices.get(startVertexLabel), vertices.get(endVertexLabel));
                edges.add(edge);

                // Adding the edge to the list of outbound edges for the start vertex.
                vertices.get(startVertexLabel).getOutboundEdges().add(edge);
            }

            return new Graph(vertices, edges);
        }
    }

    private static List<Vertex> getTopologicalOrder(Graph graph) {
        TarjanTopologicalSorter tarjan = new TarjanTopologicalSorter();
        return tarjan.getTopologicalOrder(graph);
    }
}
