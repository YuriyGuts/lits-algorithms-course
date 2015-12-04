public class CellCreatedEvent {

    private MazeGenerationTraversalItem traversalItem;

    public CellCreatedEvent(MazeGenerationTraversalItem traversalItem) {
        this.traversalItem = traversalItem;
    }

    public MazeGenerationTraversalItem getTraversalItem() {
        return traversalItem;
    }
}
