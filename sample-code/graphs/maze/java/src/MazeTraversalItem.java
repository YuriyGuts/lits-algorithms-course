public class MazeTraversalItem {

    private Cell currentCell;

    private Cell previousCell;

    public MazeTraversalItem(Cell currentCell, Cell previousCell) {
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
