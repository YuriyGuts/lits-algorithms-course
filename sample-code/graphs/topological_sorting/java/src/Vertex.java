import java.util.ArrayList;
import java.util.List;

public class Vertex {

    private int label;

    private List<Edge> outboundEdges;

    public int getLabel() {
        return label;
    }

    public void setLabel(int label) {
        this.label = label;
    }

    public List<Edge> getOutboundEdges() {
        return outboundEdges;
    }

    public Vertex(int label) {
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
