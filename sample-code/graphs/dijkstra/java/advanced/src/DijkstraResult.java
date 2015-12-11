import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class DijkstraResult {

    private Vertex startVertex;

    private Map<Vertex, Integer> distances;

    private Map<Vertex, Vertex> shortestPathPredecessors;

    public Vertex getStartVertex() {
        return startVertex;
    }

    public Map<Vertex, Integer> getDistances() {
        return distances;
    }

    public int getShortestDistanceToVertex(Vertex vertex) {
        return distances.get(vertex);
    }

    public List<Vertex> getShortestPathToVertex(Vertex vertex) {
        ArrayList<Vertex> path = new ArrayList<>();
        path.add(vertex);
        Vertex predecessor = shortestPathPredecessors.get(vertex);

        while (predecessor != null) {
            path.add(0, predecessor);
            predecessor = shortestPathPredecessors.get(predecessor);
        }

        return path;
    }

    public Map<Vertex, Vertex> getShortestPathPredecessors() {
        return shortestPathPredecessors;
    }

    public DijkstraResult(Vertex startVertex, Map<Vertex, Integer> distances, Map<Vertex, Vertex> shortestPathPredecessors) {
        this.startVertex = startVertex;
        this.distances = distances;
        this.shortestPathPredecessors = shortestPathPredecessors;
    }
}
