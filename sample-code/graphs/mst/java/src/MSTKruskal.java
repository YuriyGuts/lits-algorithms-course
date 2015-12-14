import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class MSTKruskal extends MSTAlgorithm {

    @Override
    public List<Edge> computeMST(Graph graph) {
        List<Edge> result = new ArrayList<>();

        // Populating the union-find data structure with all vertices.
        // Initially, none of the vertices are connected in the UF.
        UnionFind uf = new ArrayUnionFind(graph.getVertices().size());
        for (Vertex vertex: graph.getVertices()) {
            uf.insert(vertex.getLabel());
        }

        // Sorting all edges by weight.
        Comparator<Edge> edgeWeightComparator = (e1, e2) -> Integer.valueOf(e1.getWeight()).compareTo(e2.getWeight());
        List<Edge> sortedEdges = new ArrayList<>(graph.getEdges());
        Collections.sort(sortedEdges, edgeWeightComparator);

        int candidateEdgeIndex = 0;

        // The MST of a connected graph will always have V-1 edges.
        while (result.size() < graph.getVertices().size() - 1) {
            // Greedily picking the cheapest edge IF it does not introduce cycles in our MST.
            // If it does, picking the next best edge until we find a suitable one.
            Edge minEdge;
            do {
                minEdge = sortedEdges.get(candidateEdgeIndex++);
            }
            while (uf.find(minEdge.getStartVertex().getLabel()) == uf.find(minEdge.getEndVertex().getLabel()));
            result.add(minEdge);

            // Connect the start vertex and the end vertex in the UF.
            uf.union(minEdge.getStartVertex().getLabel(), minEdge.getEndVertex().getLabel());
        }

        // Return the list of edges that belong to the MST.
        return result;
    }
}
