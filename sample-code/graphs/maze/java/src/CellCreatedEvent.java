public class CellCreatedEvent {

    private MazeTraversalItem traversalItem;

    public CellCreatedEvent(MazeTraversalItem traversalItem) {
        this.traversalItem = traversalItem;
    }

    public MazeTraversalItem getTraversalItem() {
        return traversalItem;
    }
}
