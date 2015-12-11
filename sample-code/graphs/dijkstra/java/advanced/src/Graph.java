import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Graph {

    private Map<String, Vertex> vertices;

    private List<Edge> edges;

    public Map<String, Vertex> getVertices() {
        return vertices;
    }

    public List<Edge> getEdges() {
        return edges;
    }

    public Graph() {
        this.vertices = new HashMap<>();
        this.edges = new ArrayList<>();
    }

    public Graph(Map<String, Vertex> vertices, List<Edge> edges) {
        this.vertices = vertices;
        this.edges = edges;
    }
}
