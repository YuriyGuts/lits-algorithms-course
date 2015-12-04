import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.function.Consumer;
import java.util.stream.Collectors;

public class MazeSolver {

    public MazeSolution solve(Maze maze, Consumer<CellSolvedEvent> cellSolvedCallback, Consumer<ExitPathUpdatedEvent> exitPathUpdatedCallback) {
        // Just doing the typical BFS, but, in addition to the cell itself,
        // we'll also store the length of the (start -> cell) path in the queue.
        // Because it's BFS and the graph is not weighted, the path length will
        // also be the MINIMUM path length. Obviously, the length is 0 for the start cell.
        // We'll wrap these (currentCell, pathLength) pairs in the MazeSolutionTraversalItem class.
        Queue<MazeSolutionTraversalItem> queue = new ArrayDeque<>();
        queue.add(new MazeSolutionTraversalItem(maze.getCellByCoordinate(0, 0), 0));

        boolean[][] visited = new boolean[maze.getHeight()][maze.getWidth()];

        // Remembering the shortest path lengths for every cell in the maze.
        int[][] pathLengths = new int[maze.getHeight()][maze.getWidth()];

        while (!queue.isEmpty()) {
            // Fetch the next (cell, steps) pair from the queue.
            MazeSolutionTraversalItem traversalItem = queue.remove();
            Cell currentCell = traversalItem.getCell();
            int pathLength = traversalItem.getMinPathLength();

            // Ignoring the cell if we've already been there.
            if (visited[currentCell.getY()][currentCell.getX()]) {
                continue;
            }

            // Mark this cell so we won't visit it anymore.
            visited[currentCell.getY()][currentCell.getX()] = true;
            pathLengths[currentCell.getY()][currentCell.getX()] = pathLength;

            // Notify the UI that we've solved a new cell.
            if (cellSolvedCallback != null) {
                cellSolvedCallback.accept(new CellSolvedEvent(traversalItem));
            }

            // Discovering the unvisited neighbors that are reachable from the current_cell
            // (the ones that don't have walls between them and our cell).
            List<Cell> unvisitedNeighbors = maze.getAdjacentReachableCells(currentCell).stream()
                    .filter((cell) -> !visited[cell.getY()][cell.getX()])
                    .collect(Collectors.toList());

            // Every neighbor will have a (pathLength + 1) minimum path length.
            for (Cell neighbor: unvisitedNeighbors) {
                queue.add(new MazeSolutionTraversalItem(neighbor, pathLength + 1));
            }
        }

        // Now that we've computed the matrix of all shortest path lengths,
        // we can reconstruct the path from the end cell to the start cell.
        List<Cell> exitPath = traceExitPath(
            maze,
            pathLengths,
            maze.getCellByCoordinate(0, 0),
            maze.getCellByCoordinate(maze.getWidth() - 1, maze.getHeight() - 1)
        );

        // Notify the UI that we've traced one more cell from the exit path.
        if (exitPathUpdatedCallback != null) {
            for (Cell cell: exitPath) {
                exitPathUpdatedCallback.accept(new ExitPathUpdatedEvent(cell));
            }
        }

        return new MazeSolution(pathLengths, exitPath);
    }

    private List<Cell> traceExitPath(Maze maze, int[][] pathLengths, Cell startCell, Cell exitCell) {
        List<Cell> path = new ArrayList<>();
        path.add(exitCell);

        Cell currentCell = exitCell;

        // At each step, move to any neighbor cell that has a path length of (steps - 1)
        // until we reach the start cell.
        while (!(currentCell.getX() == startCell.getX() && currentCell.getY() == startCell.getY())) {
            for (Cell neighbor: maze.getAdjacentReachableCells(currentCell)) {
                if (pathLengths[neighbor.getY()][neighbor.getX()] == pathLengths[currentCell.getY()][currentCell.getX()] - 1) {
                    path.add(neighbor);
                    currentCell = neighbor;
                    break;
                }
            }
        }

        return path;
    }
}
