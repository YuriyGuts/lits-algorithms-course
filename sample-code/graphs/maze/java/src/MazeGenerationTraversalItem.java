public class MazeGenerationTraversalItem {

    private Cell currentCell;

    private Cell previousCell;

    public MazeGenerationTraversalItem(Cell currentCell, Cell previousCell) {
        this.currentCell = currentCell;
        this.previousCell = previousCell;
    }

    public Cell getCurrentCell() {
        return currentCell;
    }

    public Cell getPreviousCell() {
        return previousCell;
    }
}
