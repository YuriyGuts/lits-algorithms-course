import java.util.ArrayList;
import java.util.List;

public class Vertex {

    private String label;

    private List<Edge> outboundEdges;

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public List<Edge> getOutboundEdges() {
        return outboundEdges;
    }

    public Vertex(String label) {
        this.label = label;
        this.outboundEdges = new ArrayList<>();
    }

    @Override
    public String toString() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("Label: ");
        stringBuilder.append(label);

        stringBuilder.append("   Edges: ");
        for (Edge edge: outboundEdges) {
            stringBuilder.append(edge.toString());
            stringBuilder.append(", ");
        }

        return stringBuilder.toString();
    }
}
