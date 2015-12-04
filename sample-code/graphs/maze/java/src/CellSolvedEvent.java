public class CellSolvedEvent {

    private MazeSolutionTraversalItem traversalItem;

    public CellSolvedEvent(MazeSolutionTraversalItem traversalItem) {
        this.traversalItem = traversalItem;
    }

    public MazeSolutionTraversalItem getTraversalItem() {
        return traversalItem;
    }
}
