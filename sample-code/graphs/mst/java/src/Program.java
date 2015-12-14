import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class Program {

    public static void main(String[] args) throws FileNotFoundException {
        Graph graph = readGraphFromFile("graph_int_labels_small.txt");

        List<MSTAlgorithm> algorithms = Arrays.asList(
                new MSTPrimNaive(),
                new MSTPrimHeap(),
                new MSTKruskal()
        );

        for (MSTAlgorithm algorithm: algorithms) {
            long startTime = System.currentTimeMillis();
            List<Edge> mstEdges = algorithm.computeMST(graph);
            long endTime = System.currentTimeMillis();

            System.out.println(algorithm.getClass().getName());
            System.out.printf("Time elapsed: %d ms\n", endTime - startTime);
            System.out.printf("MST cost: %d\n", mstEdges.stream().mapToInt(Edge::getWeight).sum());

            for (Edge edge: mstEdges) {
                System.out.println(edge.toString());
            }

            System.out.println();
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

            // The next 'edgeCount' lines describe the edges: "startVertex endVertex".
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
}
