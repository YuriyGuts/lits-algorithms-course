import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Stack;
import java.util.function.Consumer;

public class MazeGenerator {

    private Maze maze;

    public MazeGenerator(int width, int height) {
        this.maze = new Maze(width, height);
    }

    public Maze getMaze() {
        return maze;
    }

    public Maze generate(Consumer<CellCreatedEvent> cellCreatedCallback) {
        // Just doing the typical DFS: putting the start cell in the stack.
        // But in order to generate a maze, we'll also remember the cell we came from.
        // Whenever we process a new cell, we'll break the wall between the current cell
        // and the cell we came from. Therefore, we'll need to store multiple values in one stack item.
        // We'll wrap these (currentCell, previousCell) pairs in the MazeGenerationTraversalItem class.
        Stack<MazeGenerationTraversalItem> stack = new Stack<>();
        stack.push(new MazeGenerationTraversalItem(maze.getCellByCoordinate(0, 0), null));

        boolean[][] visited = new boolean[maze.getHeight()][maze.getWidth()];

        while (!stack.empty()) {
            // Retrieve another pair of cells from the stack.
            MazeGenerationTraversalItem traversalItem = stack.pop();
            Cell currentCell = traversalItem.getCurrentCell();
            Cell previousCell = traversalItem.getPreviousCell();

            // Ignoring the cell if we've already been there.
            if (visited[currentCell.getY()][currentCell.getX()]) {
                continue;
            }

            // Mark this cell so we won't visit it anymore.
            visited[currentCell.getY()][currentCell.getX()] = true;

            // Break the wall between the current cell and the previous cell.
            if (previousCell != null) {
                maze.breakWallBetweenCells(currentCell, previousCell);

                // Notify the UI that we've created a new cell.
                if (cellCreatedCallback != null) {
                    cellCreatedCallback.accept(new CellCreatedEvent(traversalItem));
                }
            }

            // Get all neighbors that are within the bounds of the maze and have all 4 walls intact.
            List<MazeGenerationTraversalItem> nextTraversalItems = new ArrayList<>();
            for (Cell neighborCell: maze.getAdjacentCells(currentCell)) {
                if (!visited[neighborCell.getY()][neighborCell.getX()] && neighborCell.hasAllWalls()) {
                    nextTraversalItems.add(new MazeGenerationTraversalItem(neighborCell, currentCell));
                }
            }

            // Shuffle the neighbors so that we visit them in random order.
            // That will make our maze much more interesting.
            Collections.shuffle(nextTraversalItems);

            stack.addAll(nextTraversalItems);
        }

        return maze;
    }
}
