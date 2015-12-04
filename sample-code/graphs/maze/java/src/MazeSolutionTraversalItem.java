public class MazeSolutionTraversalItem {

    private Cell cell;

    private int minPathLength;

    public MazeSolutionTraversalItem(Cell cell, int minPathLength) {
        this.cell = cell;
        this.minPathLength = minPathLength;
    }

    public Cell getCell() {
        return cell;
    }

    public int getMinPathLength() {
        return minPathLength;
    }
}
