import java.util.ArrayList;
import java.util.List;

public class DijkstraResult {

    private Vertex startVertex;

    private int[] distances;

    private Vertex[] shortestPathPredecessors;

    public Vertex getStartVertex() {
        return startVertex;
    }

    public int[] getDistances() {
        return distances;
    }

    public int getShortestDistanceToVertex(Vertex vertex) {
        return distances[vertex.getLabel()];
    }

    public List<Vertex> getShortestPathToVertex(Vertex vertex) {
        ArrayList<Vertex> path = new ArrayList<>();
        path.add(vertex);
        Vertex predecessor = shortestPathPredecessors[vertex.getLabel()];

        while (predecessor != null) {
            path.add(0, predecessor);
            predecessor = shortestPathPredecessors[predecessor.getLabel()];
        }

        return path;
    }

    public Vertex[] getShortestPathPredecessors() {
        return shortestPathPredecessors;
    }

    public DijkstraResult(Vertex startVertex, int[] distances, Vertex[] shortestPathPredecessors) {
        this.startVertex = startVertex;
        this.distances = distances;
        this.shortestPathPredecessors = shortestPathPredecessors;
    }
}
