import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

public class MSTPrimHeap extends MSTAlgorithm {

    @Override
    public List<Edge> computeMST(Graph graph) {
        List<Edge> result = new ArrayList<>(graph.getVertices().size());
        boolean[] alreadyBelongsToMST = new boolean[graph.getVertices().size()];

        // The heap will allow us to quickly pick the cheapest edge among the candidates.
        Comparator<Edge> edgeWeightComparator = (e1, e2) -> Integer.valueOf(e1.getWeight()).compareTo(e2.getWeight());
        PriorityQueue<Edge> heap = new PriorityQueue<>(graph.getEdges().size(), edgeWeightComparator);

        // Including an arbitrary vertex in the MST (the first one, in our case).
        // It's safe to do so, because an MST must contain all vertices by definition.
        Vertex randomVertex = graph.getVertices().get(0);
        alreadyBelongsToMST[randomVertex.getLabel()] = true;
        heap.addAll(randomVertex.getOutboundEdges());

        // The MST of a connected graph will always have V-1 edges.
        while (result.size() < graph.getVertices().size() - 1) {
            // Trying to extend our current MST with one more vertex.
            // Selecting the cheapest edge with one end in the MST and the other not in the MST.
            Edge minEdge;
            do {
                minEdge = heap.remove();
            }
            while (alreadyBelongsToMST[minEdge.getStartVertex().getLabel()] == alreadyBelongsToMST[minEdge.getEndVertex().getLabel()]);

            Vertex vertexToAdd = alreadyBelongsToMST[minEdge.getStartVertex().getLabel()]
                    ? minEdge.getEndVertex()
                    : minEdge.getStartVertex();

            // Adding this edge to the MST and marking the vertices at both ends as consumed.
            result.add(minEdge);
            heap.addAll(vertexToAdd.getOutboundEdges());
            alreadyBelongsToMST[vertexToAdd.getLabel()] = true;
        }

        // Return the list of edges that belong to the MST.
        return result;
    }
}
