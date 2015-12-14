import java.util.ArrayList;
import java.util.List;

public class MSTPrimNaive extends MSTAlgorithm {

    @Override
    public List<Edge> computeMST(Graph graph) {
        List<Edge> result = new ArrayList<>(graph.getVertices().size());
        boolean[] alreadyBelongsToMST = new boolean[graph.getVertices().size()];

        // Including an arbitrary vertex in the MST (the first one, in our case).
        // It's safe to do so, because an MST must contain all vertices by definition.
        Vertex randomVertex = graph.getVertices().get(0);
        alreadyBelongsToMST[randomVertex.getLabel()] = true;

        // The MST of a connected graph will always have V-1 edges.
        while (result.size() < graph.getVertices().size() - 1) {
            // Trying to extend our current MST with one more vertex.
            // Selecting the cheapest edge with one end in the MST and the other not in the MST.
            Edge minEdge = null;
            for (Edge edge: graph.getEdges()) {
                if (alreadyBelongsToMST[edge.getStartVertex().getLabel()] != alreadyBelongsToMST[edge.getEndVertex().getLabel()]
                        && (minEdge == null || edge.getWeight() < minEdge.getWeight())) {
                    minEdge = edge;
                }
            }

            // Adding this edge to the MST and marking the vertices at both ends as consumed.
            result.add(minEdge);
            alreadyBelongsToMST[minEdge.getStartVertex().getLabel()] = true;
            alreadyBelongsToMST[minEdge.getEndVertex().getLabel()] = true;
        }

        // Return the list of edges that belong to the MST.
        return result;
    }
}
